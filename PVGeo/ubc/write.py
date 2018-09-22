__all__ = [
    'WriteRectilinearGridToUBC',
    'WriteImageDataToUBC',
]

import numpy as np
import vtk
import os


from ..base import WriterBase
from .. import _helpers
from .. import interface


class ubcTensorMeshWriterBase(WriterBase):
    """A base class to assist in writing data bjects to the UBC Tensor Mesh format"""
    __displayname__ = 'UBC Format Writer Base'
    __category__ = 'base'
    def __init__(self, inputType='vtkRectilinearGrid'):
        WriterBase.__init__(self, inputType=inputType, ext='msh')
        # These MUST be set by children
        self.xcells = None
        self.ycells = None
        self.zcells = None
        self.origin= None


    def WriteMesh3D(self, nx, ny, nz, filename):
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

    def WriteModels(self, grd, filename):
        """Write cell data attributes to model files"""
        nx, ny, nz = grd.GetDimensions()
        nx -= 1
        ny -= 1
        nz -= 1

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
            arr = interface.convertArray(vtkarr)
            arr = reshapeModel(arr)
            path = os.path.dirname(filename)
            fname = '%s/%s.mod' % (path, vtkarr.GetName().replace(' ', '_'))
            np.savetxt(fname, arr, comments='! ', header='Mesh File: %s' % os.path.basename(filename), fmt=self.GetFormat())

        return


class WriteRectilinearGridToUBC(ubcTensorMeshWriterBase):
    """Writes a ``vtkRectilinearGrid`` data object to the UBC Tensor Mesh format.
    This file reader currently only handles 3D data.
    """
    __displayname__ = 'Write ``vtkRectilinearGrid`` to UBC Tensor Mesh'
    __category__ = 'writer'
    def __init__(self):
        ubcTensorMeshWriterBase.__init__(self, inputType='vtkRectilinearGrid')


    def PerformWriteOut(self, inputDataObject, filename):
        # Get the input data object
        grd = inputDataObject

        # Get grid dimensions
        nx, ny, nz = grd.GetDimensions()


        # get the points and convert to spacings
        xcoords = interface.convertArray(grd.GetXCoordinates())
        ycoords = interface.convertArray(grd.GetYCoordinates())
        zcoords = interface.convertArray(grd.GetZCoordinates())

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
        self.WriteMesh3D(nx-1, ny-1, nz-1, filename)

        # Now write out model data
        self.WriteModels(grd, filename)

        # Always return 1 from pipeline methods or seg-faults will occur
        return 1




class WriteImageDataToUBC(ubcTensorMeshWriterBase):
    """Writes a ``vtkImageData`` (uniform grid) data object to the UBC Tensor Mesh format.
    This file reader currently only handles 3D data.
    """
    __displayname__ = 'Write ``vtkImageData`` to UBC Tensor Mesh'
    __category__ = 'writer'
    def __init__(self):
        ubcTensorMeshWriterBase.__init__(self, inputType='vtkImageData')


    def PerformWriteOut(self, inputDataObject, filename):
        # Get the input data object
        grd = inputDataObject

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
        self.WriteMesh3D(nx, ny, nz, filename)

        # Now write out model data
        self.WriteModels(grd, filename)

        # Always return 1 from pipeline methods or seg-faults will occur
        return 1
