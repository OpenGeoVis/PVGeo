"""
This file contains the necessary VTKPythonAlgorithmBase subclasses to implement
functionality in this submodule as filters, sources, readers, and writers in
ParaView.
"""

__all__ = [
    'GSLibReader',
    'SGeMSGridReader'
]

# This is module to import. It provides VTKPythonAlgorithmBase, the base class
# for all python-based vtkAlgorithm subclasses in VTK and decorators used to
# 'register' the algorithm with ParaView along with information about UI.
#TODO:from paraview.util.vtkAlgorithm import *

import numpy as np
import vtk
from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase

# Local Imports
from ..base import PVGeoReaderBase
from .. import _helpers
from .gslib import *
from .sgems import *

class GSLibReader(PVGeoReaderBase):
    def __init__(self):
        PVGeoReaderBase.__init__(self,
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
        self.__header = gslibRead(self.GetFileNames(i), deli=self.__delimiter,
            useTab=self.__useTab, skiprows=self.__skipRows,
            comments=self.__comments, pdo=output)
        return 1


    #### Seters and Geters ####

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

    def GetFileHeader(self):
        if self.__header is None:
            raise RuntimeError("Input file has not been read yet.")
        return self.__header


##########


class SGeMSGridReader(PVGeoReaderBase):
    def __init__(self):
        PVGeoReaderBase.__init__(self,
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
