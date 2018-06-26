""" This file provides methods for generating a vtkUnstructuredGrid
full of voxels from a point set of data.
This will soon be included in PVGeo
Author: Bane Sullivan
"""

__all__ = [
    'addCellData',
    'voxelizePoints',
    'voxelizePointsWrapper'
]

import numpy as np
import vtk
from vtk.util import numpy_support as nps

from ..version import checkNumpy




def _estimateUniformSpacing(x, y, z, dx=None, dy=None, dz=None, safe=10.0):
    """
    This assumes that the input points make up some sort of uniformly spaced
    grid. If those points do not vary along a specified axis, then use
    (dx,dy,dz) args to set a default spacing. Otherwise nonvarying axis spacings
    will be determined by other axii.
    """
    # TODO: implement ability to rotate around Z axis (think PoroTomo vs UTM)
    # TODO: implement way to estimate rotation
    if (len(x) != len(y) != len(z)):
        raise RuntimeError('The coordinate arrays must have the same lengths.')

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


def addCellData(grid, arr, name):
    c = nps.numpy_to_vtk(num_array=arr, deep=True)
    c.SetName(name)
    grid.GetCellData().AddArray(c)
    return grid


def voxelizePoints(x, y, z, dx, dy, dz, grid=None, safe=10.0, estimate_grid=True):
    if not checkNumpy(warn=False):
        raise RuntimeError("points2grid() cannot work with versions of NumPy below 1.10.x . You must update ParaView\'s NumPy")
        return None
    if grid is None:
        grid = vtk.vtkUnstructuredGrid()

    if estimate_grid:
        dx, dy, dz = _estimateUniformSpacing(x, y, z, dx=dx, dy=dy, dz=dz)

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
    addCellData(grid, arridx, 'Voxel ID')

    return grid


def voxelizePointsWrapper(grid, tup):
    x,dx,y,dy,z,dz = tup
    return voxelizePoints(x,y,z, dx,dy,dz, grid=grid)


###############################################################################

# ## For Testing:
# x = np.array([0.0,1.0,0.0])
# y = np.array([0.0,0.0,1.0])
# z = np.array([0.0,0.0,0.0])
# dx = 10.0
# dy = 10.0
# dz = 10.0
# grid = points2grid(x,y,z,dx,dy,dz)
# # Write out for viewing in ParaView
# writer = vtk.vtkXMLUnstructuredGridWriter()
# writer.SetFileName('/Users/bane/Desktop/testme.vtu')
# ###writer.SetDataModeToAscii() # Only for testing. Do not use.
# writer.SetInputData(grid)
# writer.Write()
