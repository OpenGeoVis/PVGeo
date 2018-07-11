__all__ = [
    'AlgorithmBase',
    'ReaderBase',
    'FilterPreserveTypeBase'
]


__displayname__ = 'Base Classes'

from . import _helpers

# Outside Imports:
import vtk.util.vtkAlgorithm as valg #import VTKPythonAlgorithmBase
import numpy as np

###############################################################################

class AlgorithmBase(valg.VTKPythonAlgorithmBase):
    """This is a base class to add convienace methods to the
    ``VTKPythonAlgorithmBase`` for all algorithms implemented in ``PVGeo``.
    """
    def __init__(self,
                nInputPorts=1, inputType='vtkDataSet',
                nOutputPorts=1, outputType='vtkTable'):
        valg.VTKPythonAlgorithmBase.__init__(self,
            nInputPorts=nInputPorts, inputType=inputType,
            nOutputPorts=nOutputPorts, outputType=outputType)
        # Add error handler to make errors easier to deal with
        self.__errorObserver = _helpers.ErrorObserver()
        self.__errorObserver.MakeObserver(self)

    def GetOutput(self, port=0):
        """A conveience method to get the output data object of this ``PVGeo`` algorithm.
        """
        return self.GetOutputDataObject(port)

    def ErrorOccurred(self):
        """A conveience method for handling errors on the VTK pipeline

        Return:
            bool: true if an error has ovvured since last checked
        """
        return self.__errorObserver.ErrorOccurred()

    def ErrorMessage(self):
        """A conveience method to print the error message.
        """
        return self.__errorObserver.ErrorMessage()


###############################################################################

# Base Reader
class ReaderBase(AlgorithmBase):
    def __init__(self, nOutputPorts=1, outputType='vtkTable'):
        AlgorithmBase.__init__(self,
            nInputPorts=0,
            nOutputPorts=nOutputPorts, outputType=outputType)
        # Attributes are namemangled to ensure proper setters/getters are used
        # For the VTK/ParaView pipeline
        self.__dt = 1.0
        self.__timesteps = None
        # For the reader
        self.__fileNames = []
        # To know whether or not the read needs to perform
        self.__needToRead = True

    def NeedToRead(self, flag=None):
        """Ask self if the reader needs to read the files again.

        Args:
            flag (bool): Set the read status

        Return:
            bool: the status of the reader.
        """
        if flag is not None and isinstance(flag, (bool, int)):
            self.__needToRead = flag
        return self.__needToRead

    def Modified(self, readAgain=True):
        """Call modified if the files needs to be read again again
        """
        if readAgain: self.__needToRead = readAgain
        AlgorithmBase.Modified(self)

    def _UpdateTimeSteps(self):
        """For internal use only: appropriately sets the timesteps.
        """
        self.__timesteps = _helpers.UpdateTimeSteps(self, self.__fileNames, self.__dt)
        return 1

    #### Algorithm Methods ####

    def RequestInformation(self, request, inInfo, outInfo):
        """This is a conveience method that should be overwritten when needed.
        This will handle setting the timesteps appropriately based on the number
        of file names when the pipeline needs to know the time information.
        """
        self._UpdateTimeSteps()
        return 1

    #### Methods for performing the read ####
    # These are meant to be overwritten by child classes

    def _GetFileContents(self, idx=None):
        raise NotImplementedError()

    def _ReadUpFront(self):
        raise NotImplementedError()

    def _GetRawData(self, idx=0):
        raise NotImplementedError()

    #### Seters and Geters ####

    def GetTimestepValues(self):
        """Use this in ParaView decorator to register timesteps on the pipeline.
        """
        return self.__timesteps.tolist() if self.__timesteps is not None else None

    def SetTimeDelta(self, dt):
        """An advanced property to set the time step in seconds.
        """
        if dt != self.__dt:
            self.__dt = dt
            self.Modified()

    def ClearFileNames(self):
        """Use to clear file names of the reader.

        Note:
            * This does not set the reader to need to read again as there are no files to read.
        """
        self.__fileNames = []

    def AddFileName(self, fname):
        """Use to set the file names for the reader. Handles singlt string or list of strings.
        Args:
            fname (str): The absolute file name with path to read.
        """
        if fname is None:
            return # do nothing if None is passed by a constructor on accident
        if isinstance(fname, list):
            for f in fname:
                self.AddFileName(f)
        elif fname not in self.__fileNames:
            self.__fileNames.append(fname)
        self.Modified()

    def GetFileNames(self, idx=None):
        """Returns the list of file names or given and index returns a specified
        timestep's filename.
        """
        if idx is None:
            return self.__fileNames
        return self.__fileNames[idx]


###############################################################################

# Base filter to preserve input data type
class FilterPreserveTypeBase(AlgorithmBase):
    """A Base class for implementing filters that preserve the data type of
    their input.
    """
    def __init__(self):
        AlgorithmBase.__init__(self,
            nInputPorts=1, inputType='vtkDataObject',
            nOutputPorts=1)

    # THIS IS CRUCIAL to preserve data type through filter
    def RequestDataObject(self, request, inInfo, outInfo):
        """There is no need to overwrite this. This method lets the pipeline
        know that the algorithm will dynamically decide the output dat type
        based in the input data type.
        """
        self.OutputType = self.GetInputData(inInfo, 0, 0).GetClassName()
        self.FillOutputPortInformation(0, outInfo.GetInformationObject(0))
        return 1
