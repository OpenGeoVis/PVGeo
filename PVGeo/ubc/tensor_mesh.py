__all__ = [
    'TensorMeshReader',
    'TensorMeshAppender',
]

import numpy as np
import vtk
import os
import pandas as pd
import sys
if sys.version_info < (3,):
    from StringIO import StringIO
else:
    from io import StringIO

from ..base import AlgorithmBase
from .two_file_base import ubcMeshReaderBase, ModelAppenderBase
from .. import _helpers
from .. import interface



class TensorMeshReader(ubcMeshReaderBase):
    """UBC Mesh 2D/3D models are defined using a 2-file format. The "mesh" file
    describes how the data is discretized. The "model" file lists the physical
    property values for all cells in a mesh. A model file is meaningless without
    an associated mesh file. The reader will automatically detect if the mesh is
    2D or 3D and read the remainder of the data with that dimensionality
    assumption. If the mesh file is 2D, then then model file must also be in the
    2D format (same for 3D).

    Note:
        Model File is optional. Reader will still construct ``vtkRectilinearGrid`` safely.
    """
    __displayname__ = 'UBC Tensor Mesh Reader'
    __category__ = 'reader'
    def __init__(self, nOutputPorts=1, outputType='vtkRectilinearGrid', **kwargs):
        ubcMeshReaderBase.__init__(self,
            nOutputPorts=nOutputPorts, outputType=outputType, **kwargs)

        self.__mesh = vtk.vtkRectilinearGrid()
        self.__models = []


    @staticmethod
    def PlaceModelOnMesh(mesh, model, dataNm='Data'):
        """Places model data onto a mesh. This is for the UBC Grid data reaers
        to associate model data with the mesh grid.

        Args:
            mesh (vtkRectilinearGrid): The ``vtkRectilinearGrid`` that is the mesh to place the model data upon.
            model (np.array): A NumPy float array that holds all of the data to place inside of the mesh's cells.
            dataNm (str) : The name of the model data array once placed on the ``vtkRectilinearGrid``.

        Return:
            vtkRectilinearGrid : Returns the input ``vtkRectilinearGrid`` with model data appended.
        """
        if type(model) is dict:
            for key in model.keys():
                TensorMeshReader.PlaceModelOnMesh(mesh, model[key], dataNm=key)
            return mesh

        # model.GetNumberOfValues() if model is vtkDataArray
        # Make sure this model file fits the dimensions of the mesh
        ext = mesh.GetExtent()
        n1,n2,n3 = ext[1],ext[3],ext[5]
        if (n1*n2*n3 < len(model)):
            raise _helpers.PVGeoError('Model `%s` has more data than the given mesh has cells to hold.' % dataNm)
        elif (n1*n2*n3 > len(model)):
            raise _helpers.PVGeoError('Model `%s` does not have enough data to fill the given mesh\'s cells.' % dataNm)

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
        c = interface.convertArray(model, name=dataNm, deep=True)
        # THIS IS CELL DATA! Add the model data to CELL data:
        mesh.GetCellData().AddArray(c)
        return mesh

    #------------------------------------------------------------------#
    #----------------------     UBC MESH 2D    ------------------------#
    #------------------------------------------------------------------#

    @staticmethod
    def ubcMesh2D(FileName, output):
        """This method reads a UBC 2D Mesh file and builds an empty ``vtkRectilinearGrid``
        for data to be inserted into. `Format Specs`_.

        .. _Format Specs: http://giftoolscookbook.readthedocs.io/en/latest/content/fileFormats/mesh2Dfile.html

        Args:
            FileName (str) : The mesh filename as an absolute path for the input mesh file in UBC 3D Mesh Format.
            output (vtkRectilinearGrid) : The output data object

        Return:
            vtkRectilinearGrid : a ``vtkRectilinearGrid`` generated from the UBC 3D Mesh grid. Mesh is defined by the input mesh file. No data attributes here, simply an empty mesh. Use the ``PlaceModelOnMesh()`` method to associate with model data.
        """
        # Read in data from file
        xpts, xdisc, zpts, zdisc = ubcMeshReaderBase._ubcMesh2D_part(FileName)

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
            return interface.convertArray(c,deep=True)

        xcoords = _genCoords(xpts, xdisc)
        zcoords = _genCoords(zpts, zdisc, z=True)
        ycoords = interface.convertArray(np.zeros(1),deep=True)

        output.SetDimensions(nx,2,nz) # note this subtracts 1
        output.SetXCoordinates(xcoords)
        output.SetYCoordinates(ycoords)
        output.SetZCoordinates(zcoords)

        return output

    @staticmethod
    def ubcModel2D(FileName):
        """Reads a 2D model file and returns a 1D NumPy float array. Use the ``PlaceModelOnMesh()`` method to associate with a grid.

        Args:
            FileName (str) : The model filename as an absolute path for the input model file in UBCMesh Model Format. Also accepts a list of string file names.

        Return:
            np.array : a NumPy float array that holds the model data read from the file. Use the ``PlaceModelOnMesh()`` method to associate with a grid. If a list of file names is given then it will return a dictionary of NumPy float array with keys as the basenames of the files.

        Note:
            Only supports single component data
        """
        if type(FileName) is list:
            out = {}
            for f in FileName:
                out[os.path.basename(f)] = TensorMeshReader.ubcModel2D(f)
            return out

        dim = np.genfromtxt(FileName, dtype=int, delimiter=None, comments='!', max_rows=1)
        names = ['col%d' % i for i in range(dim[0])]
        df = pd.read_csv(FileName, names=names, delim_whitespace=True, skiprows=1, comment='!')
        data = df.values
        if np.shape(data)[0] != dim[1] and np.shape(data)[1] != dim[0]:
            raise _helpers.PVGeoError('Mode file `%s` improperly formatted.' % FileName)
        return data.flatten(order='F')


    def __ubcMeshData2D(self, FileName_Mesh, FileName_Models, output):
        """Helper method to read a 2D mesh
        """
        # Construct/read the mesh
        if self.NeedToReadMesh():
            TensorMeshReader.ubcMesh2D(FileName_Mesh, self.__mesh)
            self.NeedToReadMesh(flag=False)
        output.DeepCopy(self.__mesh)
        if self.NeedToReadModels() and self.ThisHasModels():
            self.__models = []
            for f in FileName_Models:
                # Read the model data
                self.__models.append(TensorMeshReader.ubcModel2D(f))
            self.NeedToReadModels(flag=False)
        return output


    #------------------------------------------------------------------#
    #----------------------     UBC MESH 3D    ------------------------#
    #------------------------------------------------------------------#

    @staticmethod
    def ubcMesh3D(FileName, output):
        """This method reads a UBC 3D Mesh file and builds an empty
        ``vtkRectilinearGrid`` for data to be inserted into.

        Args:
            FileName (str) : The mesh filename as an absolute path for the input mesh file in UBC 3D Mesh Format.
            output (vtkRectilinearGrid) : The output data object

        Return:
            vtkRectilinearGrid : a ``vtkRectilinearGrid`` generated from the UBC 3D Mesh grid. Mesh is defined by the input mesh file. No data attributes here, simply an empty mesh. Use the ``PlaceModelOnMesh()`` method to associate with model data.
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
        output.SetXCoordinates(interface.convertArray(cox,deep=True))
        output.SetYCoordinates(interface.convertArray(coy,deep=True))
        output.SetZCoordinates(interface.convertArray(coz,deep=True))

        return output


    def __ubcMeshData3D(self, FileName_Mesh, FileName_Models, output):
        """Helper method to read a 3D mesh"""
        # Construct/read the mesh
        if self.NeedToReadMesh():
            TensorMeshReader.ubcMesh3D(FileName_Mesh, self.__mesh)
            self.NeedToReadMesh(flag=False)
        output.DeepCopy(self.__mesh)
        if self.NeedToReadModels() and self.ThisHasModels():
            self.__models = []
            for f in FileName_Models:
                # Read the model data
                self.__models.append(TensorMeshReader.ubcModel3D(f))
            self.NeedToReadModels(flag=False)
        return output


    def __ubcTensorMesh(self, FileName_Mesh, FileName_Models, output):
        """Wrapper to Read UBC GIF 2D and 3D meshes. UBC Mesh 2D/3D models are defined using a 2-file format. The "mesh" file describes how the data is descritized. The "model" file lists the physical property values for all cells in a mesh. A model file is meaningless without an associated mesh file. If the mesh file is 2D, then then model file must also be in the 2D format (same for 3D).

        Args:
            FileName_Mesh (str) : The mesh filename as an absolute path for the input mesh file in UBC 2D/3D Mesh Format
            FileName_Models (str or list(str)) : The model filename(s) as an absolute path for the input model file in UBC 2D/3D Model Format.
            output (vtkRectilinearGrid) : The output data object

        Return:
            vtkRectilinearGrid : Returns a ``vtkRectilinearGrid`` generated from the UBC 2D/3D Mesh grid. Mesh is defined by the input mesh file. Cell data is defined by the input model file.

        """
        # Check if the mesh is a UBC 2D mesh
        if self.Is2D():
            self.__ubcMeshData2D(FileName_Mesh, FileName_Models, output)
        # Check if the mesh is a UBC 3D mesh
        elif self.Is3D():
            self.__ubcMeshData3D(FileName_Mesh, FileName_Models, output)
        else:
            raise _helpers.PVGeoError('File format not recognized')
        return output

    def RequestData(self, request, inInfo, outInfo):
        """Handles data request by the pipeline.
        """
        # Get output:
        output = self.GetOutputData(outInfo, 0)
        # Get requested time index
        i = _helpers.getRequestedTime(self, outInfo)
        self.__ubcTensorMesh(
            self.GetMeshFileName(),
            self.GetModelFileNames(),
            output)
        # Place the model data for given timestep onto the mesh
        if len(self.__models) > i:
            TensorMeshReader.PlaceModelOnMesh(output, self.__models[i], self.GetDataName())
        return 1


    def RequestInformation(self, request, inInfo, outInfo):
        """Handles info request by pipeline about timesteps and grid extents.
        """
        # Call parent to handle time stuff
        ubcMeshReaderBase.RequestInformation(self, request, inInfo, outInfo)
        # Now set whole output extent
        if self.NeedToReadMesh():
            ext = self._ReadExtent()
            info = outInfo.GetInformationObject(0)
            # Set WHOLE_EXTENT: This is absolutely necessary
            info.Set(vtk.vtkStreamingDemandDrivenPipeline.WHOLE_EXTENT(), ext, 6)
        return 1

    def ClearMesh(self):
        """Use to clean/rebuild the mesh
        """
        self.__mesh = vtk.vtkRectilinearGrid()
        ubcMeshReaderBase.ClearModels(self)

    def ClearModels(self):
        """Use to clean the models and reread
        """
        self.__models = []
        ubcMeshReaderBase.ClearModels(self)

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


    def _ReadUpFront(self):
        reader = ubcMeshReaderBase.ubcModel3D
        if not self._is3D:
            # Note how in UBC format, 2D grids are specified on an XZ plane (no Y component)
            # This will only work prior to rotations to account for real spatial reference
            reader = TensorMeshReader.ubcModel2D
        self._models = []
        for f in self._modelFileNames:
            # Read the model data
            self._models.append(reader(f))
        self.NeedToRead(flag=False)
        return

    def _PlaceOnMesh(self, output, idx=0):
        TensorMeshReader.PlaceModelOnMesh(output, self._models[idx], self._dataname)
        return
