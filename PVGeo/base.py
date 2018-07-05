all = [
    'PVGeoReaderBase',
    'FilterPreserveTypeBase'
]

from . import _helpers

# Outside Imports:
from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase
import numpy as np

###############################################################################

class PVGeoAlgorithmBase(VTKPythonAlgorithmBase):
    """This is a base class to add convienace methods to the `VTKPythonAlgorithmBase`"""
    def __init__(self,
                nInputPorts=1, inputType='vtkDataSet',
                nOutputPorts=1, outputType='vtkTable'):
        VTKPythonAlgorithmBase.__init__(self,
            nInputPorts=nInputPorts, inputType=inputType,
            nOutputPorts=nOutputPorts, outputType=outputType)

    def GetOutput(self, port=0):
        return self.GetOutputDataObject(port)


###############################################################################

# Base Reader
class PVGeoReaderBase(PVGeoAlgorithmBase):
    def __init__(self, nOutputPorts=1, outputType='vtkTable'):
        PVGeoAlgorithmBase.__init__(self,
            nInputPorts=0,
            nOutputPorts=nOutputPorts, outputType=outputType)
        # For the VTK/ParaView pipeline
        self.__dt = 1.0
        self.__timesteps = None
        # For the reader
        self.__fileNames = []
        # To know whether or not the read needs to perform
        self.__needToRead = True

    def _NeedToRead(self):
        """Ask self if the reader needs to read the files again"""
        return self.__needToRead

    def _SetAsRead(self):
        self.__needToRead = False

    def Modified(self, readAgain=True):
        """Call modified if the files needs to be read again again"""
        self.__needToRead = readAgain
        PVGeoAlgorithmBase.Modified(self)

    def _GetTimeSteps(self):
        return self.__timesteps.tolist() if self.__timesteps is not None else None

    def _UpdateTimeSteps(self):
        """for internal use only"""
        self.__timesteps = _helpers.UpdateTimesteps(self, self.__fileNames, self.__dt)

    def RequestInformation(self, request, inInfo, outInfo):
        self._UpdateTimeSteps()
        return 1

    #### Methods for performing the read ####

    def _GetFileContents(self):
        raise NotImplementedError()

    def _ReadUpFront(self):
        raise NotImplementedError()

    def _GetRawData(self, idx=0):
        raise NotImplementedError()

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

# Base filter to preserve input data type
class FilterPreserveTypeBase(PVGeoAlgorithmBase):
    def __init__(self):
        PVGeoAlgorithmBase.__init__(self,
            nInputPorts=1, inputType='vtkDataSet',
            nOutputPorts=1)

    # THIS IS CRUCIAL to preserve data type through filter
    def RequestDataObject(self, request, inInfo, outInfo):
        """Overwritten by subclass to manage data object creation.
        There is not need to overwrite this class if the output can
        be created based on the OutputType data member."""
        self.OutputType = self.GetInputData(inInfo, 0, 0).GetClassName()
        self.FillOutputPortInformation(0, outInfo.GetInformationObject(0))
        return 1
