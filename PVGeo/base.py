__all__ = [
    'AlgorithmBase',
    'ReaderBaseBase',
    'ReaderBase',
    'FilterBase',
    'FilterPreserveTypeBase',
    'TwoFileReaderBase',
    'WriterBase',
    'InterfacedBaseReader',
]


__displayname__ = 'Base Classes'

import warnings

import numpy as np
# Outside Imports:
import vtk  # NOTE: This is the first import executed in the package! Keep here!!
import vtk.util.vtkAlgorithm as valg  # import VTKPythonAlgorithmBase

from . import _helpers
from . import interface

###############################################################################

class AlgorithmBase(valg.VTKPythonAlgorithmBase):
    """This is a base class to add convienace methods to the
    ``VTKPythonAlgorithmBase`` for all algorithms implemented in ``PVGeo``.
    We implement our algorithms in this manner to harness all of the backend
    support that the ``VTKPythonAlgorithmBase`` class provides for integrating
    custom algorithms on a VTK pipeline. All of the pipeline methods for setting
    inputs, getting outputs, making requests are handled by the super classes.
    For more information on what functionality is available, check out the VTK
    Docs for the `vtkAlgorithm`_ and then check out the following blog posts:

    * `vtkPythonAlgorithm is great`_
    * A VTK pipeline primer `(part 1)`_, `(part 2)`_, and `(part 3)`_
    * `ParaView Python Docs`_

    .. _vtkAlgorithm: https://www.vtk.org/doc/nightly/html/classvtkAlgorithm.html
    .. _vtkPythonAlgorithm is great: https://blog.kitware.com/vtkpythonalgorithm-is-great/
    .. _(part 1): https://blog.kitware.com/a-vtk-pipeline-primer-part-1/
    .. _(part 2): https://blog.kitware.com/a-vtk-pipeline-primer-part-2/
    .. _(part 3): https://blog.kitware.com/a-vtk-pipeline-primer-part-3/
    .. _ParaView Python Docs: https://www.paraview.org/ParaView/Doc/Nightly/www/py-doc/paraview.util.vtkAlgorithm.html
    """
    __displayname__ = 'Algorithm Base'
    __category__ = 'base'

    def __init__(self,
                nInputPorts=1, inputType='vtkDataSet',
                nOutputPorts=1, outputType='vtkTable', **kwargs):
        valg.VTKPythonAlgorithmBase.__init__(self,
            nInputPorts=nInputPorts, inputType=inputType,
            nOutputPorts=nOutputPorts, outputType=outputType)
        # Add error handler to make errors easier to deal with
        self.__error_observer = _helpers.ErrorObserver()
        self.__error_observer.make_observer(self)

    def GetOutput(self, port=0):
        """A conveience method to get the output data object of this ``PVGeo``
        algorithm.
        """
        return interface.wrap_pyvista(self.GetOutputDataObject(port))

    def error_occurred(self):
        """A conveience method for handling errors on the VTK pipeline

        Return:
            bool: true if an error has ovvured since last checked
        """
        return self.__error_observer.error_occurred()

    def get_error_message(self):
        """A conveience method to print the error message.
        """
        return self.__error_observer.get_error_message()

    def apply(self):
        """Update the algorithm and get the output data object"""
        self.Update()
        return interface.wrap_pyvista(self.GetOutput())

    def update(self):
        """Alias for self.Update()"""
        return self.Update()

    def get_output(self, port=0):
        """Alias for self.GetOutput()"""
        return self.GetOutput(port=port)

