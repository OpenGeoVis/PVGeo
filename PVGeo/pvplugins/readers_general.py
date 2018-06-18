__all__ = [
    'vtkPackedBinariesReader',
    'vtkDelimitedTextReader',
    'vtkXYZTextReader',
]

# Outside Modules
import numpy as np
import vtk
from vtk.util import numpy_support as nps
import warnings
# Get plugin generator imports
try:
    # This is module to import. It provides VTKPythonAlgorithmBase, the base class
    # for all python-based vtkAlgorithm subclasses in VTK and decorators used to
    # 'register' the algorithm with ParaView along with information about UI.
    from paraview.util.vtkAlgorithm import *
except ImportError:
    from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase
    from PVGeo._detail import *

# PVGeo Imports
import PVGeo
from PVGeo import vtkPVGeoReaderBase
from PVGeo import _helpers
from PVGeo.readers_general import packedBinaries, madagascar
from PVGeo.readers_general import delimitedText, xyzRead

@smproxy.reader(name="vtkPackedBinariesReader",
       label="PackedBinariesReader",
       extensions="bin H@ rsf",
       file_description="PackedBinariesReader")
class vtkPackedBinariesReader(vtkPVGeoReaderBase):
    def __init__(self):
        vtkPVGeoReaderBase.__init__(self,
            nOutputPorts=1, outputType='vtkTable')
        # Other Parameters
        self.__dataName = "Data"
        self.__endian = ''
        self.__dtype = 'f'
        self.__madagascar = False


    def RequestData(self, request, inInfo, outInfo):
        # Get output:
        output = vtk.vtkTable.GetData(outInfo)
        # Get requested time index
        i = _helpers.getTimeStepFileIndex(self, self.GetFileNames(), dt=self.GetTimeStep())

        if self.__madagascar:
            madagascar(self.GetFileNames()[i], dataNm=self.GetDataName(), endian=self.GetEndian(), dtype=self.GetDType(), pdo=output)
        else:
            packedBinaries(self.GetFileNames()[i], dataNm=self.__dataName, endian=self.__endian, dtype=self.__dtype, pdo=output)

        return 1

    #### Seters and Geters ####
    @smproperty.stringvector(name="FileNames")
    @smdomain.filelist()
    def SetFileNames(self, fnames):
        vtkPVGeoReaderBase.SetFileNames(self, fnames)

    @smproperty.doublevector(name="TimeStep", default_values=1.0, panel_visibility="adcanced")
    def SetTimeStep(self, timeStep):
        vtkPVGeoReaderBase.SetTimeStep(self, timeStep)

    def SetEndian(self, endian):
        if endian != self.__endian:
            self.__endian = endian
            self.Modified()

    def GetEndian(self):
        return self.__endian

    def SetDType(self, dtype):
        if dtype != self.__dtype:
            self.__dtype = dtype
            self.Modified()

    def GetDType(self):
        return self.__dtype

    def SetDataName(self, dataName):
        if dataName != self.__dataName:
            self.__dataName = dataName
            self.Modified()

    def GetDataName(self):
        return self.__dataName

    def SetMadagascar(self, flag):
        if flag != self.__madagascar:
            self.__madagascar = flag
            self.Modified()


#########


@smproxy.reader(name="vtkDelimitedTextReader",
       label="vtkDelimitedTextReader",
       extensions="",
       file_description="PackedBinariesReader")
class vtkDelimitedTextReader(vtkPVGeoReaderBase):
    def __init__(self):
        vtkPVGeoReaderBase.__init__(self,
            nOutputPorts=1, outputType='vtkTable')

        # Other Parameters:
        self.__delimiter = " "
        self.__useTab = False
        self.__skipRows = 0
        self.__comments = "#"
        self.__hasTitles = True


    def RequestData(self, request, inInfo, outInfo):
        # Get output:
        output = vtk.vtkTable.GetData(outInfo)
        # Get requested time index
        i = _helpers.getTimeStepFileIndex(self, self.GetFileNames(), dt=self.GetTimeStep())
        # Read file and generate output
        delimitedText(self.GetFileNames()[i], deli=self.__delimiter,
            useTab=self.__useTab, hasTits=self.__hasTitles,
            skiprows=self.__skipRows, comments=self.__comments, pdo=output)
        return 1


    #### Seters and Geters ####
    @smproperty.stringvector(name="FileNames")
    @smdomain.filelist()
    def SetFileNames(self, fnames):
        vtkPVGeoReaderBase.SetFileNames(self, fnames)

    @smproperty.doublevector(name="TimeStep", default_values=1.0, panel_visibility="adcanced")
    def SetTimeStep(self, timeStep):
        vtkPVGeoReaderBase.SetTimeStep(self, timeStep)

    def SetDelimiter(self, deli):
        if deli != self.__delimiter:
            self.__delimiter = deli
            self.Modified()

    def SetUseTab(self, flag):
        if flag != self.__useTab:
            self.__useTab = flag
            self.Modified()

    def SetSkipRows(self, skip):
        if skip != self.__skipRows:
            self.__skipRows = skip
            self.Modified()

    def SetComments(self, identifier):
        if identifier != self.__comments:
            self.__comments = identifier
            self.Modified()


###

class vtkXYZTextReader(vtkPVGeoReaderBase):
    def __init__(self):
        vtkPVGeoReaderBase.__init__(self,
            nOutputPorts=1, outputType='vtkTable')

        # Other Parameters:
        self.__delimiter = " "
        self.__useTab = False
        self.__skipRows = 0
        self.__comments = "#"

    def RequestData(self, request, inInfo, outInfo):
        # Get output:
        output = vtk.vtkTable.GetData(outInfo)
        # Get requested time index
        i = _helpers.getTimeStepFileIndex(self, self.GetFileNames(), dt=self.GetTimeStep())
        # Read file and generate output
        xyzRead(self.GetFileNames(i), deli=self.__delimiter,
            useTab=self.__useTab, skiprows=self.__skipRows,
            comments=self.__comments, pdo=output)

    #### Seters and Geters ####
    @smproperty.stringvector(name="FileNames")
    @smdomain.filelist()
    def SetFileNames(self, fnames):
        vtkPVGeoReaderBase.SetFileNames(self, fnames)

    @smproperty.doublevector(name="TimeStep", default_values=1.0, panel_visibility="adcanced")
    def SetTimeStep(self, timeStep):
        vtkPVGeoReaderBase.SetTimeStep(self, timeStep)
