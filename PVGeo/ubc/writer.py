# __all__ = [
#     'writeUBCTensorMesh'
# ]
#
# import numpy as np
# from vtk.util import numpy_support as nps
# import vtk
# import os
#
# def writeUBCTensorMesh(grid, filename):
#     """
#     grid param must be vtkImageData or vtkRectilinearGrid
#     filename is absolute path
#     """
#     if type(grid) is not vtk.vtkImageData or type(grid) is not vtk.vtkRectilinearGrid:
#         raise _helpers.PVGeoError('`writeUBCTensorMesh()` can on handle `vtk.vtkImageData` or `vtk.vtkRectilinearGrid`.')
#     # get the points along each axis:
#
#     # TODO: decide if 2D or 3D
#
#     # find origin (top southwest corner)
#
#     # flip z
#
#     # get spacings
#
#     # write out
#
#     with open(filename, 'w') as f:
#         f.write('%d %d %d\n' % (nx,ny,nz))
#
#
#
#     return None
