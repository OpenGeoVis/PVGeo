__all__ = [
    'ubcMeshReaderBase',
    'ModelAppenderBase',
]

__displayname__ = 'Base Classes'

# Outside Imports:
import os
import numpy as np
import pandas as pd
import vtk

from .. import _helpers, base

###############################################################################


# UBC Mesh Reader Base
class ubcMeshReaderBase(base.TwoFileReaderBase):
    """A base class for the UBC mesh readers
    """
    __displayname__ = 'UBC Mesh Reader Base'
    __category__ = 'base'
    extensions = 'mesh msh dat txt text'
    def __init__(self, nOutputPorts=1, outputType='vtkUnstructuredGrid', **kwargs):
        base.TwoFileReaderBase.__init__(self,
            nOutputPorts=nOutputPorts, outputType=outputType,
            **kwargs)
        self.__data_name = 'Data'
        self.__use_filename = True # flag on whether or not to use the model file
                                 # extension as data name
        # For keeping track of type (2D vs 3D)
        self.__sizeM = None


    def is_3d(self):
        """Returns true if mesh is spatially references in three dimensions"""
        return self.__sizeM.shape[0] >= 3

    def is_2d(self):
        """Returns true if mesh is spatially references in only two dimensions"""
        return self.__sizeM.shape[0] == 1

    @staticmethod
    def _ubc_mesh_2d_part(FileName):
        """Internal helper to read 2D mesh file"""
        # This is a helper method to read file contents of mesh
        try:
            fileLines = np.genfromtxt(FileName, dtype=str, delimiter='\n', comments='!')
        except (IOError, OSError) as fe:
            raise _helpers.PVGeoError(str(fe))

        def _genTup(sft, n):
            # This reads in the data for a dimension
            pts = []
            disc = []
            for i in range(n):
                ln = fileLines[i+sft].split('!')[0].split()
                if i is 0:
                    o = ln[0]
                    pts.append(o)
                    ln = [ln[1],ln[2]]
                pts.append(ln[0])
                disc.append(ln[1])
            return pts, disc

        # Get the number of lines for each dimension
        nx = int(fileLines[0].split('!')[0])
        nz = int(fileLines[nx+1].split('!')[0])

        # Get the origins and tups for both dimensions
        xpts, xdisc = _genTup(1, nx)
        zpts, zdisc = _genTup(2+nx, nz)

        return xpts, xdisc, zpts, zdisc

    def _read_extent(self):
        """Reads the mesh file for the UBC 2D/3D Mesh or OcTree format to get
        output extents. Computationally inexpensive method to discover whole
        output extent.

        Return:
            tuple(int) :
                This returns a tuple of the whole extent for the grid to be
                made of the input mesh file (0,n1-1, 0,n2-1, 0,n3-1). This
                output should be directly passed to set the whole output extent.

        """
        # Read the mesh file as line strings, remove lines with comment = !
        v = np.array(np.__version__.split('.')[0:2], dtype=int)
        FileName = self.get_mesh_filename()
        try:
            if v[0] >= 1 and v[1] >= 10:
                # max_rows in numpy versions >= 1.10
                msh = np.genfromtxt(FileName, delimiter='\n', dtype=np.str, comments='!', max_rows=1)
            else:
                # This reads whole file :(
                msh = np.genfromtxt(FileName, delimiter='\n', dtype=np.str, comments='!')[0]
        except (IOError, OSError) as fe:
            raise _helpers.PVGeoError(str(fe))
        # Fist line is the size of the model
        self.__sizeM = np.array(msh.ravel()[0].split(), dtype=int)
        # Check if the mesh is a UBC 2D mesh
        if self.__sizeM.shape[0] == 1:
            # Read in data from file
            xpts, xdisc, zpts, zdisc = ubcMeshReaderBase._ubc_mesh_2d_part(FileName)
            nx = np.sum(np.array(xdisc,dtype=int))+1
            nz = np.sum(np.array(zdisc,dtype=int))+1
            return (0,nx, 0,1, 0,nz)
        # Check if the mesh is a UBC 3D mesh or OcTree
        elif self.__sizeM.shape[0] >= 3:
            # Get mesh dimensions
            dim = self.__sizeM[0:3]
            ne,nn,nz = dim[0], dim[1], dim[2]
            return (0,ne, 0,nn, 0,nz)
        else:
            raise _helpers.PVGeoError('File format not recognized')


    @staticmethod
    def ubc_model_3d(FileName):
        """Reads the 3D model file and returns a 1D NumPy float array. Use the
        place_model_on_mesh() method to associate with a grid.

        Args:
            FileName (str) : The model file name(s) as an absolute path for the
                input model file in UBC 3D Model Model Format. Also accepts a
                `list` of string file names.

        Return:
            np.array :
                Returns a NumPy float array that holds the model data
                read from the file. Use the ``place_model_on_mesh()`` method to
                associate with a grid. If a list of file names is given then it
                will return a dictionary of NumPy float array with keys as the
                basenames of the files.
        """
        # Check if recurssion needed
        if isinstance(FileName, (list, tuple)):
            out = {}
            for f in FileName:
                out[os.path.basename(f)] = ubcMeshReaderBase.ubc_model_3d(f)
            return out
        # Perform IO
        try:
            data = np.genfromtxt(FileName, dtype=np.float, comments='!')
        except (IOError, OSError) as fe:
            raise _helpers.PVGeoError(str(fe))
        return data

    def set_use_filename(self, flag):
        """Set a flag on whether or not to use the filename as the data array name"""
        if self.__use_filename != flag:
            self.__use_filename = flag
            self.Modified(read_again_mesh=False, read_again_models=False)

    def set_data_name(self, name):
        """Set the data array name"""
        if name == '':
            self.__use_filename = True
            self.Modified(read_again_mesh=False, read_again_models=False)
        elif self.__data_name != name:
            self.__data_name = name
            self.__use_filename = False
            self.Modified(read_again_mesh=False, read_again_models=False)

    def get_data_name(self):
        """Get the data array name"""
        if self.__use_filename:
            mname = self.get_model_filenames(idx=0)
            return os.path.basename(mname)
        return self.__data_name




