"""
These are helpers specifically for the file readers for private use only.
@author: Bane Sullivan
"""
__all__ = [
    'getVTKtype',
    'placeArrInTable',
    'getdTypes',
    'cleanDataNm'
]

import numpy as np
from vtk.util import numpy_support as nps
import vtk
import os
from . import errors as _helpers

def getVTKtype(typ):
    """This looks up the VTK type for a give python data type.

    Return:
        int : the integer type id specified in vtkType.h
    """
    typ = nps.get_vtk_array_type(typ)
    if typ is 3:
        return 13
    return typ

def converStringArray(arr):
    """A helper to convert a numpy array of strings to a vtkStringArray

    Return:
        vtkStringArray : the converted array
    """
    vtkarr = vtk.vtkStringArray()
    for val in arr:
        vtkarr.InsertNextValue(val)
    return vtkarr

def ConvertArray(arr):
    """A helper to convert a numpy array to a vtkDataArray

    Return:
        vtkDataArray : the converted array

    Note:
        this converts the data array but does not set a name. The name must be set for this data array to be added to a vtkDataSet ``array.SetName('Data')``
    """
    typ = getVTKtype(arr.dtype)
    if typ is 13:
        VTK_data = converStringArray(arr)
    else:
        VTK_data = nps.numpy_to_vtk(num_array=arr, deep=True, array_type=typ)
    return VTK_data


def placeArrInTable(ndarr, titles, pdo):
    """Takes a 1D/2D numpy array and makes a vtkTable of it

    Args:
        ndarr (numpy.ndarray) : The 1D/2D array to be converted to a table
        titles (list or tuple): The titles for the arrays in the table. Must have same number of elements as columns in input ndarray
        pdo (vtkTable) : The output data object pointer

    Return:
        vtkTable : returns the same input pdo table
    """
    # Put columns into table
    if len(np.shape(ndarr)) > 2:
        raise _helpers.PVGeoError('Input np.ndarray must be 1D or 2D to be converted to vtkTable.')
    if len(np.shape(ndarr)) == 1:
        # First check if it is an array full of tuples (varying type)
        if isinstance(ndarr[0], (tuple, np.void)):
            for i in range(len(titles)):
                placeArrInTable(ndarr['f%d' % i], [titles[i]], pdo)
            return pdo
        # Otherwise it is just a 1D array which needs to be 2D
        else:
            ndarr = np.reshape(ndarr, (-1, 1))
    cols = np.shape(ndarr)[1]

    for i in range(cols):
        VTK_data = ConvertArray(ndarr[:,i])
        VTK_data.SetName(titles[i])
        pdo.AddColumn(VTK_data)
    return pdo



def getdTypes(dtype='', endian=None):
    """This converts char dtypes and an endian to a numpy and VTK data type.

    Return:
        tuple (numpy.dtype, int) : the numpy data type and the integer type id specified in vtkType.h for VTK data types
    """
    # If native `@` was chosen then do not pass an endian
    if endian is '@':
        #print('WARNING: Native endianness no longer supported for packed binary reader. Please chose `>` or `<`. This defaults to big `>`.')
        endian = ''
    # No endian specified:
    elif endian is None:
        endian = ''
    # Get numpy and VTK data types and return them both
    if dtype is 'd':
        vtktype = vtk.VTK_DOUBLE
    elif dtype is 'f':
        vtktype = vtk.VTK_FLOAT
    elif dtype is 'i':
        vtktype = vtk.VTK_INT
    else:
        raise _helpers.PVGeoError('dtype \'%s\' unknown:' % dtype)
    # Return data types
    dtype = np.dtype('%s%s' % (endian, dtype))
    return dtype, vtktype


def cleanDataNm(dataNm, FileName):
    """A helper to clean a FileName to make a useful data array name"""
    if dataNm is None or dataNm == '':
        dataNm = os.path.splitext(os.path.basename(FileName))[0]
    return dataNm
