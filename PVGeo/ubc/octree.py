__all__ = [
    # OcTree
    'OcTreeReader',
    'OcTreeAppender',
]

import numpy as np
from vtk.util import numpy_support as nps
import vtk
import os
import sys
if sys.version_info < (3,):
    from StringIO import StringIO
else:
    from io import StringIO

from ..base import AlgorithmBase
from .two_file_base import ubcMeshReaderBase, ModelAppenderBase
from .. import _helpers
from .. import interface



class OcTreeReader(ubcMeshReaderBase):
    """This class reads a UBC OcTree Mesh file and builds a ``vtkUnstructuredGrid`` of the data in the file.
    Model File is optional. Reader will still construct ``vtkUnstructuredGrid`` safely.
    """
    __displayname__ = 'UBC OcTree Mesh Reader'
    __category__ = 'reader'
    def __init__(self, nOutputPorts=1, outputType='vtkUnstructuredGrid', **kwargs):
        ubcMeshReaderBase.__init__(self,
            nOutputPorts=nOutputPorts, outputType=outputType,
            **kwargs)

        self.__mesh = vtk.vtkUnstructuredGrid()
        self.__models = []


    @staticmethod
    def ubcOcTreeMesh(FileName, pdo=None):
        """This method reads a UBC OcTree Mesh file and builds a ``vtkUnstructuredGrid`` of the data in the file. This method generates the ``vtkUnstructuredGrid`` without any data attributes.

        Args:
            FileName (str): The mesh filename as an absolute path for the input mesh file in UBC OcTree format.
            pdo (vtkUnstructuredGrid): A pointer to the output data object.

        Returns:
            vtkUnstructuredGrid: Returns a ``vtkUnstructuredGrid`` generated from the UBCMesh grid. Mesh is defined by the input mesh file. No data attributes here, simply an empty mesh. Use the ``PlaceModelOnOcTreeMesh()`` method to associate with model data.
        """
        if pdo is None:
            pdo = vtk.vtkUnstructuredGrid() # vtkUnstructuredGrid

        #--- Read in the mesh ---#
        fileLines = np.genfromtxt(FileName, dtype=str,
            delimiter='\n', comments='!')

        # Get mesh dimensions
        dim = np.array(fileLines[0].
            split('!')[0].split(), dtype=int)
        # First three values are the number of cells in the core mesh and remaining 6 values are padding for the core region.
        pad = dim[3:6] # TODO: check if there because optional... might throw error if not there
        dim = dim[0:3]
        ne,nn,nz = dim[0], dim[1], dim[2]

        # The origin corner (Southwest-top)
        #- Remember UBC format specifies down as the positive Z
        #- Easting, Northing, Altitude
        oo = np.array(
            fileLines[1].split('!')[0].split(),
            dtype=float
        )
        oe,on,oz = oo[0],oo[1],oo[2]

        # Widths of the core cells in the Easting, Northing, and Vertical directions.
        ww = np.array(
            fileLines[2].split('!')[0].split(),
            dtype=float
        )
        we,wn,wz = ww[0],ww[1],ww[2]

        # Number of cells in OcTree mesh
        numCells = np.array(
            fileLines[3].split('!')[0].split(),
            dtype=float
        )

        # Read the remainder of the file containing the index arrays
        indArr = np.loadtxt(
            StringIO("\n".join(fileLines[4::])), dtype=np.int)

        # Start processing the information
        # Make vectors of the base mesh node, starting in the wsb corner
        vec_full_nx = np.cumsum(np.hstack((oe, we * np.ones(ne))))
        vec_full_ny = np.cumsum(np.hstack((on, wn * np.ones(nn))))
        vec_full_nz = np.cumsum(np.hstack((oz - wz * nz, wz * np.ones(nz))))
        # Make indices
        indC = indArr[:, 0:3] + np.array([-1, -1, -1])  # Shift to be 0 indexed
        # Flip the z-ind to start from bottom
        indC[:, 2] = nz - indC[:, 2] - indArr[:, 3]
        cell_size = np.reshape(indArr[:, 3], (len(indArr[:, 3]), 1))
        cell_zero = np.zeros((len(cell_size), 1), dtype=np.int)
        # Need to reference the nodal numbers to form the cell.
        # Find the 8 corners of each cell
        #
        #             z+   y+
        #             |  /
        #             | /
        #             |/_ _ _ x+
        #
        #    N7--------N8
        #   /|         /|
        #  N5--------N6 |
        #  | |        | |
        #  | N3-------|N4
        #  |/         |/
        #  N1--------N2

        # UBC Octree indexes always the top-left-close corner first
        # For to define the cells in UBC order
        cell_n1 = indC + np.hstack((cell_zero, cell_zero, cell_zero))  # Node 1 in all cells
        cell_n2 = indC + np.hstack((cell_size, cell_zero, cell_zero))  # Node 2 in all cells
        cell_n3 = indC + np.hstack((cell_zero, cell_size, cell_zero))  # Node 3 in all cells
        cell_n4 = indC + np.hstack((cell_size, cell_size, cell_zero))  # Node 4 in all cells
        cell_n5 = indC + np.hstack((cell_zero, cell_zero, cell_size))  # Node 5 in all cells
        cell_n6 = indC + np.hstack((cell_size, cell_zero, cell_size))  # Node 6 in all cells
        cell_n7 = indC + np.hstack((cell_zero, cell_size, cell_size))  # Node 7 in all cells
        cell_n8 = indC + np.hstack((cell_size, cell_size, cell_size))  # Node 8 in all cells
        # Sort the nodal index to be from the south-west-bottom most corner,
        # comply with SimPEG ordering
        # NOTE: Is not needed but prefered
        ind_cell_corner = np.argsort(
            cell_n1.view(','.join(3 * ['int'])), axis=0, order=('f2', 'f1', 'f0'))
        sortcell_n1 = cell_n1[ind_cell_corner][:, 0, :]
        sortcell_n2 = cell_n2[ind_cell_corner][:, 0, :]
        sortcell_n3 = cell_n3[ind_cell_corner][:, 0, :]
        sortcell_n4 = cell_n4[ind_cell_corner][:, 0, :]
        sortcell_n5 = cell_n5[ind_cell_corner][:, 0, :]
        sortcell_n6 = cell_n6[ind_cell_corner][:, 0, :]
        sortcell_n7 = cell_n7[ind_cell_corner][:, 0, :]
        sortcell_n8 = cell_n8[ind_cell_corner][:, 0, :]
        # Find the unique nodes
        all_nodes = np.concatenate((
            sortcell_n1,
            sortcell_n2,
            sortcell_n3,
            sortcell_n4,
            sortcell_n5,
            sortcell_n6,
            sortcell_n7,
            sortcell_n8), axis=0)
        # Make a rec array to search for uniques
        all_nodes_rec = all_nodes.view(','.join(3 * ['int']))[:, 0]
        unique_nodes, ind_nodes_vec = np.unique(all_nodes_rec, return_inverse=True)

        # Reshape the matrix
        ind_nodes_mat = ind_nodes_vec.reshape(((8, int(ind_nodes_vec.size / 8)))).T
        ind_nodes_full = np.concatenate((
            np.ones((
                ind_nodes_mat.shape[0],
                1), dtype=np.int64) * ind_nodes_mat.shape[1],
            ind_nodes_mat), axis=1).ravel()

        # Make the VTK object
        # Make the points.
        ptsArr = np.concatenate((
            vec_full_nx[unique_nodes['f0']].reshape(-1, 1),
            vec_full_ny[unique_nodes['f1']].reshape(-1, 1),
            vec_full_nz[unique_nodes['f2']].reshape(-1, 1)), axis=1)
        vtkPtsData = interface.convertArray(ptsArr, deep=1)
        vtkPts = vtk.vtkPoints()
        vtkPts.SetData(vtkPtsData)

        # Make the cells
        # Cells -cell array
        CellArr = vtk.vtkCellArray()
        CellArr.SetNumberOfCells(numCells)
        CellArr.SetCells(
            numCells,
            nps.numpy_to_vtkIdTypeArray(
                np.ascontiguousarray(ind_nodes_full), deep=1))

        # Construct the VTK object declared in `pdo`
        # Set the objects properties
        pdo.SetPoints(vtkPts)
        pdo.SetCells(vtk.VTK_VOXEL, CellArr)

        # Add the indexing of the cell's
        vtkIndexArr = interface.convertArray(ind_cell_corner.ravel(), name='index_cell_corner', deep=1)
        pdo.GetCellData().AddArray(vtkIndexArr)

        return pdo

    @staticmethod
    def PlaceModelOnOcTreeMesh(mesh, model, dataNm='Data'):
        """Places model data onto a mesh. This is for the UBC Grid data reaers to associate model data with the mesh grid.

        Args:
            mesh (vtkUnstructuredGrid): The ``vtkUnstructuredGrid`` that is the mesh to place the model data upon. Needs to have been read in by ubcOcTree
            model (np.ndarray): A NumPy float array that holds all of the data to place inside of the mesh's cells.
            dataNm (str): The name of the model data array once placed on the ``vtkUnstructuredGrid``.

        Returns:
            vtkUnstructuredGrid: Returns the input ``vtkUnstructuredGrid`` with model data appended.
        """
        if type(model) is dict:
            for key in model.keys():
                mesh = OcTreeReader.PlaceModelOnOcTreeMesh(mesh, model[key], dataNm=key)
            return mesh
        # Make sure this model file fits the dimensions of the mesh
        numCells = mesh.GetNumberOfCells()
        if (numCells < len(model)):
            raise _helpers.PVGeoError('This model file has more data than the given mesh has cells to hold.')
        elif (numCells > len(model)):
            raise _helpers.PVGeoError('This model file does not have enough data to fill the given mesh\'s cells.')

        # This is absolutely crucial!
        # Do not play with unless you know what you are doing!
        ind_reorder = nps.vtk_to_numpy(
            mesh.GetCellData().GetArray('index_cell_corner'))

        model = model[ind_reorder]

        # Convert data to VTK data structure and append to output
        c = interface.convertArray(model, name=dataNm, deep=True)
        # THIS IS CELL DATA! Add the model data to CELL data:
        mesh.GetCellData().AddArray(c)
        return mesh



    def __ubcOcTree(self, FileName_Mesh, FileName_Models, output):
        """Wrapper to Read UBC GIF OcTree mesh and model file pairs. UBC OcTree models are defined using a 2-file format. The "mesh" file describes how the data is descritized. The "model" file lists the physical property values for all cells in a mesh. A model file is meaningless without an associated mesh file. This only handles OcTree formats

        Args:
            FileName_Mesh (str): The OcTree Mesh filename as an absolute path for the input mesh file in UBC OcTree Mesh Format
        FileName_Models (list(str)): The model filenames as absolute paths for the input model timesteps in UBC OcTree Model Format.
            output (vtkUnstructuredGrid): The output data object

        Returns:
            vtkUnstructuredGrid: Returns a ``vtkUnstructuredGrid`` generated from the UBC 2D/3D Mesh grid. Mesh is defined by the input mesh file. Cell data is defined by the input model file.
        """
        if self.NeedToReadMesh():
            # Construct/read the mesh
            OcTreeReader.ubcOcTreeMesh(FileName_Mesh, pdo=self.__mesh)
            self.NeedToReadMesh(flag=False)
        output.DeepCopy(self.__mesh)
        if self.NeedToReadModels() and self.ThisHasModels():
            # Read the model data
            self.__models = []
            for f in FileName_Models:
                # Read the model data
                self.__models.append(ubcMeshReaderBase.ubcModel3D(f))
            self.NeedToReadModels(flag=False)
        return output


    def RequestData(self, request, inInfo, outInfo):
        # Get output:
        output = self.GetOutputData(outInfo, 0)
        # Get requested time index
        i = _helpers.getRequestedTime(self, outInfo)
        self.__ubcOcTree(
            self.GetMeshFileName(),
            self.GetModelFileNames(),
            output)

        # Place the model data for given timestep onto the mesh
        if len(self.__models) > i:
            OcTreeReader.PlaceModelOnOcTreeMesh(output, self.__models[i], self.GetDataName())

        return 1


    def RequestInformation(self, request, inInfo, outInfo):
        """Pipeline method for handling requests about the grid extents and time
        step values
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
        """Use to clean/rebuild the mesh.
        """
        self.__mesh = vtk.vtkUnstructuredGrid()
        ubcMeshReaderBase.ClearModels(self)

    def ClearModels(self):
        """Use to clean the models and reread the data
        """
        self.__models = []
        ubcMeshReaderBase.ClearModels(self)





################################################################################

class OcTreeAppender(ModelAppenderBase):
    """This filter reads a timeseries of models and appends it to an input
    ``vtkUnstructuredGrid``
    """
    __displayname__ = 'UBC OcTree Mesh Appender'
    __category__ = 'filter'
    def __init__(self, **kwargs):
        ModelAppenderBase.__init__(self,
            inputType='vtkUnstructuredGrid',
            outputType='vtkUnstructuredGrid',
            **kwargs)


    def _ReadUpFront(self):
        reader = ubcMeshReaderBase.ubcModel3D
        self._models = []
        for f in self._modelFileNames:
            # Read the model data
            self._models.append(reader(f))
        self.NeedToRead(flag=False)
        return

    def _PlaceOnMesh(self, output, idx=0):
        OcTreeReader.PlaceModelOnOcTreeMesh(output, self._models[idx], self._dataname)
        return
