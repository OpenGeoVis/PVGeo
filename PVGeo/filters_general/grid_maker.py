__all__ = [
    'VoxelizePoints',
]

import numpy as np
import vtk
from vtk.util import numpy_support as nps
from vtk.numpy_interface import dataset_adapter as dsa

from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase
from .. import _helpers
from ..version import checkNumpy



class VoxelizePoints(VTKPythonAlgorithmBase):
    """This makes a vtkUnstructuredGrid of scattered points given voxel sizes as input arrays."""
    def __init__(self):
        VTKPythonAlgorithmBase.__init__(self,
            nInputPorts=1, inputType='vtkPolyData',
            nOutputPorts=1, outputType='vtkUnstructuredGrid')
        self.__dx = None
        self.__dy = None
        self.__dz = None
        self.__estimatGrid = True

    @staticmethod
    def AddCellData(grid, arr, name):
        c = nps.numpy_to_vtk(num_array=arr, deep=True)
        c.SetName(name)
        grid.GetCellData().AddArray(c)
        return grid

    @staticmethod
    def EstimateUniformSpacing(x, y, z, dx=None, dy=None, dz=None, safe=10.0):
        """
        This assumes that the input points make up some sort of uniformly spaced
        grid. If those points do not vary along a specified axis, then use
        (dx,dy,dz) args to set a default spacing. Otherwise nonvarying axis spacings
        will be determined by other axii.
        """
        # TODO: implement ability to rotate around Z axis (think PoroTomo vs UTM)
        # TODO: implement way to estimate rotation
        assert(len(x)==len(y)==len(z))
        num = len(x)
        default = [dx,dy,dz]
        if num == 1:
            # Only one point.. use default
            for i in range(3):
                if default[i] is None:
                    default[i] = safe
            return default

        # Get unique elements
        us = [np.unique(x), np.unique(y), np.unique(z)]
        diffs = []
        for u in us:
            diffs.append(np.diff(u))
        for i in range(3):
            if len(diffs[i]) > 0:
                # Get average spacing
                diffs[i] = np.average(diffs[i])

        # If an axis did not vary, then use one of the other axii to determine spacing
        diffs.append(diffs[0])
        diffs.append(diffs[1])
        for i in range(3):
            # Axis does not vary and no default given
            if isinstance(diffs[i], np.ndarray) and default[i] is None:
                if isinstance(diffs[i+1], np.ndarray):
                    default[i] = default[i+2]
                else: default[i] = diffs[i+1]
            elif isinstance(diffs[i], np.ndarray) and default[i] is not None:
                pass
            else: default[i] = diffs[i]

        # This is an easy way if the points definitely make a 3D grid...
        # dx = np.average(np.diff(np.unique(x)))
        # dy = np.average(np.diff(np.unique(y)))
        # dz = np.average(np.diff(np.unique(z)))

        return default[0], default[1], default[2]

    @staticmethod
    def PointsToGrid(x,y,z, dx,dy,dz, grid=None, estimate_grid=True):
        if not checkNumpy():
            raise RuntimeError("`VoxelizePoints` cannot work with versions of NumPy below 1.10.x . You must update NumPy.")
            return None
        if grid is None:
            grid = vtk.vtkUnstructuredGrid()

        if estimate_grid:
            dx, dy, dz = VoxelizePoints.EstimateUniformSpacing(x, y, z, dx=dx, dy=dy, dz=dz)

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

        # Search for unique nodes
        unique_nodes, ind_nodes = np.unique(all_nodes, return_inverse=True, axis=0)
        numPts = len(unique_nodes)

        # Make the cells
        pts = vtk.vtkPoints()
        cells = vtk.vtkCellArray()

        # insert unique nodes as points
        for i in range(numPts):
            # for each node
            pts.InsertPoint(i,
                unique_nodes[i,0], unique_nodes[i,1], unique_nodes[i,2]
            )

        cnt = 0
        arridx = np.zeros(numCells)
        for i in range(numCells):
            vox = vtk.vtkVoxel()
            for j in range(8):
                vox.GetPointIds().SetId(j, ind_nodes[j*numCells + i])
            cells.InsertNextCell(vox)

            arridx[i] = i
            cnt += 8

        grid.SetPoints(pts)
        grid.SetCells(vtk.VTK_VOXEL, cells)
        VoxelizePoints.AddCellData(grid, arridx, 'Voxel ID')

        return grid

    @staticmethod
    def PointsToGridWrapper(grid, tup):
        """tup = (x,dx,y,dy,z,dz)"""
        x, dx, y, dy, z, dz = tup
        return VoxelizePoints.PointsToGrid(x, y, z, dx, dy, dz, grid=grid)

    def _CopyArrays(self, pdi, pdo):
        for i in range(pdi.GetPointData().GetNumberOfArrays()):
            arr = pdi.GetPointData().GetArray(i)
            _helpers.addArray(pdo, 1, arr) # adds to CELL data
        return pdo

    def RequestData(self, request, inInfo, outInfo):
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        pdo = self.GetOutputData(outInfo, 0)
        # Perfrom task
        wpdi = dsa.WrapDataObject(pdi)
        pts = wpdi.Points
        x, y, z = pts[:,0], pts[:,1], pts[:,2]
        VoxelizePoints.PointsToGrid(x, y, z,
            self.__dx, self.__dy, self.__dz,
            grid=pdo, estimate_grid=self.__estimatGrid)
        # Now append data to grid
        self._CopyArrays(pdi, pdo)
        return 1

    #### Seters and Geters ####

    def SetDeltaX(self, dx):
        self.__dx = dx
        self.Modified()

    def SetDeltaY(self, dy):
        self.__dy = dy
        self.Modified()

    def SetDeltaZ(self, dz):
        self.__dz = dz
        self.Modified()

    def SetEstimateGrid(self, flag):
        if self.__estimatGrid != flag:
            self.__estimatGrid = flag
            self.Modified()





###############################################################################

# ## For Testing:
# x = np.array([0.0,1.0,0.0])
# y = np.array([0.0,0.0,1.0])
# z = np.array([0.0,0.0,0.0])
# dx = 10.0
# dy = 10.0
# dz = 10.0
# grid = VoxelizePoints.PointsToGrid(x,y,z,dx,dy,dz)
# # Write out for viewing in ParaView
# writer = vtk.vtkXMLUnstructuredGridWriter()
# writer.SetFileName('/Users/bane/Desktop/testme.vtu')
# ###writer.SetDataModeToAscii() # Only for testing. Do not use.
# writer.SetInputData(grid)
# writer.Write()
