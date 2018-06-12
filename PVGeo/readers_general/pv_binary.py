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
    'PackedBinariesReader',
    'MadagascarReader'
]

import numpy as np
import vtk
from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase
from vtk.util import numpy_support as nps
import warnings

# Local Imports
from ..base import PVGeoReaderBase
from .. import _helpers
from .binaries import packedBinaries, madagascar


class PackedBinariesReader(PVGeoReaderBase):
    def __init__(self):
        PVGeoReaderBase.__init__(self,
            nOutputPorts=1, outputType='vtkTable')
        # Other Parameters
        self.__dataName = "Data"
        self.__endian = ''
        self.__dtype = 'f'


    def RequestData(self, request, inInfo, outInfo):
        # Get output:
        output = vtk.vtkTable.GetData(outInfo)
        # Get requested time index
        i = _helpers.getTimeStepFileIndex(self, self.GetFileNames(), dt=self.GetTimeStep())
        packedBinaries(self.GetFileNames()[i], dataNm=self.__dataName, endian=self.__endian, dtype=self.__dtype, pdo=output)
        return 1

    #### Seters and Geters ####

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


#########

class MadagascarReader(PackedBinariesReader):
    def __init__(self):
        PackedBinariesReader.__init__(self)

    def RequestData(self, request, inInfo, outInfo):
        # Get output:
        output = vtk.vtkTable.GetData(outInfo)
        # Get requested time index
        i = _helpers.getTimeStepFileIndex(self, self.GetFileNames(), dt=self.GetTimeStep())
        madagascar(self.GetFileNames()[i], dataNm=self.GetDataName(), endian=self.GetEndian(), dtype=self.GetDType(), pdo=output)
        return 1
