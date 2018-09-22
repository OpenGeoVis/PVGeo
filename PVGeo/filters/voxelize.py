__all__ = [
    'VoxelizePoints',
]

import numpy as np
import vtk
from vtk.util import keys
from vtk.numpy_interface import dataset_adapter as dsa
from vtk.util import numpy_support as nps

from ..base import FilterBase
from .. import _helpers
from ..version import checkNumpy
from .xyz import RotationTool
from .. import interface

###############################################################################


class VoxelizePoints(FilterBase):
    """This makes a ``vtkUnstructuredGrid`` of scattered points given voxel sizes as input arrays.
    This assumes that the data is at least 2-Dimensional on the XY Plane.
    """
    __displayname__ = 'Voxelize Points'
    __category__ = 'filter'
    def __init__(self, **kwargs):
        FilterBase.__init__(self,
            nInputPorts=1, inputType='vtkPolyData',
            nOutputPorts=1, outputType='vtkUnstructuredGrid')
        self.__dx = kwargs.get('dx', None)
        self.__dy = kwargs.get('dy', None)
        self.__dz = kwargs.get('dz', None)
        self.__estimateGrid = kwargs.get('estimate', True)
        self.__safe = kwargs.get('safe', 10.0)

        # Not controlled by user:
        self.__angle = 0.0



    def AddFieldData(self, grid):
        """An internal helper to add the recovered information as field data
        """
        # Add angle
        a = vtk.vtkDoubleArray()
        a.SetName('Recovered Angle (Deg.)')
        a.SetNumberOfValues(1)
        a.SetValue(0, np.rad2deg(self.__angle))
        grid.GetFieldData().AddArray(a)
        # Add cell sizes
        s = vtk.vtkDoubleArray()
        s.SetName('Recovered Cell Sizes')
        s.SetNumberOfComponents(3)
        s.InsertNextTuple3(self.__dx, self.__dy, self.__dz)
        grid.GetFieldData().AddArray(s)
        return grid

    @staticmethod
    def AddCellData(grid, arr, name):
        """Add a NumPy array as cell data to the given grid input
        """
        c = interface.convertArray(arr, name=name)
        grid.GetCellData().AddArray(c)
        return grid


    def EstimateUniformSpacing(self, x, y, z):
        """This assumes that the input points make up some sort of uniformly spaced
        grid on at least an XY Plane
        """
        # TODO: implement ability to rotate around Z axis (think PoroTomo vs UTM)
        # TODO: implement way to estimate rotation
        assert(len(x) == len(y) == len(z))
        num = len(x)
        if num == 1:
            # Only one point.. use safe
            return x, y, z, self.__safe, self.__safe, self.__safe, 0.0

        r = RotationTool()
        xr, yr, zr, dx, dy, angle = r.EstimateAndRotate(x, y, z)
        self.__angle = angle
        uz = np.diff(np.unique(z))
        if len(uz) > 0: dz = np.average(uz)
        else: dz = self.__safe
        self.__dx = dx
        self.__dy = dy
        self.__dz = dz
        return xr, yr, zr


    def PointsToGrid(self, xo,yo,zo, dx,dy,dz, grid=None):
        """Convert XYZ points to a ``vtkUnstructuredGrid``.
        """
        if not checkNumpy(alert='warn'):
            return grid
        if grid is None:
            grid = vtk.vtkUnstructuredGrid()

        # TODO: Check dtypes on all arrays. Need to be floats

        if self.__estimateGrid:
            x,y,z = self.EstimateUniformSpacing(xo, yo, zo)
        else:
            x,y,z = xo, yo, zo

        dx,dy,dz = self.__dx, self.__dy, self.__dz
        if isinstance(dx, np.ndarray) and len(dx) != len(x):
            raise _helpers.PVGeoError('X-Cell spacings are not properly defined for all points.')
        if isinstance(dy, np.ndarray) and len(dy) != len(y):
            raise _helpers.PVGeoError('X-Cell spacings are not properly defined for all points.')
        if isinstance(dz, np.ndarray) and len(dz) != len(z):
            raise _helpers.PVGeoError('X-Cell spacings are not properly defined for all points.')

        numCells = len(x)

        # Generate cell nodes for all points in data set
        #- Bottom
        c_n1 = np.stack( ((x - dx/2) , (y - dy/2), (z - dz/2) ), axis=1)
        c_n2 = np.stack(( (x + dx/2) , (y - dy/2), (z - dz/2) ), axis=1)
        c_n3 = np.stack(( (x - dx/2) , (y + dy/2), (z - dz/2) ), axis=1)
        c_n4 = np.stack(( (x + dx/2) , (y + dy/2), (z - dz/2) ), axis=1)
        #- Top
        c_n5 = np.stack(( (x - dx/2) , (y - dy/2), (z + dz/2) ), axis=1)
        c_n6 = np.stack(( (x + dx/2) , (y - dy/2), (z + dz/2) ), axis=1)
        c_n7 = np.stack(( (x - dx/2) , (y + dy/2), (z + dz/2) ), axis=1)
        c_n8 = np.stack(( (x + dx/2) , (y + dy/2), (z + dz/2) ), axis=1)

        #- Concatenate
        all_nodes = np.concatenate((
            c_n1,
            c_n2,
            c_n3,
            c_n4,
            c_n5,
            c_n6,
            c_n7,
            c_n8), axis=0)

        # Search for unique nodes and use the min cell size as the tolerance
        TOLERANCE = np.min([dx, dy]) / 2.0
        # Round XY plane by the tolerance
        txy = np.around(all_nodes[:,0:2]/TOLERANCE)
        all_nodes[:,0:2] = txy
        unique_nodes, ind_nodes = np.unique(all_nodes, return_inverse=True, axis=0)
        unique_nodes[:,0:2] *= TOLERANCE
        numPts = len(unique_nodes)

        # Make the cells
        pts = vtk.vtkPoints()
        cells = vtk.vtkCellArray()

        # insert unique nodes as points
        if self.__estimateGrid:
            unique_nodes[:,0:2] = RotationTool.Rotate(unique_nodes[:,0:2], -self.__angle)
            self.AddFieldData(grid)

        # Add unique nodes as points in output
        pts.SetData(interface.convertArray(unique_nodes))

        # Add cell vertices
        j = np.multiply(np.tile(np.arange(0, 8, 1), numCells), numCells)
        arridx = np.add(j, np.repeat(np.arange(0, numCells, 1, dtype=int), 8))

        ids = ind_nodes[arridx].reshape((numCells, 8))
        cellsMat = np.concatenate((np.ones((ids.shape[0], 1), dtype=np.int64)*ids.shape[1], ids), axis=1).ravel()

        cells = vtk.vtkCellArray()
        cells.SetNumberOfCells(numCells)
        cells.SetCells(numCells, nps.numpy_to_vtkIdTypeArray(cellsMat, deep=True))

        # Set the output
        grid.SetPoints(pts)
        grid.SetCells(vtk.VTK_VOXEL, cells)
        return grid

    def _CopyArrays(self, pdi, pdo):
        """internal helper to copy arrays from point data to cell data in the voxels.
        """
        for i in range(pdi.GetPointData().GetNumberOfArrays()):
            arr = pdi.GetPointData().GetArray(i)
            _helpers.addArray(pdo, 1, arr) # adds to CELL data
        return pdo

    def RequestData(self, request, inInfoVec, outInfoVec):
        """Used by pipeline to generate output
        """
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfoVec, 0, 0)
        pdo = self.GetOutputData(outInfoVec, 0)
        # Perfrom task
        wpdi = dsa.WrapDataObject(pdi)
        pts = wpdi.Points
        x, y, z = pts[:,0], pts[:,1], pts[:,2]
        self.PointsToGrid(x, y, z,
            self.__dx, self.__dy, self.__dz, grid=pdo)
        # Now append data to grid
        self._CopyArrays(pdi, pdo)
        return 1


    #### Seters and Geters ####


    def SetSafeSize(self, safe):
        """A voxel size to use if a spacing cannot be determined for an axis
        """
        if self.__safe != safe:
            self.__safe = safe
            self.Modified()

    def SetDeltaX(self, dx):
        """Set the X cells spacing

        Args:
            dx (float or np.array(floats)): the spacing(s) for the cells in the X-direction
        """
        self.__dx = dx
        self.Modified()

    def SetDeltaY(self, dy):
        """Set the Y cells spacing

        Args:
            dy (float or np.array(floats)): the spacing(s) for the cells in the Y-direction
        """
        self.__dy = dy
        self.Modified()

    def SetDeltaZ(self, dz):
        """Set the Z cells spacing

        Args:
            dz (float or np.array(floats)): the spacing(s) for the cells in the Z-direction
        """
        self.__dz = dz
        self.SetSafeSize(np.min(dz))
        self.Modified()

    def SetDeltas(self, dx, dy, dz):
        """Set the cell spacings for each axial direction

        Args:
            dx (float or np.array(floats)): the spacing(s) for the cells in the X-direction
            dy (float or np.array(floats)): the spacing(s) for the cells in the Y-direction
            dz (float or np.array(floats)): the spacing(s) for the cells in the Z-direction
        """
        self.SetDeltaX(dx)
        self.SetDeltaY(dy)
        self.SetDeltaZ(dz)

    def SetEstimateGrid(self, flag):
        """Set a flag on whether or not to estimate the grid spacing/rotation
        """
        if self.__estimateGrid != flag:
            self.__estimateGrid = flag
            self.Modified()


    def GetRecoveredAngle(self, degrees=True):
        """Returns the recovered angle if set to recover the input grid. If the
        input points are rotated, then this angle will reflect a close
        approximation of that rotation.

        Args:
            degrees (bool): A flag on to return decimal degrees or radians.
        """
        if degrees: return np.rad2deg(self.__angle)
        return self.__angle

    def GetSpacing(self):
        """Get the cell spacings"""
        return (self.__dx, self.__dy, self.__dz)




###############################################################################
