__all__ = [
    'readPVGPGridExtents',
    'readPVGPGrid'
]

import numpy as np
from vtk.util import numpy_support as nps
import vtk
import json
import struct
import base64


#-----------
# PVGP Custom Grid file type
"""
This file reader will open a header file that points to a packed binary data files
The header will have Parameters for extent, spacing, origin, and number of arrays
Each data array will be in a seperate binary data file

Example Header in Json Format
"""


def _getdtypes(dtype):
    if dtype == 'float64':
        num_bytes = 8 # DOUBLE
        sdtype = 'd'
        vtktype = vtk.VTK_DOUBLE
    elif dtype == 'float32':
        num_bytes = 4 # FLOAT
        sdtype = 'f'
        vtktype = vtk.VTK_FLOAT
    elif 'int' in dtype:
        num_bytes = 4 # INTEGER
        sdtype = 'i'
        vtktype = vtk.VTK_INT
    else:
        raise Exception('dtype \'%s\' unknown.' % dtype)

    return dtype, sdtype, num_bytes, vtktype


def readPVGPGridExtents(headerfile):
    with open(headerfile, 'r') as f:
        lib = json.load(f)
    n1,n2,n3 = lib['extent']
    return (0,n1-1, 0,n2-1, 0,n3-1)


def readPVGPGrid(headerfile, pdo=None, path=None):
    """
    @desc:
    Generates vtkImageData from the uniform grid defined in the PVGP uniformly gridded data format.

    @params:
    headerfile : str: req : The file name / absolute path for the input header file that cotains all parameters and pointers to file locations.
    pdo : vtk.vtkImageData : opt : A pointer to the output data object.
    path : str : opt : The absolute path to the PVGP grid database to override the path in the header file.

    @return:
    vtkImageData : A uniformly spaced gridded volume of data from input file

    """
    if pdo is None:
        pdo = vtk.vtkImageData() # vtkImageData
    # Read and parse header file
    with open(headerfile, 'r') as f:
        lib = json.load(f)
    basename = lib['basename']
    extent = lib['extent']
    spacing = lib['spacing']
    origin = lib['origin']
    order = lib['order']
    endian = lib['endian']
    numArrays = lib['numArrays']
    dataArrays = lib['dataArrays']
    if path is None:
        path = lib['originalPath']

    # Grab Parameters
    n1, n2, n3 = extent
    ox, oy, oz = origin
    sx, sy, sz = spacing
    # Setup vtkImageData
    pdo.SetDimensions(n1, n2, n3)
    pdo.SetExtent(0,n1-1, 0,n2-1, 0,n3-1)
    pdo.SetOrigin(ox, oy, oz)
    pdo.SetSpacing(sx, sy, sz)
    # Read in data arrays
    dataArrs = []
    dataNames = []
    vtktypes = []
    for darr in dataArrays:
        dataNames.append(darr)
        dtype, sdtype, num_bytes, vtktype = _getdtypes(dataArrays[darr]['dtype'])
        vtktypes.append(vtktype)
        # Grab and decode data array
        encoded = base64.b64decode(dataArrays[darr]['data'])

        raw = struct.unpack(endian+str(n1*n2*n3)+sdtype, encoded)
        dataArrs.append(np.asarray(raw, dtype=dtype))

    """TODO:
    if order is not 'F':
        # Reshape the arrays
        arr = np.reshape(arr, (n1,n2,n3), order=order).flatten(order='C')"""

    # vtk data arrays
    for i in range(numArrays):
        arr = dataArrs[i]
        VTK_data = nps.numpy_to_vtk(num_array=arr, deep=True, array_type=vtktypes[i])
        VTK_data.SetName(dataNames[i])
        pdo.GetPointData().AddArray(VTK_data)

    return pdo
