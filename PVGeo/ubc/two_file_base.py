all = [
    'TwoFileReaderBase',
]

from . import _helpers

# Outside Imports:
from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase
import numpy as np


# Two File Reader Base
class TwoFileReaderBase(VTKPythonAlgorithmBase):
    def __init__(self, nOutputPorts=1, outputType='vtkUnstructuredGrid'):
        VTKPythonAlgorithmBase.__init__(self,
            nInputPorts=0,
            nOutputPorts=nOutputPorts, outputType=outputType)
        self.__dt = 1.0
        self.__timesteps = None
        self.__meshFileName = None # Can only be one!
        self.__modelFileNames = [] # Can be many (single attribute, manytimesteps)


    def _GetTimeSteps(self):
        return self.__timesteps.tolist() if self.__timesteps is not None else None

    def _UpdateTimeSteps(self):
        """for internal use only"""
        self.__timesteps = _helpers.UpdateTimesteps(self, self.__modelFileNames, self.__dt)

    def RequestInformation(self, request, inInfo, outInfo):
        self._UpdateTimeSteps()
        return 1


    #### Seters and Geters ####

    def GetTimestepValues(self):
        """Use this in ParaView decorator to register timesteps"""
        return self._GetTimeSteps()

    def SetTimeDelta(self, dt):
        """An advanced property for the time step in seconds."""
        if dt != self.__dt:
            self.__dt = dt
            self.Modified()

    def ClearMeshFileName(self):
        """Use to clear mesh file name"""
        self.__meshFileName = None

    def ClearModelFileNames(self):
        """Use to clear data file names"""
        self.__modelFileNames = []

    def AddModelFileName(self, fname):
        """Use to set the file names for the reader. Handles singlt string or list of strings."""
        if fname is None:
            return # do nothing if None is passed by a constructor on accident
        if isinstance(fname, list):
            for f in fname:
                self.AddModelFileName(f)
        elif fname not in self.__modelFileNames:
            self.__modelFileNames.append(fname)
        self.Modified()

    def GetModelFileNames(self, idx=None):
        """Returns the list of file names or given and index returns a specified timestep's filename"""
        if idx is None:
            return self.__modelFileNames
        return self.__modelFileNames[idx]

    def GetMeshFileName(self):
        return self.__meshFileName


###############################################################################


# Two File Reader Base
class ubcMeshReaderBase(TwoFileReaderBase):
    def __init__(self, nOutputPorts=1, outputType='vtkUnstructuredGrid'):
        TwoFileReaderBase.__init__(self,
            nOutputPorts=nOutputPorts, outputType=outputType)
