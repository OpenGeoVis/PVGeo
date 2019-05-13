__all__ = [
    'TensorMeshReader',
    'TensorMeshAppender',
    'TopoMeshAppender',
]

__displayname__ = 'Tensor Mesh'

import os
import sys

import numpy as np
import pandas as pd
import vtk

from .. import _helpers, interface
from ..base import AlgorithmBase
from .two_file_base import ModelAppenderBase, ubcMeshReaderBase

if sys.version_info < (3,):
    from StringIO import StringIO
else:
    from io import StringIO




class TensorMeshReader(ubcMeshReaderBase):
    """UBC Mesh 2D/3D models are defined using a 2-file format. The "mesh" file
    describes how the data is discretized. The "model" file lists the physical
    property values for all cells in a mesh. A model file is meaningless without
    an associated mesh file. The reader will automatically detect if the mesh is
    2D or 3D and read the remainder of the data with that dimensionality
    assumption. If the mesh file is 2D, then then model file must also be in the
    2D format (same for 3D).

    Note:
        Model File is optional. Reader will still construct
        ``vtkRectilinearGrid`` safely.
    """
    __displayname__ = 'UBC Tensor Mesh Reader'
    __category__ = 'reader'
    description = 'PVGeo: UBC Mesh 2D/3D Two-File Format'
    def __init__(self, nOutputPorts=1, outputType='vtkRectilinearGrid', **kwargs):
        ubcMeshReaderBase.__init__(self,
            nOutputPorts=nOutputPorts, outputType=outputType, **kwargs)

        self.__mesh = vtk.vtkRectilinearGrid()
        self.__models = []


    @staticmethod
    def place_model_on_mesh(mesh, model, data_name='Data'):
        """Places model data onto a mesh. This is for the UBC Grid data reaers
        to associate model data with the mesh grid.

        Args:
            mesh (vtkRectilinearGrid): The ``vtkRectilinearGrid`` that is the
                mesh to place the model data upon.
            model (np.array): A NumPy float array that holds all of the data to
                place inside of the mesh's cells.
            data_name (str) : The name of the model data array once placed on the
                ``vtkRectilinearGrid``.

        Return:
            vtkRectilinearGrid :
                Returns the input ``vtkRectilinearGrid`` with model data appended.
        """
        if isinstance(model, dict):
            for key in model.keys():
                TensorMeshReader.place_model_on_mesh(mesh, model[key], data_name=key)
            return mesh

        # model.GetNumberOfValues() if model is vtkDataArray
        # Make sure this model file fits the dimensions of the mesh
        ext = mesh.GetExtent()
        n1,n2,n3 = ext[1],ext[3],ext[5]
        if (n1*n2*n3 < len(model)):
            raise _helpers.PVGeoError('Model `%s` has more data than the given mesh has cells to hold.' % data_name)
        elif (n1*n2*n3 > len(model)):
            raise _helpers.PVGeoError('Model `%s` does not have enough data to fill the given mesh\'s cells.' % data_name)

        # Swap axes because VTK structures the coordinates a bit differently
        #-  This is absolutely crucial!
        #-  Do not play with unless you know what you are doing!
        if model.ndim > 1 and model.ndim < 3:
            ncomp = model.shape[1]
            model = np.reshape(model, (n1, n2, n3, ncomp))
            model = np.swapaxes(model,0,1)
            model = np.swapaxes(model,0,2)
            # Now reverse Z axis
            model = model[::-1,:,:,:] # Note it is in Fortran ordering
            model = np.reshape(model, (n1*n2*n3, ncomp))
        else:
            model = np.reshape(model, (n1,n2,n3))
            model = np.swapaxes(model,0,1)
            model = np.swapaxes(model,0,2)
            # Now reverse Z axis
            model = model[::-1,:,:] # Note it is in Fortran ordering
            model = model.flatten()

        # Convert data to VTK data structure and append to output
        c = interface.convert_array(model, name=data_name, deep=True)
        # THIS IS CELL DATA! Add the model data to CELL data:
        mesh.GetCellData().AddArray(c)
        return mesh

    #------------------------------------------------------------------#
    #----------------------     UBC MESH 2D    ------------------------#
    #------------------------------------------------------------------#

    @staticmethod
    def ubc_mesh_2d(FileName, output):
        """This method reads a UBC 2D Mesh file and builds an empty
        ``vtkRectilinearGrid`` for data to be inserted into. `Format Specs`_.

        .. _Format Specs: http://giftoolscookbook.readthedocs.io/en/latest/content/fileFormats/mesh2Dfile.html

        Args:
            FileName (str) : The mesh filename as an absolute path for the input
                mesh file in UBC 3D Mesh Format.
            output (vtkRectilinearGrid) : The output data object

        Return:
            vtkRectilinearGrid :
                a ``vtkRectilinearGrid`` generated from the UBC 3D Mesh grid.
                Mesh is defined by the input mesh file.
                No data attributes here, simply an empty mesh. Use the
                ``place_model_on_mesh()`` method to associate with model data.
        """
        # Read in data from file
        xpts, xdisc, zpts, zdisc = ubcMeshReaderBase._ubc_mesh_2d_part(FileName)

        nx = np.sum(np.array(xdisc,dtype=int))+1
        nz = np.sum(np.array(zdisc,dtype=int))+1

        # Now generate the vtkRectilinear Grid
        def _genCoords(pts, disc, z=False):
            c = [float(pts[0])]
            for i in range(len(pts)-1):
                start = float(pts[i])
                stop = float(pts[i+1])
                num = int(disc[i])
                w = (stop-start)/num

                for j in range(1,num):
                    c.append(start + (j)*w)
                c.append(stop)
            c = np.array(c,dtype=float)
            if z:
                c = -c[::-1]
            return interface.convert_array(c,deep=True)

        xcoords = _genCoords(xpts, xdisc)
        zcoords = _genCoords(zpts, zdisc, z=True)
        ycoords = interface.convert_array(np.zeros(1),deep=True)

        output.SetDimensions(nx,2,nz) # note this subtracts 1
        output.SetXCoordinates(xcoords)
        output.SetYCoordinates(ycoords)
        output.SetZCoordinates(zcoords)

        return output

    @staticmethod
    def ubc_model_2d(FileName):
        """Reads a 2D model file and returns a 1D NumPy float array. Use the
        ``place_model_on_mesh()`` method to associate with a grid.

        Note:
            Only supports single component data

        Args:
            FileName (str) : The model filename as an absolute path for the
                input model file in UBCMesh Model Format. Also accepts a list of
                string file names.

        Return:
            np.array :
                a NumPy float array that holds the model data read from
                the file. Use the ``place_model_on_mesh()`` method to associate
                with a grid. If a list of file names is given then it will
                return a dictionary of NumPy float array with keys as the
                basenames of the files.
        """
        if isinstance(FileName, (list, tuple)):
            out = {}
            for f in FileName:
                out[os.path.basename(f)] = TensorMeshReader.ubc_model_2d(f)
            return out

        dim = np.genfromtxt(FileName, dtype=int, delimiter=None, comments='!', max_rows=1)
        names = ['col%d' % i for i in range(dim[0])]
        df = pd.read_csv(FileName, names=names, delim_whitespace=True, skiprows=1, comment='!')
        data = df.values
        if np.shape(data)[0] != dim[1] and np.shape(data)[1] != dim[0]:
            raise _helpers.PVGeoError('Mode file `%s` improperly formatted.' % FileName)
        return data.flatten(order='F')


    def __ubc_mesh_data_2d(self, filename_mesh, filename_models, output):
        """Helper method to read a 2D mesh
        """
        # Construct/read the mesh
        if self.need_to_readMesh():
            TensorMeshReader.ubc_mesh_2d(filename_mesh, self.__mesh)
            self.need_to_readMesh(flag=False)
        output.DeepCopy(self.__mesh)
        if self.need_to_readModels() and self.this_has_models():
            self.__models = []
            for f in filename_models:
                # Read the model data
                self.__models.append(TensorMeshReader.ubc_model_2d(f))
            self.need_to_readModels(flag=False)
        return output


    #------------------------------------------------------------------#
    #----------------------     UBC MESH 3D    ------------------------#
    #------------------------------------------------------------------#

    @staticmethod
    def ubc_mesh_3d(FileName, output):
        """This method reads a UBC 3D Mesh file and builds an empty
        ``vtkRectilinearGrid`` for data to be inserted into.

        Args:
            FileName (str) : The mesh filename as an absolute path for the input
                mesh file in UBC 3D Mesh Format.
            output (vtkRectilinearGrid) : The output data object

        Return:
            vtkRectilinearGrid :
                a ``vtkRectilinearGrid`` generated from the UBC 3D Mesh grid.
                Mesh is defined by the input mesh file.
                No data attributes here, simply an empty mesh. Use the
                ``place_model_on_mesh()`` method to associate with model data.
        """

        #--- Read in the mesh ---#
        fileLines = np.genfromtxt(FileName, dtype=str,
            delimiter='\n', comments='!')

        # Get mesh dimensions
        dim = np.array(fileLines[0].split('!')[0].split(), dtype=int)
        dim = (dim[0]+1, dim[1]+1, dim[2]+1)

        # The origin corner (Southwest-top)
        #- Remember UBC format specifies down as the positive Z
        #- Easting, Northing, Altitude
        oo = np.array(
            fileLines[1].split('!')[0].split(),
            dtype=float
        )
        ox,oy,oz = oo[0],oo[1],oo[2]

        # Read cell sizes for each line in the UBC mesh files
        def _readCellLine(line):
            line_list = []
            for seg in line.split():
                if '*' in seg:
                    sp = seg.split('*')
                    seg_arr = np.ones((int(sp[0]),), dtype=float) * float(sp[1])
                else:
                    seg_arr = np.array([float(seg)], dtype=float)
                line_list.append(seg_arr)
            return np.concatenate(line_list)

        # Read the cell sizes
        cx = _readCellLine(fileLines[2].split('!')[0])
        cy = _readCellLine(fileLines[3].split('!')[0])
        cz = _readCellLine(fileLines[4].split('!')[0])
        # Invert the indexing of the vector to start from the bottom.
        cz = cz[::-1]
        # Adjust the reference point to the bottom south west corner
        oz = oz - np.sum(cz)

        # Now generate the coordinates for from cell width and origin
        cox = ox + np.cumsum(cx)
        cox = np.insert(cox,0,ox)
        coy = oy + np.cumsum(cy)
        coy = np.insert(coy,0,oy)
        coz = oz + np.cumsum(cz)
        coz = np.insert(coz,0,oz)

        # Set the dims and coordinates for the output
        output.SetDimensions(dim[0],dim[1],dim[2])
        # Convert to VTK array for setting coordinates
        output.SetXCoordinates(interface.convert_array(cox,deep=True))
        output.SetYCoordinates(interface.convert_array(coy,deep=True))
        output.SetZCoordinates(interface.convert_array(coz,deep=True))

        return output


    def __ubc_mesh_data_3d(self, filename_mesh, filename_models, output):
        """Helper method to read a 3D mesh"""
        # Construct/read the mesh
        if self.need_to_readMesh():
            TensorMeshReader.ubc_mesh_3d(filename_mesh, self.__mesh)
            self.need_to_readMesh(flag=False)
        output.DeepCopy(self.__mesh)
        if self.need_to_readModels() and self.this_has_models():
            self.__models = []
            for f in filename_models:
                # Read the model data
                self.__models.append(TensorMeshReader.ubc_model_3d(f))
            self.need_to_readModels(flag=False)
        return output


    def __ubc_tensor_mesh(self, filename_mesh, filename_models, output):
        """Wrapper to Read UBC GIF 2D and 3D meshes. UBC Mesh 2D/3D models are
        defined using a 2-file format. The "mesh" file describes how the data is
        descritized. The "model" file lists the physical property values for all
        cells in a mesh. A model file is meaningless without an associated mesh
        file. If the mesh file is 2D, then then model file must also be in the
        2D format (same for 3D).

        Args:
            filename_mesh (str) : The mesh filename as an absolute path for the
                input mesh file in UBC 2D/3D Mesh Format
            filename_models (str or list(str)) : The model filename(s) as an
                absolute path for the input model file in UBC 2D/3D Model Format.
            output (vtkRectilinearGrid) : The output data object

        Return:
            vtkRectilinearGrid :
                a ``vtkRectilinearGrid`` generated from the UBC 2D/3D Mesh grid.
                Mesh is defined by the input mesh file.
                Cell data is defined by the input model file.

        """
        # Check if the mesh is a UBC 2D mesh
        if self.is_2d():
            self.__ubc_mesh_data_2d(filename_mesh, filename_models, output)
        # Check if the mesh is a UBC 3D mesh
        elif self.is_3d():
            self.__ubc_mesh_data_3d(filename_mesh, filename_models, output)
        else:
            raise _helpers.PVGeoError('File format not recognized')
        return output

    def RequestData(self, request, inInfo, outInfo):
        """Handles data request by the pipeline.
        """
        # Get output:
        output = self.GetOutputData(outInfo, 0)
        # Get requested time index
        i = _helpers.get_requested_time(self, outInfo)
        self.__ubc_tensor_mesh(
            self.get_mesh_filename(),
            self.get_model_filenames(),
            output)
        # Place the model data for given timestep onto the mesh
        if len(self.__models) > i:
            TensorMeshReader.place_model_on_mesh(output, self.__models[i], self.get_data_name())
        return 1


    def RequestInformation(self, request, inInfo, outInfo):
        """Handles info request by pipeline about timesteps and grid extents.
        """
        # Call parent to handle time stuff
        ubcMeshReaderBase.RequestInformation(self, request, inInfo, outInfo)
        # Now set whole output extent
        if self.need_to_readMesh():
            ext = self._read_extent()
            info = outInfo.GetInformationObject(0)
            # Set WHOLE_EXTENT: This is absolutely necessary
            info.Set(vtk.vtkStreamingDemandDrivenPipeline.WHOLE_EXTENT(), ext, 6)
        return 1

    def clear_mesh(self):
        """Use to clean/rebuild the mesh
        """
        self.__mesh = vtk.vtkRectilinearGrid()
        ubcMeshReaderBase.clear_models(self)

    def clear_models(self):
        """Use to clean the models and reread
        """
        self.__models = []
        ubcMeshReaderBase.clear_models(self)