###############################################################################
# Base Base Reader
class ReaderBaseBase(AlgorithmBase):
    """A base class for inherrited functionality common to all reader algorithms
    """
    __displayname__ = 'Reader Base Base'
    __category__ = 'base'
    def __init__(self, nOutputPorts=1, outputType='vtkTable', **kwargs):
        AlgorithmBase.__init__(self,
            nInputPorts=0,
            nOutputPorts=nOutputPorts, outputType=outputType, **kwargs)
        # Attributes are namemangled to ensure proper setters/getters are used
        # For the reader
        self.__filenames = kwargs.get('filenames', [])
        # To know whether or not the read needs to perform
        self.__need_to_read = True

    def need_to_read(self, flag=None):
        """Ask self if the reader needs to read the files again.

        Args:
            flag (bool): Set the read status

        Return:
            bool: the status of the reader.
        """
        if flag is not None and isinstance(flag, (bool, int)):
            self.__need_to_read = flag
        return self.__need_to_read

    def Modified(self, read_again=True):
        """Call modified if the files needs to be read again again
        """
        if read_again: self.__need_to_read = read_again
        AlgorithmBase.Modified(self)

    def modified(self, read_again=True):
        return self.Modified(read_again=read_again)

    #### Methods for performing the read ####
    # These are meant to be overwritten by child classes

    def _get_file_contents(self, idx=None):
        raise NotImplementedError()

    def _read_up_front(self):
        raise NotImplementedError()

    def _get_raw_data(self, idx=0):
        raise NotImplementedError()

    #### Seters and Geters ####

    def clear_file_names(self):
        """Use to clear file names of the reader.

        Note:
            This does not set the reader to need to read again as there are
            no files to read.
        """
        self.__filenames = []

    def AddFileName(self, filename):
        """Use to set the file names for the reader. Handles singlt string or
        list of strings.

        Args:
            filename (str): The absolute file name with path to read.
        """
        if filename is None:
            return # do nothing if None is passed by a constructor on accident
        if isinstance(filename, list):
            for f in filename:
                self.AddFileName(f)
        elif filename not in self.__filenames:
            self.__filenames.append(filename)
        self.Modified()

    def add_file_name(self, filename):
        """Use to set the file names for the reader. Handles singlt string or
        list of strings.

        Args:
            filename (str): The absolute file name with path to read.
        """
        return self.AddFileName(filename)

    def get_file_names(self, idx=None):
        """Returns the list of file names or given and index returns a specified
        timestep's filename.
        """
        if self.__filenames is None or len(self.__filenames) < 1:
            raise _helpers.PVGeoError('File names are not set.')
        if idx is None:
            return self.__filenames
        return self.__filenames[idx]

    def apply(self, filename):
        """Given a file name (or list of file names), perfrom the read"""
        self.AddFileName(filename)
        self.Update()
        return interface.wrap_pyvista(self.GetOutput())

###############################################################################

# Base filter to preserve input data type
class FilterBase(AlgorithmBase):
    """A base class for implementing filters which holds several convienace
    methods"""
    __displayname__ = 'Filter Base'
    __category__ = 'base'
    def __init__(self,
        nInputPorts=1, inputType='vtkDataSet',
        nOutputPorts=1, outputType='vtkPolyData', **kwargs):
        AlgorithmBase.__init__(self,
            nInputPorts=nInputPorts, inputType=inputType,
            nOutputPorts=nOutputPorts, outputType=outputType, **kwargs)

    def apply(self, input_data_object):
        """Run this algorithm on the given input dataset"""
        self.SetInputDataObject(input_data_object)
        self.Update()
        return interface.wrap_pyvista(self.GetOutput())



###############################################################################
# Base Reader
class ReaderBase(ReaderBaseBase):
    """A base class for inherrited functionality common to all reader algorithms
    that need to handle a time series.
    """
    __displayname__ = 'Reader Base: Time Varying'
    __category__ = 'base'
    def __init__(self, nOutputPorts=1, outputType='vtkTable', **kwargs):
        ReaderBaseBase.__init__(self,
            nOutputPorts=nOutputPorts, outputType=outputType, **kwargs)
        # Attributes are namemangled to ensure proper setters/getters are used
        # For the VTK/ParaView pipeline
        self.__dt = kwargs.get('dt', 1.0)
        self.__timesteps = None


    def _update_time_steps(self):
        """For internal use only: appropriately sets the timesteps.
        """
        if len(self.get_file_names()) > 1:
            self.__timesteps = _helpers.update_time_steps(self, self.get_file_names(), self.__dt)
        return 1

    #### Algorithm Methods ####

    def RequestInformation(self, request, inInfo, outInfo):
        """This is a conveience method that should be overwritten when needed.
        This will handle setting the timesteps appropriately based on the number
        of file names when the pipeline needs to know the time information.
        """
        self._update_time_steps()
        return 1


    #### Seters and Geters ####

    def get_time_step_values(self):
        """Use this in ParaView decorator to register timesteps on the pipeline.
        """
        return self.__timesteps.tolist() if self.__timesteps is not None else None

    def set_time_delta(self, dt):
        """An advanced property to set the time step in seconds.
        """
        if dt != self.__dt:
            self.__dt = dt
            self.Modified()


###############################################################################

