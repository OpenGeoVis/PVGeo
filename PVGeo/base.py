all = [
    'ReaderBase',
]

from . import _helpers

# Outside Imports:
from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase
import numpy as np


# Base Reader
class ReaderBase(VTKPythonAlgorithmBase):
    def __init__(self, nOutputPorts=1, outputType='vtkTable'):
        VTKPythonAlgorithmBase.__init__(self,
            nInputPorts=0,
            nOutputPorts=nOutputPorts, outputType=outputType)
        self.__dt = 1.0
        self.__timesteps = None
        self.__fileNames = []


    def _GetTimeSteps(self):
        return self.__timesteps.tolist() if self.__timesteps is not None else None

    def _UpdateTimeSteps(self):
        """for internal use only"""
        self.__timesteps = _helpers.UpdateTimesteps(self, self.__fileNames, self.__dt)

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

    def ClearFileNames(self):
        """Use to clear file names"""
        self.__fileNames = []

    def AddFileName(self, fname):
        """Use to set the file names for the reader. Handles singlt string or list of strings."""
        if fname is None:
            return # do nothing if None is passed by a constructor on accident
        if isinstance(fname, list):
            for f in fname:
                self.AddFileName(f)
        elif fname not in self.__fileNames:
            self.__fileNames.append(fname)
        self.Modified()

    def GetFileNames(self, idx=None):
        """Returns the list of file names or given and index returns a specified timestep's filename"""
        if idx is None:
            return self.__fileNames
        return self.__fileNames[idx]


###############################################################################
