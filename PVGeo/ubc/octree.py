__all__ = [
    # OcTree
    'OcTreeReader',
    'OcTreeAppender',
]

__displayname__ = 'OcTree Mesh'

import os

import numpy as np
import vtk
from vtk.util import numpy_support as nps

from .. import _helpers, interface
from ..base import AlgorithmBase
from .two_file_base import ModelAppenderBase, ubcMeshReaderBase


with _helpers.HiddenPrints():
    import discretize



class OcTreeReader(ubcMeshReaderBase):
    """This class reads a UBC OcTree Mesh file and builds a
    ``vtkUnstructuredGrid`` of the data in the file. Model File is optional.
    Reader will still construct ``vtkUnstructuredGrid`` safely.
    """
    __displayname__ = 'UBC OcTree Mesh Reader'
    __category__ = 'reader'
    description = 'PVGeo: UBC OcTree Mesh'
    def __init__(self, nOutputPorts=1, outputType='vtkUnstructuredGrid', **kwargs):
        ubcMeshReaderBase.__init__(self,
            nOutputPorts=nOutputPorts, outputType=outputType,
            **kwargs)

        self.__mesh = None
        self.__models = []


    def ubc_octree_mesh(self, FileName, pdo=None):
        """This method reads a UBC OcTree Mesh file and builds a
        ``vtkUnstructuredGrid`` of the data in the file. This method generates
        the ``vtkUnstructuredGrid`` without any data attributes.

        Args:
            FileName (str): The mesh filename as an absolute path for the input
                mesh file in UBC OcTree format.
            pdo (vtkUnstructuredGrid): A pointer to the output data object.

        Return:
            vtkUnstructuredGrid:
                a ``vtkUnstructuredGrid`` generated from the UBCMesh grid.
                Mesh is defined by the input mesh file.
                No data attributes here, simply an empty mesh. Use the
                ``place_model_on_octree_mesh()`` method to associate with model data.
        """
        try:
            self.__mesh = discretize.TreeMesh.readUBC(FileName)
        except (IOError, OSError) as fe:
            raise _helpers.PVGeoError(str(fe))
        if pdo is None:
            pdo = self.__mesh.toVTK()
        else:
            pdo.DeepCopy(self.__mesh.toVTK())
        return pdo

    @staticmethod
    def place_model_on_octree_mesh(mesh, model, data_name='Data'):
        """Places model data onto a mesh. This is for the UBC Grid data reaers
        to associate model data with the mesh grid.

        Args:
            mesh (vtkUnstructuredGrid): The ``vtkUnstructuredGrid`` that is the
                mesh to place the model data upon. Needs to have been read in by ubcOcTree
            model (np.ndarray): A NumPy float array that holds all of the data
                to place inside of the mesh's cells.
            data_name (str): The name of the model data array once placed on the
                ``vtkUnstructuredGrid``.

        Return:
            vtkUnstructuredGrid:
                The input ``vtkUnstructuredGrid`` with model data appended.
        """
        if isinstance(model, dict):
            for key in model.keys():
                mesh = OcTreeReader.place_model_on_octree_mesh(mesh, model[key], data_name=key)
            return mesh
        # Make sure this model file fits the dimensions of the mesh
        numCells = mesh.GetNumberOfCells()
        if (numCells < len(model)):
            raise _helpers.PVGeoError('This model file has more data than the given mesh has cells to hold.')
        elif (numCells > len(model)):
            raise _helpers.PVGeoError('This model file does not have enough data to fill the given mesh\'s cells.')

        # This is absolutely crucial!
        # Do not play with unless you know what you are doing!
        # Also note that this assumes ``discretize`` handles addin this array
        ind_reorder = nps.vtk_to_numpy(
            mesh.GetCellData().GetArray('index_cell_corner'))

        model = model[ind_reorder]

        # Convert data to VTK data structure and append to output
        c = interface.convert_array(model, name=data_name, deep=True)
        # THIS IS CELL DATA! Add the model data to CELL data:
        mesh.GetCellData().AddArray(c)
        return mesh



    def __ubc_octree(self, filename_mesh, filename_models, output):
        """Wrapper to Read UBC GIF OcTree mesh and model file pairs. UBC OcTree
        models are defined using a 2-file format. The "mesh" file describes how
        the data is descritized. The "model" file lists the physical property
        values for all cells in a mesh. A model file is meaningless without an
        associated mesh file. This only handles OcTree formats

        Args:
            filename_mesh (str): The OcTree Mesh filename as an absolute path
                for the input mesh file in UBC OcTree Mesh Format
        filename_models (list(str)): The model filenames as absolute paths for
            the input model timesteps in UBC OcTree Model Format.
            output (vtkUnstructuredGrid): The output data object

        Return:
            vtkUnstructuredGrid:
                A ``vtkUnstructuredGrid`` generated from the UBC 2D/3D Mesh grid.
                Mesh is defined by the input mesh file. Cell data is defined by
                the input model file.
        """
        if self.need_to_readMesh():
            # Construct/read the mesh
            self.ubc_octree_mesh(filename_mesh, pdo=output)
            self.need_to_readMesh(flag=False)
        output.DeepCopy(self.__mesh.toVTK())
        if self.need_to_readModels() and self.this_has_models():
            # Read the model data
            self.__models = []
            for f in filename_models:
                # Read the model data
                self.__models.append(ubcMeshReaderBase.ubc_model_3d(f))
            self.need_to_readModels(flag=False)
        return output


    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output"""
        # Get output:
        output = self.GetOutputData(outInfo, 0)
        # Get requested time index
        i = _helpers.get_requested_time(self, outInfo)
        self.__ubc_octree(
            self.get_mesh_filename(),
            self.get_model_filenames(),
            output)

        # Place the model data for given timestep onto the mesh
        if len(self.__models) > i:
            self.place_model_on_octree_mesh(output, self.__models[i], self.get_data_name())

        return 1


    def RequestInformation(self, request, inInfo, outInfo):
        """Pipeline method for handling requests about the grid extents and time
        step values
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
        """Use to clean/rebuild the mesh.
        """
        self.__mesh = vtk.vtkUnstructuredGrid()
        ubcMeshReaderBase.clear_models(self)

    def clear_models(self):
        """Use to clean the models and reread the data
        """
        self.__models = []
        ubcMeshReaderBase.clear_models(self)





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


    def _read_up_front(self):
        """Internal helper to read all data at start"""
        reader = ubcMeshReaderBase.ubc_model_3d
        self._models = []
        for f in self._model_filenames:
            # Read the model data
            self._models.append(reader(f))
        self.need_to_read(flag=False)
        return

    def _place_on_mesh(self, output, idx=0):
        """Internal helper to place a model on the mesh for a given index"""
        OcTreeReader.place_model_on_octree_mesh(output, self._models[idx], self.get_data_name())
        return