###############################################################################


# UBC Model Appender Base
class ModelAppenderBase(base.AlgorithmBase):
    """A base class for create mesh-model appenders on the UBC Mesh formats
    """
    __displayname__ = 'Model Appender Base'
    __category__ = 'base'
    def __init__(self, inputType='vtkRectilinearGrid', outputType='vtkRectilinearGrid', **kwargs):
        base.AlgorithmBase.__init__(self,
            nInputPorts=1, inputType=inputType,
            nOutputPorts=1, outputType=outputType)
        self._model_filenames = kwargs.get('model_files', [])
        self.__data_name = kwargs.get('dataname', 'Appended Data')
        self.__use_filename = True
        self._models = []
        self.__need_to_read = True
        self._is_3D = None
        # For the VTK/ParaView pipeline
        self.__dt = kwargs.get('dt', 1.0)
        self.__timesteps = None
        self.__last_successfull_index = 0 #This is the index to use if the current timestep is unavailable


    def need_to_read(self, flag=None):
        """Ask self if the reader needs to read the files again

        Args:
            flag (bool): if the flag is set then this method will set the read
                status

        Return:
            bool:
                The status of the reader aspect of the filter.
        """
        if flag is not None and isinstance(flag, (bool, int)):
            self.__need_to_read = flag
            self._update_time_steps()
        return self.__need_to_read

    def Modified(self, read_again=True):
        """Call modified if the files needs to be read again again.
        """
        if read_again: self.__need_to_read = read_again
        base.AlgorithmBase.Modified(self)

    def modified(self, read_again=True):
        """Call modified if the files needs to be read again again.
        """
        return self.Modified(read_again=read_again)

    def _update_time_steps(self):
        """For internal use only: appropriately sets the timesteps.
        """
        # Use the inputs' timesteps: this merges the timesteps values
        ts0 = _helpers.get_input_time_steps(self, port=0)
        if ts0 is None: ts0 = np.array([])
        ts1 = _helpers._calculate_time_range(len(self._model_filenames), self.__dt)
        tsAll = np.unique(np.concatenate((ts0, ts1), 0))
        # Use both inputs' time steps
        self.__timesteps = _helpers.update_time_steps(self, tsAll, explicit=True)
        return 1

    def _read_up_front(self):
        raise NotImpelementedError()

    def _place_on_mesh(self, output, idx=0):
        raise NotImplementedError()


    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output
        """
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        output = self.GetOutputData(outInfo, 0)
        output.DeepCopy(pdi) # ShallowCopy if you want changes to propagate upstream
        # Get requested time index
        i = _helpers.get_requested_time(self, outInfo)
        # Perfrom task:
        if self.__need_to_read:
            self._read_up_front()
        # Place the model data for given timestep onto the mesh
        if len(self._models) > i:
            self._place_on_mesh(output, idx=i)
            self.__last_successfull_index = i
        else:
            # put the last array as a placeholder
            self._place_on_mesh(output, idx=self.__last_successfull_index)
        return 1

    def RequestInformation(self, request, inInfo, outInfo):
        """Used by pipeline to handle time variance and update output extents
        """
        self._update_time_steps()
        pdi = self.GetInputData(inInfo, 0, 0)
        # Determine if 2D or 3D and read
        if isinstance(pdi, vtk.vtkRectilinearGrid) and pdi.GetExtent()[3] == 1:
            self._is_3D = False
        else:
            self._is_3D = True
        return 1

    #### Setters and Getters ####

    def has_models(self):
        """Return True if models are associated with this mesh"""
        return len(self._model_filenames) > 0

    def get_time_step_values(self):
        """Use this in ParaView decorator to register timesteps.
        """
        # if unset, force at least one attempt to set the timesteps
        if self.__timesteps is None: self._update_time_steps()
        return self.__timesteps if self.__timesteps is not None else None

    def clear_models(self):
        """Use to clear data file names.
        """
        self._model_filenames = []
        self._models = []
        self.Modified(read_again=True)

    def add_model_file_name(self, filename):
        """Use to set the file names for the reader. Handles single string or
        list of strings.
        """
        if filename is None:
            return # do nothing if None is passed by a constructor on accident
        elif isinstance(filename, (list, tuple)):
            for f in filename:
                self.add_model_file_name(f)
            self.Modified()
        elif filename not in self._model_filenames:
            self._model_filenames.append(filename)
            self.Modified()
        return 1

    def get_model_filenames(self, idx=None):
        """Returns the list of file names or given and index returns a specified
        timestep's filename.
        """
        if idx is None or not self.has_models():
            return self._model_filenames
        return self._model_filenames[idx]

    def set_use_filename(self, flag):
        """Set a flag on whether or not to use the filename as the data array name"""
        if self.__use_filename != flag:
            self.__use_filename = flag
            self.Modified(read_again=False)

    def set_data_name(self, name):
        """Set the data array name"""
        if name == '':
            self.__use_filename = True
            self.Modified(read_again=False)
        elif self.__data_name != name:
            self.__data_name = name
            self.__use_filename = False
            self.Modified(read_again=False)

    def get_data_name(self):
        """Get the data array name"""
        if self.__use_filename:
            mname = self.get_model_filenames(idx=0)
            return os.path.basename(mname)
        return self.__data_name
