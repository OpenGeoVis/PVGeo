__all__ = [
    'AlgorithmBase',
    'ReaderBase',
    'FilterPreserveTypeBase',
    'TwoFileReaderBase',
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
    We implement our algorithms in this manner to harness all of the backend support that the ``VTKPythonAlgorithmBase`` class provides for integrating custom algorithms on a VTK pipeline. All of the pipeline methods for setting inputs, getting outputs, making requests are handled by the super classes. For more information on what functionality is available, check out the VTK Docs for the `vtkAlgorithm`_ and then check out the following blog posts:

    * `vtkPythonAlgorithm is great`_
    * A VTK pipeline primer `(part 1)`_, `(part 2)`_, and `(part 3)`_

    .. _vtkAlgorithm: https://www.vtk.org/doc/nightly/html/classvtkAlgorithm.html
    .. _vtkPythonAlgorithm is great: https://blog.kitware.com/vtkpythonalgorithm-is-great/
    .. _(part 1): https://blog.kitware.com/a-vtk-pipeline-primer-part-1/
    .. _(part 2): https://blog.kitware.com/a-vtk-pipeline-primer-part-2/
    .. _(part 3): https://blog.kitware.com/a-vtk-pipeline-primer-part-3/
    """
    __displayname__ = 'Algorithm Base'
    __type__ = 'base'

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
    """A base class for inherrited functionality common to all reader algorithms
    """
    __displayname__ = 'Reader Base'
    __type__ = 'base'
    def __init__(self, nOutputPorts=1, outputType='vtkTable', **kwargs):
        AlgorithmBase.__init__(self,
            nInputPorts=0,
            nOutputPorts=nOutputPorts, outputType=outputType,
            **kwargs)
        # Attributes are namemangled to ensure proper setters/getters are used
        # For the VTK/ParaView pipeline
        self.__dt = kwargs.get('dt', 1.0)
        self.__timesteps = None
        # For the reader
        self.__fileNames = kwargs.get('filenames', [])
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

    def Apply(self, fname):
        """Given a file name (or list of file names), perfrom the read"""
        self.AddFileName(fname)
        self.Update()
        return self.GetOutput()

###############################################################################

# Base filter to preserve input data type
class FilterBase(AlgorithmBase):
    """A base class for implementing filters which holds several convienace methods"""
    __displayname__ = 'Filter Base'
    __type__ = 'base'
    def __init__(self,
        nInputPorts=1, inputType='vtkDataSet',
        nOutputPorts=1, outputType='vtkPolyData'):
        AlgorithmBase.__init__(self,
            nInputPorts=nInputPorts, inputType=inputType,
            nOutputPorts=nOutputPorts, outputType=outputType)

    def Apply(self, inputDataObject):
        self.SetInputDataObject(inputDataObject)
        self.Update()
        return self.GetOutput()



###############################################################################

# Base filter to preserve input data type
class FilterPreserveTypeBase(FilterBase):
    """A Base class for implementing filters that preserve the data type of
    their arbitrary input.
    """
    __displayname__ = 'Filter Preserve Type Base'
    __type__ = 'base'
    def __init__(self):
        FilterBase.__init__(self,
            nInputPorts=1, inputType='vtkDataObject',
            nOutputPorts=1)

    # THIS IS CRUCIAL to preserve data type through filter
    def RequestDataObject(self, request, inInfo, outInfo):
        """There is no need to overwrite this. This method lets the pipeline
        know that the algorithm will dynamically decide the output data type
        based in the input data type.
        """
        self.OutputType = self.GetInputData(inInfo, 0, 0).GetClassName()
        self.FillOutputPortInformation(0, outInfo.GetInformationObject(0))
        return 1

###############################################################################

# Two File Reader Base
class TwoFileReaderBase(AlgorithmBase):
    """A base clase for readers that need to handle two input files.
    One meta-data file and a series of data files.
    """
    __displayname__ = 'Two File Reader Base'
    __type__ = 'base'
    def __init__(self, nOutputPorts=1, outputType='vtkUnstructuredGrid', **kwargs):
        AlgorithmBase.__init__(self,
            nInputPorts=0,
            nOutputPorts=nOutputPorts, outputType=outputType)
        self.__dt = kwargs.get('dt', 1.0)
        self.__timesteps = None
        self.__meshFileName = kwargs.get('meshfile', None) # Can only be one!
        modfiles = kwargs.get('modelfiles', []) # Can be many (single attribute, manytimesteps)
        if isinstance(modfiles, str):
            modfiles = [modfiles]
        self.__modelFileNames = modfiles
        self.__needToReadMesh = True
        self.__needToReadModels = True


    def __UpdateTimeSteps(self):
        """For internal use only
        """
        if len(self.__modelFileNames) > 0:
            self.__timesteps = _helpers.UpdateTimeSteps(self, self.__modelFileNames, self.__dt)
        return 1

    def NeedToReadMesh(self, flag=None):
        """Ask self if the reader needs to read the mesh file again.

        Args:
            flag (bool): set the status of the reader for mesh files.
        """
        if flag is not None and isinstance(flag, (bool, int)):
            self.__needToReadMesh = flag
        return self.__needToReadMesh

    def NeedToReadModels(self, flag=None):
        """Ask self if the reader needs to read the model files again.

        Args:
            flag (bool): set the status of the reader for model files.
        """
        if flag is not None and isinstance(flag, (bool, int)):
            self.__needToReadModels = flag
        return self.__needToReadModels

    def Modified(self, readAgainMesh=True, readAgainModels=True):
        """Call modified if the files needs to be read again again

        Args:
            readAgainMesh (bool): set the status of the reader for mesh files.
            readAgainModels (bool): set the status of the reader for model files.
        """
        if readAgainMesh: self.NeedToReadMesh(flag=readAgainMesh)
        if readAgainModels: self.NeedToReadModels(flag=readAgainModels)
        return AlgorithmBase.Modified(self)

    def RequestInformation(self, request, inInfo, outInfo):
        self.__UpdateTimeSteps()
        return 1


    #### Seters and Geters ####


    @staticmethod
    def HasModels(modelfiles):
        """A convienance method to see if a list contatins models filenames.
        """
        if isinstance(modelfiles, list):
            return len(modelfiles) > 0
        return modelfiles is not None

    def ThisHasModels(self):
        """Ask self if the reader has model filenames set.
        """
        return TwoFileReaderBase.HasModels(self.__modelFileNames)

    def GetTimestepValues(self):
        """Use this in ParaView decorator to register timesteps
        """
        return self.__timesteps.tolist() if self.__timesteps is not None else None

    def SetTimeDelta(self, dt):
        """An advanced property for the time step in seconds.
        """
        if dt != self.__dt:
            self.__dt = dt
            self.Modified(readAgainMesh=False, readAgainModels=False)

    def ClearMesh(self):
        """Use to clear mesh file name
        """
        self.__meshFileName = None
        self.Modified(readAgainMesh=True, readAgainModels=False)

    def ClearModels(self):
        """Use to clear data file names
        """
        self.__modelFileNames = []
        self.Modified(readAgainMesh=False, readAgainModels=True)

    def SetMeshFileName(self, fname):
        """Set the mesh file name.
        """
        if self.__meshFileName != fname:
            self.__meshFileName = fname
            self.Modified(readAgainMesh=True, readAgainModels=False)

    def AddModelFileName(self, fname):
        """Use to set the file names for the reader. Handles single string or list of strings.

        Args:
            fname (str or list(str)): the file name(s) to use for the model data.
        """
        if fname is None:
            return # do nothing if None is passed by a constructor on accident
        if isinstance(fname, list):
            for f in fname:
                self.AddModelFileName(f)
            self.Modified(readAgainMesh=False, readAgainModels=True)
        elif fname not in self.__modelFileNames:
            self.__modelFileNames.append(fname)
            self.Modified(readAgainMesh=False, readAgainModels=True)
        return 1

    def GetModelFileNames(self, idx=None):
        """Returns the list of file names or given and index returns a specified
        timestep's filename.
        """
        if idx is None or not self.ThisHasModels():
            return self.__modelFileNames
        return self.__modelFileNames[idx]

    def GetMeshFileName(self):
        return self.__meshFileName

    def Apply(self):
        """Perfrom the read with parameters/file names set during init or by setters"""
        self.Update()
        return self.GetOutput()