# Base filter to preserve input data type
class FilterPreserveTypeBase(FilterBase):
    """A Base class for implementing filters that preserve the data type of
    their arbitrary input.
    """
    __displayname__ = 'Filter Preserve Type Base'
    __category__ = 'base'
    def __init__(self, nInputPorts=1, **kwargs):
        FilterBase.__init__(self,
            nInputPorts=nInputPorts, inputType=kwargs.pop('inputType', 'vtkDataObject'),
            nOutputPorts=1, **kwargs)
        self._preserve_port = 0 # This is the port to preserve data object type

    # THIS IS CRUCIAL to preserve data type through filter
    def RequestDataObject(self, request, inInfo, outInfo):
        """There is no need to overwrite this. This method lets the pipeline
        know that the algorithm will dynamically decide the output data type
        based in the input data type.
        """
        self.OutputType = self.GetInputData(inInfo, self._preserve_port, 0).GetClassName()
        self.FillOutputPortInformation(0, outInfo.GetInformationObject(0))
        return 1

###############################################################################

# Two File Reader Base
class TwoFileReaderBase(AlgorithmBase):
    """A base clase for readers that need to handle two input files.
    One meta-data file and a series of data files.
    """
    __displayname__ = 'Two File Reader Base'
    __category__ = 'base'
    def __init__(self, nOutputPorts=1, outputType='vtkUnstructuredGrid', **kwargs):
        AlgorithmBase.__init__(self,
            nInputPorts=0,
            nOutputPorts=nOutputPorts, outputType=outputType)
        self.__dt = kwargs.get('dt', 1.0)
        self.__timesteps = None
        self.__mesh_filename = kwargs.get('meshfile', None) # Can only be one!
        modfiles = kwargs.get('model_files', []) # Can be many (single attribute, manytimesteps)
        if isinstance(modfiles, str):
            modfiles = [modfiles]
        self.__model_filenames = modfiles
        self.__need_to_read_mesh = True
        self.__need_to_read_models = True


    def __update_time_steps(self):
        """For internal use only
        """
        if len(self.__model_filenames) > 0:
            self.__timesteps = _helpers.update_time_steps(self, self.__model_filenames, self.__dt)
        return 1

    def need_to_readMesh(self, flag=None):
        """Ask self if the reader needs to read the mesh file again.

        Args:
            flag (bool): set the status of the reader for mesh files.
        """
        if flag is not None and isinstance(flag, (bool, int)):
            self.__need_to_read_mesh = flag
        return self.__need_to_read_mesh

    def need_to_readModels(self, flag=None):
        """Ask self if the reader needs to read the model files again.

        Args:
            flag (bool): set the status of the reader for model files.
        """
        if flag is not None and isinstance(flag, (bool, int)):
            self.__need_to_read_models = flag
        return self.__need_to_read_models

    def Modified(self, read_again_mesh=True, read_again_models=True):
        """Call modified if the files needs to be read again again

        Args:
            read_again_mesh (bool): set the status of the reader for mesh files.
            read_again_models (bool): set the status of the reader for model files.
        """
        if read_again_mesh: self.need_to_readMesh(flag=read_again_mesh)
        if read_again_models: self.need_to_readModels(flag=read_again_models)
        return AlgorithmBase.Modified(self)

    def modified(self, read_again_mesh=True, read_again_models=True):
        return self.Modified(read_again_mesh=read_again_mesh, read_again_models=read_again_models)

    def RequestInformation(self, request, inInfo, outInfo):
        """Used by pipeline to handle setting up time variance"""
        self.__update_time_steps()
        return 1


    #### Seters and Geters ####


    @staticmethod
    def has_models(model_files):
        """A convienance method to see if a list contatins models filenames.
        """
        if isinstance(model_files, list):
            return len(model_files) > 0
        return model_files is not None

    def this_has_models(self):
        """Ask self if the reader has model filenames set.
        """
        return TwoFileReaderBase.has_models(self.__model_filenames)

    def get_time_step_values(self):
        """Use this in ParaView decorator to register timesteps
        """
        return self.__timesteps.tolist() if self.__timesteps is not None else None

    def set_time_delta(self, dt):
        """An advanced property for the time step in seconds.
        """
        if dt != self.__dt:
            self.__dt = dt
            self.Modified(read_again_mesh=False, read_again_models=False)

    def clear_mesh(self):
        """Use to clear mesh file name
        """
        self.__mesh_filename = None
        self.Modified(read_again_mesh=True, read_again_models=False)

    def clear_models(self):
        """Use to clear data file names
        """
        self.__model_filenames = []
        self.Modified(read_again_mesh=False, read_again_models=True)

    def set_mesh_filename(self, filename):
        """Set the mesh file name.
        """
        if self.__mesh_filename != filename:
            self.__mesh_filename = filename
            self.Modified(read_again_mesh=True, read_again_models=False)

    def add_model_file_name(self, filename):
        """Use to set the file names for the reader. Handles single string or
        list of strings.

        Args:
            filename (str or list(str)): the file name(s) to use for the model data.
        """
        if filename is None:
            return # do nothing if None is passed by a constructor on accident
        if isinstance(filename, list):
            for f in filename:
                self.add_model_file_name(f)
            self.Modified(read_again_mesh=False, read_again_models=True)
        elif filename not in self.__model_filenames:
            self.__model_filenames.append(filename)
            self.Modified(read_again_mesh=False, read_again_models=True)
        return 1

    def get_model_filenames(self, idx=None):
        """Returns the list of file names or given and index returns a specified
        timestep's filename.
        """
        if idx is None or not self.this_has_models():
            return self.__model_filenames
        return self.__model_filenames[idx]

    def get_mesh_filename(self):
        """Get the mesh filename"""
        return self.__mesh_filename

    def apply(self):
        """Perfrom the read with parameters/file names set during init or by
        setters"""
        self.Update()
        return interface.wrap_pyvista(self.GetOutput())


