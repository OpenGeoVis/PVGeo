__all__ = [
    'WriteRectilinearGridToUBC',
    'WriteImageDataToUBC',
]

import numpy as np
from vtk.util import numpy_support as nps
import vtk
import os


from ..base import WriterBase
from .. import _helpers


class ubcTensorMeshWriterBase(WriterBase):
    """A base class to assist in writing data bjects to the UBC Tensor Mesh format"""
    __displayname__ = 'UBC Format Writer Base'
    __type__ = 'base'
    def __init__(self, inputType='vtkRectilinearGrid'):
        WriterBase.__init__(self, inputType=inputType, ext='msh')


    def WriteMesh3D(self):
        def arr2str(arr):
            return ' '.join(map(str, arr))

        nx, ny, nz = self.dim
        ox, oy, oz = self.origin

        # Write out grid / mesh
        with open(self.GetFileName(), 'w') as f:
            f.write('%d %d %d\n' % (nx, ny, nz))
            f.write('%d %d %d\n' % (ox, oy, oz))
            f.write('%s\n' % arr2str(self.xcells))
            f.write('%s\n' % arr2str(self.ycells))
            f.write('%s\n' % arr2str(self.zcells))
        return

    def WriteModels(self, grd):
        """Write cell data attributes to model files"""
        nx, ny, nz = self.dim

        def reshapeModel(model):
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
            arr = nps.vtk_to_numpy(vtkarr)
            arr = reshapeModel(arr)
            path = os.path.dirname(self.GetFileName())
            fname = '%s/%s.mod' % (path, vtkarr.GetName())
            np.savetxt(fname, arr, comments='! ', header='Mesh File: %s' % os.path.basename(self.GetFileName()))

        return


class WriteRectilinearGridToUBC(ubcTensorMeshWriterBase):
    """Writes a ``vtkRectilinearGrid`` data object to the UBC Tensor Mesh format.
    This file reader currently only handles 3D data.
    """
    __displayname__ = 'Write ``vtkRectilinearGrid`` to UBC Tensor Mesh'
    __type__ = 'writer'
    def __init__(self):
        ubcTensorMeshWriterBase.__init__(self, inputType='vtkRectilinearGrid')


    def RequestData(self, request, inInfoVec, outInfoVec):
        # Get the input data object
        grd = self.GetInputData(inInfoVec, 0, 0)

        # Get grid dimensions
        nx, ny, nz = grd.GetDimensions()
        nx -= 1
        ny -= 1
        nz -= 1
        self.dim = (nx, ny, nz)

        # get the points and convert to spacings
        xcoords = nps.vtk_to_numpy(grd.GetXCoordinates())
        ycoords = nps.vtk_to_numpy(grd.GetYCoordinates())
        zcoords = nps.vtk_to_numpy(grd.GetZCoordinates())

        # Now get the cell sizes
        self.xcells = np.diff(xcoords)
        self.ycells = np.diff(ycoords)
        self.zcells = np.diff(zcoords)

        # find origin (top southwest corner): this works because of input type
        ox, oy, oz = np.min(xcoords), np.min(ycoords), np.max(zcoords)
        self.origin = (ox, oy, oz)
        # flip z
        self.zcells = self.zcells[::-1]

        # TODO: decide if 2D or 3D

        # Write mesh
        self.WriteMesh3D()

        # Now write out model data
        self.WriteModels(grd)

        # Always return 1 from pipeline methods or seg-faults will occur
        return 1




class WriteImageDataToUBC(ubcTensorMeshWriterBase):
    """Writes a ``vtkImageData`` (uniform grid) data object to the UBC Tensor Mesh format.
    This file reader currently only handles 3D data.
    """
    __displayname__ = 'Write ``vtkImageData`` to UBC Tensor Mesh'
    __type__ = 'writer'
    def __init__(self):
        ubcTensorMeshWriterBase.__init__(self, inputType='vtkImageData')


    def RequestData(self, request, inInfoVec, outInfoVec):
        # Get the input data object
        grd = self.GetInputData(inInfoVec, 0, 0)

        # Get grid dimensions
        nx, ny, nz = grd.GetDimensions()
        nx -= 1
        ny -= 1
        nz -= 1
        self.dim = (nx, ny, nz)

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
        self.WriteMesh3D()

        # Now write out model data
        self.WriteModels(grd)

        # Always return 1 from pipeline methods or seg-faults will occur
        return 1