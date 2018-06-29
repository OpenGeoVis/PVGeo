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


    def _GetRequestedTime(self, outInfo, idx=0):
        # USAGE: i = self._GetRequestedTime(outInfo)
        executive = self.GetExecutive()
        timesteps = self.__timesteps
        outInfo = outInfo.GetInformationObject(idx)
        if timesteps is None or len(timesteps) == 0:
            return 0
        elif outInfo.Has(executive.UPDATE_TIME_STEP()) and len(timesteps) > 0:
            utime = outInfo.Get(executive.UPDATE_TIME_STEP())
            return np.argmin(np.abs(timesteps - utime))
        else:
            # if we cant match the time, give first
            assert(len(timesteps) > 0)
            return 0


    def RequestInformation(self, request, inInfo, outInfo):
        self.__timesteps = _helpers.UpdateTimesteps(self, self.__fileNames, self.__dt)
        return 1


    #### Seters and Geters ####


    def SetTimeSteps(self, timesteps):
        """Only use this internally"""
        self.__timesteps = timesteps
        self.Modified()

    def GetTimeSteps(self):
        return self.__timesteps

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