###############################################################################

class WriterBase(AlgorithmBase):
    __displayname__ = 'Writer Base'
    __category__ = 'base'
    def __init__(self, nInputPorts=1, inputType='vtkPolyData', **kwargs):
        AlgorithmBase.__init__(self, nInputPorts=nInputPorts, inputType=inputType,
                                     nOutputPorts=0)
        self.__filename = kwargs.get('filename', None)
        self.__fmt = '%.9e'
        # For composite datasets: not always used
        self.__blockfilenames = None
        self.__composite = False


    def FillInputPortInformation(self, port, info):
        """Allows us to save composite datasets as well.

        Note:
            I only care about ``vtkMultiBlockDataSet``
        """
        info.Set(self.INPUT_REQUIRED_DATA_TYPE(), self.InputType)
        info.Append(self.INPUT_REQUIRED_DATA_TYPE(), 'vtkMultiBlockDataSet') # vtkCompositeDataSet
        return 1


    def SetFileName(self, filename):
        """Specify the filename for the output. Writer can only handle a single
        output data object/time step."""
        if not isinstance(filename, str):
            raise RuntimeError('File name must be string. Only single file is supported.')
        if self.__filename != filename:
            self.__filename = filename
            self.Modified()

    def set_file_name(self, filename):
        """Specify the filename for the output. Writer can only handle a single
        output data object/time step."""
        return self.SetFileName(filename)

    def get_file_name(self):
        """Get the set filename."""
        return self.__filename

    def Write(self, input_data_object=None):
        """Perfrom the write out."""
        if input_data_object:
            self.SetInputDataObject(input_data_object)
        self.Modified()
        self.Update()

    def write(self, input_data_object=None):
        return self.write(input_data_object=input_data_object)

    def perform_write_out(self, input_data_object, filename, object_name):
        """This method must be implemented. This is automatically called by
        ``RequestData`` for single inputs or composite inputs."""
        raise NotImplementedError('perform_write_out must be implemented!')

    def apply(self, input_data_object):
        """Run this writer algorithm on the given input data object"""
        self.SetInputDataObject(input_data_object)
        self.Modified()
        self.Update()

    def set_format(self, fmt):
        """Use to set the ASCII format for the writer default is ``'%.9e'``"""
        if self.__fmt != fmt and isinstance(fmt, str):
            self.__fmt = fmt
            self.Modified()

    def get_format(self):
        """Get the ASCII format used for floats"""
        return self.__fmt

    #### Following methods are for composite datasets ####

    def use_composite(self):
        """True if input dataset is a composite dataset"""
        return self.__composite

    def set_block_filenames(self, n):
        """Gets a list of filenames based on user input filename and creates a
        numbered list of filenames for the reader to save out. Assumes the
        filename has an extension set already.
        """
        number = n
        count = 0
        while (number > 0):
            number = number // 10
            count = count + 1
        count = '%d' % count
        identifier = '_%.' + count + 'd'
        blocknum = [identifier % i for i in range(n)]
        # Check the file extension:
        ext = self.get_file_name().split('.')[-1]
        basename = self.get_file_name().replace('.%s' % ext, '')
        self.__blockfilenames = [basename + '%s.%s' % (blocknum[i], ext) for i in range(n)]
        return self.__blockfilenames

    def get_block_filename(self, idx):
        """Get filename for component of a multi block dataset"""
        return self.__blockfilenames[idx]


    def RequestData(self, request, inInfo, outInfo):
        """Subclasses must implement a ``perform_write_out`` method that takes an
        input data object and a filename. This method will automatically handle
        composite data sets.
        """
        inp = self.GetInputData(inInfo, 0, 0)
        if isinstance(inp, vtk.vtkMultiBlockDataSet):
            self.__composite = True
        # Handle composite datasets. NOTE: This only handles vtkMultiBlockDataSet
        if self.__composite:
            num = inp.GetNumberOfBlocks()
            self.set_block_filenames(num)
            for i in range(num):
                data = inp.GetBlock(i)
                name = inp.GetMetaData(i).Get(vtk.vtkCompositeDataSet.NAME())
                if data.IsTypeOf(self.InputType):
                    self.perform_write_out(data, self.get_block_filename(i), name)
                else:
                    warnings.warn('Input block %d of type(%s) not saveable by writer.' % (i, type(data)))
        # Handle single input dataset
        else:
            self.perform_write_out(inp, self.get_file_name(), None)
        return 1