################################################################################

class TensorMeshAppender(ModelAppenderBase):
    """This filter reads a timeseries of models and appends it to an input
    ``vtkRectilinearGrid``
    """
    __displayname__ = 'UBC Tensor Mesh Appender'
    __category__ = 'filter'
    def __init__(self, **kwargs):
        ModelAppenderBase.__init__(self,
            inputType='vtkRectilinearGrid',
            outputType='vtkRectilinearGrid',
            **kwargs)


    def _read_up_front(self):
        """Internal helepr to read data at start"""
        reader = ubcMeshReaderBase.ubc_model_3d
        if not self._is_3D:
            # Note how in UBC format, 2D grids are specified on an XZ plane (no Y component)
            # This will only work prior to rotations to account for real spatial reference
            reader = TensorMeshReader.ubc_model_2d
        self._models = []
        for f in self._model_filenames:
            # Read the model data
            self._models.append(reader(f))
        self.need_to_read(flag=False)
        return

    def _place_on_mesh(self, output, idx=0):
        """Internal helepr to place a model on the mesh for a given index"""
        TensorMeshReader.place_model_on_mesh(output, self._models[idx], self.get_data_name())
        return


################################################################################

class TopoMeshAppender(AlgorithmBase):
    """This filter reads a single discrete topography file and appends it as a
    boolean data array.
    """
    __displayname__ = 'Append UBC Discrete Topography'
    __category__ = 'filter'
    def __init__(self, inputType='vtkRectilinearGrid',
                       outputType='vtkRectilinearGrid', **kwargs):
        AlgorithmBase.__init__(self,
            nInputPorts=1, inputType=inputType,
            nOutputPorts=1, outputType=outputType)
        self._topoFileName = kwargs.get('filename', None)
        self.__indices = None
        self.__need_to_read = True
        self.__ne, self.__nn = None, None

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
        return self.__need_to_read

    def Modified(self, read_again=True):
        """Call modified if the files needs to be read again again.
        """
        if read_again: self.__need_to_read = read_again
        AlgorithmBase.Modified(self)

    def modified(self, read_again=True):
        """Call modified if the files needs to be read again again.
        """
        return self.Modified(read_again=read_again)


    def _read_up_front(self):
        """Internal helepr to read data at start"""
        # Read the file
        content = np.genfromtxt(self._topoFileName, dtype=str, delimiter='\n',
                                comments='!')
        dim = content[0].split()
        self.__ne, self.__nn = int(dim[0]), int(dim[1])
        self.__indices = pd.read_csv(StringIO("\n".join(content[1::])),
                            names=['i', 'j', 'k'], delim_whitespace=True)
        # NOTE: K indices are inverted
        self.need_to_read(flag=False)
        return

    def _place_on_mesh(self, output):
        """Internal helepr to place an active cells model on the mesh"""
        # Check mesh extents to math topography
        nx, ny, nz = output.GetDimensions()
        nx, ny, nz = nx-1, ny-1, nz-1 # because GetDimensions counts the nodes
        topz = np.max(self.__indices['k']) + 1
        if nx != self.__nn or ny != self.__ne or topz > nz:
            raise _helpers.PVGeoError('Dimension mismatch between input grid and topo file.')
        # # Adjust the k indices to be in caarteian system
        # self.__indices['k'] = nz - self.__indices['k']
        # Fill out the topo and add it as model as it will be in UBC format
        # Create a 3D array of 1s and zeros (1 means beneath topo or active)
        topo = np.empty((ny, nx, nz), dtype=float)
        topo[:] = np.nan
        for row in self.__indices.values:
            i, j, k = row
            topo[i, j, k+1:] = 0
            topo[i, j, :k+1] = 1
        # Add as model... ``place_model_on_mesh`` handles the rest
        TensorMeshReader.place_model_on_mesh(output, topo.flatten(), 'Active Topography')
        return


    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output
        """
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        output = self.GetOutputData(outInfo, 0)
        output.DeepCopy(pdi) # ShallowCopy if you want changes to propagate upstream
        # Perfrom task:
        if self.__need_to_read:
            self._read_up_front()
        # Place the model data for given timestep onto the mesh
        self._place_on_mesh(output)
        return 1


    #### Setters and Getters ####

    def clear_topo_file(self):
        """Use to clear data file name.
        """
        self._topoFileName = None
        self.Modified(read_again=True)

    def set_topo_filename(self, filename):
        """Use to set the file names for the reader. Handles single strings only
        """
        if filename is None:
            return # do nothing if None is passed by a constructor on accident
        elif isinstance(filename, str) and self._topoFileName != filename:
            self._topoFileName = filename
            self.Modified()
        return 1


################################################################################

#
# import numpy as np
# indices = np.array([[0,0,1],
#                     [0,1,1],
#                     [0,2,1],
#                     [1,0,1],
#                     [1,1,1],
#                     [1,2,1],
#                     [2,0,1],
#                     [2,1,1],
#                     [2,2,1],
#                     ])
#
# topo = np.empty((3,3,3), dtype=float)
# topo[:] = np.nan
#
# for row in indices:
#     i, j, k = row
#     topo[i, j, k:] = 0
#     topo[i, j, :k] = 1
# topo
