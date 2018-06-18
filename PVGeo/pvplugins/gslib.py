"""
This file contains the necessary VTKPythonAlgorithmBase subclasses to implement
functionality in this submodule as filters, sources, readers, and writers in
ParaView.
"""

__all__ = [
    'vtkGSLibReader',
    'vtkSGeMSGridReader'
]

# This is module to import. It provides VTKPythonAlgorithmBase, the base class
# for all python-based vtkAlgorithm subclasses in VTK and decorators used to
# 'register' the algorithm with ParaView along with information about UI.
#TODO:from paraview.util.vtkAlgorithm import *

import numpy as np
import vtk

try:
    from paraview.util.vtkAlgorithm import *
except ImportError:
    from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase
    from PVGeo._detail import *

# Local Imports
from PVGeo import vtkPVGeoReaderBase
from PVGeo import _helpers
from PVGeo.gslib import sgemsGrid, sgemsExtent, gslibRead

@smproxy.reader(name="gslibRead",
       label="PVGeo: GSLIB File Format",
       extensions="sgems dat geoeas gslib GSLIB txt SGEMS",
       file_description="The GSLIB file format has headers lines followed by the data as a space delimited ASCI file (this filter is set up to allow you to choose any single character delimiter). The first header line is the title and will be printed to the console. This line may have the dimensions for a grid to be made of the data. The second line is the number (n) of columns of data. The next n lines are the variable names for the data in each column. You are allowed up to ten characters for the variable name. The data follow with a space between each field (column).")
class vtkGSLibReader(vtkPVGeoReaderBase):
    def __init__(self):
        vtkPVGeoReaderBase.__init__(self,
            nOutputPorts=1, outputType='vtkTable')

        # Other Parameters
        self.__delimiter = " "
        self.__useTab = False
        self.__skipRows = 0
        self.__comments = "#"
        # These are attributes the derived from file contents:
        self.__header = None


    def RequestData(self, request, inInfo, outInfo):
        # Get output:
        output = vtk.vtkTable.GetData(outInfo)
        # Get requested time index
        i = _helpers.getTimeStepFileIndex(self, self.GetFileNames(), dt=self.GetTimeStep())
        print(i)
        self.__header = gslibRead(self.GetFileNames(i),             deli=self.__delimiter,
            useTab=self.__useTab, skiprows=self.__skipRows,
            comments=self.__comments, pdo=output)
        return 1


    #### Seters and Geters ####
    @smproperty.stringvector(name="FileNames", panel_visibility="adcanced")
    @smdomain.filelist()
    def SetFileNames(self, fnames):
        vtkPVGeoReaderBase.SetFileNames(self, fnames)

    @smproperty.doublevector(name="TimeStep", default_values=1.0, panel_visibility="adcanced")
    def SetTimeStep(self, timeStep):
        vtkPVGeoReaderBase.SetTimeStep(self, timeStep)

    @smproperty.stringvector(name="Delimiter", default_values=" ")
    def SetDelimiter(self, deli):
        if deli != self.__delimiter:
            self.__delimiter = deli
            self.Modified()

    @smproperty.xml(_helpers.getPropertyXml('UseTab', 'Use Tab Delimiter', 'SetUseTab', False, help='A boolean to override the Delimiter_Field and use a Tab delimiter.'))
    def SetUseTab(self, flag):
        if flag != self.__useTab:
            self.__useTab = flag
            print('flag set! Tab')
            self.Modified()

    @smproperty.intvector(name="SkipRows", default_values=0)
    def SetSkipRows(self, skip):
        if skip != self.__skipRows:
            self.__skipRows = skip
            self.Modified()

    @smproperty.stringvector(name="Comments", default_values="#")
    def SetComments(self, identifier):
        if identifier != self.__comments:
            self.__comments = identifier
            self.Modified()

    def GetFileHeader(self):
        if self.__header is None:
            raise RuntimeError("Input file has not been read yet.")
        return self.__header


##########


@smproxy.reader(name="SGeMSGridReader",
       label="SGeMSGridReader",
       extensions="dat gslib sgems SGEMS",
       file_description="Dummy Reader... gslibRead")
class vtkSGeMSGridReader(vtkPVGeoReaderBase):
    def __init__(self):
        vtkPVGeoReaderBase.__init__(self,
            nOutputPorts=1, outputType='vtkImageData')

        # Other Parameters:
        self.__delimiter = " "
        self.__useTab = False
        self.__skipRows = 0
        self.__comments = "#"


    def RequestData(self, request, inInfo, outInfo):
        # Get requested time index
        i = _helpers.getTimeStepFileIndex(self, self.GetFileNames(), dt=self.GetTimeStep())
        output = vtk.vtkImageData.GetData(outInfo)
        sgemsGrid(self.GetFileNames(i), deli=self.__delimiter,
            useTab=self.__useTab, skiprows=self.__skipRows,
            comments=self.__comments, pdo=output)
        return 1


    def RequestInformation(self, request, inInfo, outInfo):
        _helpers.setOutputTimesteps(self, self.GetFileNames(), dt=self.GetTimeStep())
        # Now set whole output extent
        ext = sgemsExtent(self.GetFileNames(0), deli=self.__delimiter,
            useTab=self.__useTab, comments=self.__comments)
        info = outInfo.GetInformationObject(0)
        # Set WHOLE_EXTENT: This is absolutely necessary
        info.Set(vtk.vtkStreamingDemandDrivenPipeline.WHOLE_EXTENT(), ext, 6)
        return 1


    #### Seters and Geters ####
    @smproperty.stringvector(name="FileNames")
    @smdomain.filelist()
    def SetFileNames(self, fnames):
        vtkPVGeoReaderBase.SetFileNames(self, fnames)

    @smproperty.doublevector(name="TimeStep", default_values=1.0, panel_visibility="adcanced")
    def SetTimeStep(self, timeStep):
        vtkPVGeoReaderBase.SetTimeStep(self, timeStep)
