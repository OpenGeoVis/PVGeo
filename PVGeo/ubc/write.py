__all__ = [
    'WriteRectilinearGridToUBC',
    'WriteImageDataToUBC',
]

__displayname__ = 'Writers'

import os

import numpy as np
import vtk

from .. import _helpers, interface
from ..base import WriterBase


class ubcTensorMeshWriterBase(WriterBase):
    """A base class to assist in writing data bjects to the UBC Tensor Mesh
    format.
    """
    __displayname__ = 'UBC Format Writer Base'
    __category__ = 'base'
    def __init__(self, inputType='vtkRectilinearGrid'):
        WriterBase.__init__(self, inputType=inputType, ext='msh')
        # These MUST be set by children
        self.xcells = None
        self.ycells = None
        self.zcells = None
        self.origin= None


    def write_mesh_3d(self, nx, ny, nz, filename):
        """Write 3D Tensor Mesh to the UBC format"""
        def arr2str(arr):
            return ' '.join(map(str, arr))

        ox, oy, oz = self.origin

        # Write out grid / mesh
        with open(filename, 'w') as f:
            f.write('%d %d %d\n' % (nx, ny, nz))
            f.write('%d %d %d\n' % (ox, oy, oz))
            f.write('%s\n' % arr2str(self.xcells))
            f.write('%s\n' % arr2str(self.ycells))
            f.write('%s\n' % arr2str(self.zcells))
        return

    def write_models(self, grd, filename):
        """Write cell data attributes to model files"""
        nx, ny, nz = grd.GetDimensions()
        nx -= 1
        ny -= 1
        nz -= 1

        def reshape_model(model):
            # Swap axes because VTK structures the coordinates a bit differently
            #-  This is absolutely crucial!
            #-  Do not play with unless you know what you are doing!
            model = np.reshape(model, (nz, ny, nx))
            model = np.swapaxes(model, 0, 2)
            model = np.swapaxes(model, 0, 1)
            # Now reverse Z axis
            model = model[:, :, ::-1]
            return model.flatten()

        # make up file names for models
        for i in range(grd.GetCellData().GetNumberOfArrays()):
            vtkarr = grd.GetCellData().GetArray(i)
            arr = interface.convert_array(vtkarr)
            arr = reshape_model(arr)
            path = os.path.dirname(filename)
            filename = '%s/%s.mod' % (path, vtkarr.GetName().replace(' ', '_'))
            np.savetxt(filename, arr, comments='! ', header='Mesh File: %s' % os.path.basename(filename), fmt=self.get_format())

        return


class WriteRectilinearGridToUBC(ubcTensorMeshWriterBase):
    """Writes a ``vtkRectilinearGrid`` data object to the UBC Tensor Mesh format.
    This file reader currently only handles 3D data.
    """
    __displayname__ = 'Write ``vtkRectilinearGrid`` to UBC Tensor Mesh'
    __category__ = 'writer'
    def __init__(self):
        ubcTensorMeshWriterBase.__init__(self, inputType='vtkRectilinearGrid')


    def perform_write_out(self, input_data_object, filename, object_name):
        """Write out a ``vtkRectilinearGrid`` to the UBC file format"""
        # Get the input data object
        grd = input_data_object

        # Get grid dimensions
        nx, ny, nz = grd.GetDimensions()


        # get the points and convert to spacings
        xcoords = interface.convert_array(grd.GetXCoordinates())
        ycoords = interface.convert_array(grd.GetYCoordinates())
        zcoords = interface.convert_array(grd.GetZCoordinates())

        # TODO: decide if 2D or 3D

        # Now get the cell sizes
        self.xcells = np.diff(xcoords)
        self.ycells = np.diff(ycoords)
        self.zcells = np.diff(zcoords)

        # find origin (top southwest corner): this works because of input type
        ox, oy, oz = np.min(xcoords), np.min(ycoords), np.max(zcoords)
        self.origin = (ox, oy, oz)
        # flip z
        self.zcells = self.zcells[::-1]

        # Write mesh
        self.write_mesh_3d(nx-1, ny-1, nz-1, filename)

        # Now write out model data
        self.write_models(grd, filename)

        # Always return 1 from pipeline methods or seg-faults will occur
        return 1




class WriteImageDataToUBC(ubcTensorMeshWriterBase):
    """Writes a ``vtkImageData`` (uniform grid) data object to the UBC Tensor
    Mesh format. This file reader currently only handles 3D data.
    """
    __displayname__ = 'Write ``vtkImageData`` to UBC Tensor Mesh'
    __category__ = 'writer'
    def __init__(self):
        ubcTensorMeshWriterBase.__init__(self, inputType='vtkImageData')


    def perform_write_out(self, input_data_object, filename, object_name):
        """Write out a ``vtkImageData`` to the UBC file format"""
        # Get the input data object
        grd = input_data_object

        # Get grid dimensions
        nx, ny, nz = grd.GetDimensions()
        nx -= 1
        ny -= 1
        nz -= 1

        # get the points and convert to spacings
        dx, dy, dz = grd.GetSpacing()

        # Now make the cell arrays
        self.xcells = np.full(nx, dx)
        self.ycells = np.full(ny, dy)
        self.zcells = np.full(nz, dz)

        # find origin (top southwest corner)
        ox, oy, oz = grd.GetOrigin()
        oz += (nz*dz)
        self.origin = (ox, oy, oz)

        # TODO: decide if 2D or 3D

        # Write mesh
        self.write_mesh_3d(nx, ny, nz, filename)

        # Now write out model data
        self.write_models(grd, filename)

        # Always return 1 from pipeline methods or seg-faults will occur
        return 1