###############################################################################

class InterfacedBaseReader(ReaderBase):
    """A general base reader for all interfacing with librarues that already
    have file I/O methods and VTK data object interfaces. This provides a
    routine for using an external library to handle all I/O and produce the
    VTK data objects."""
    __displayname__ = 'Interfaced Base Reader'
    def __init__(self, **kwargs):
        ReaderBase.__init__(self, **kwargs)
        self.__objects = []


    # THIS IS CRUCIAL to dynamically decided output type
    def RequestDataObject(self, request, inInfo, outInfo):
        """Do not override. This method lets the us dynamically decide the
        output data type based in the read meshes.
        Note: they all have to be the same VTK type.
        """
        self._read_up_front()
        self.FillOutputPortInformation(0, outInfo.GetInformationObject(0))
        return 1


    @staticmethod
    def _read_file(filename):
        """OVERRIDE: Reads from the the libraries format and returns an object
        in the given library's format."""
        raise NotImplementedError()

    @staticmethod
    def _get_vtk_object(obj):
        """OVERRIDE: Given an object in the interfaced library's type, return
        a converted VTK data object."""
        raise NotImplementedError()

    def _read_up_front(self):
        """Do not override. A predifiened routine for reading the files up front."""
        filenames = self.get_file_names()
        self.__objects = []
        for f in filenames:
            mesh = self._read_file(f)
            obj = self._get_vtk_object(mesh)
            self.__objects.append(obj)
        # Now check that all objects in list are same type and set output type
        typ = type(self.__objects[0])
        if not all(isinstance(x, typ) for x in self.__objects):
            raise _helpers.PVGeoError('Input VTK objects are not all of the same type.')
        self.OutputType = self.__objects[0].GetClassName()

    def _get_object_at_index(self, idx=None):
        """Internal helper to get the data object at the specified index"""
        if idx is not None:
            return self.__objects[idx]
        return self.__objects[0]

    def RequestData(self, request, inInfo, outInfo):
        """Do not override. Used by pipeline to get data for current timestep
        and populate the output data object.
        """
        # Get requested time index
        i = _helpers.get_requested_time(self, outInfo)
        # Get output:
        output = self.GetOutputData(outInfo, 0)
        output.ShallowCopy(self._get_object_at_index(idx=i))
        return 1

    def RequestInformation(self, request, inInfo, outInfo):
        """Do not override. Used by pipeline to set extents and time info.
        """
        # Call parent to handle time stuff
        ReaderBase.RequestInformation(self, request, inInfo, outInfo)
        # Now set whole output extent
        info = outInfo.GetInformationObject(0)
        obj = self.__objects[0] # Get first grid to set output extents
        # Set WHOLE_EXTENT: This is absolutely necessary
        ext = obj.GetExtent()
        info.Set(vtk.vtkStreamingDemandDrivenPipeline.WHOLE_EXTENT(), ext, 6)
        return 1

###############################################################################
