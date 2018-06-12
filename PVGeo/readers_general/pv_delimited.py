"""
This file contains the necessary VTKPythonAlgorithmBase subclasses to implement
functionality in this submodule as filters, sources, readers, and writers in
ParaView.
"""


# This is module to import. It provides VTKPythonAlgorithmBase, the base class
# for all python-based vtkAlgorithm subclasses in VTK and decorators used to
# 'register' the algorithm with ParaView along with information about UI.
#TODO:from paraview.util.vtkAlgorithm import *

__all__ = [
    'DelimitedTextReader',
]

import numpy as np
import vtk
from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase

# Local Imports
from ..base import PVGeoReaderBase
from .. import _helpers
from .delimited import *

class DelimitedTextReader(PVGeoReaderBase):
    def __init__(self):
        PVGeoReaderBase.__init__(self,
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

class XYZTextReader(PVGeoReaderBase):
    def __init__(self):
        PVGeoReaderBase.__init__(self,
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
