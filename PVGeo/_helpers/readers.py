"""
These are helpers specifically for the file readers for private use only.
@author: Bane Sullivan
"""
__all__ = [
    '_getVTKtype',
    '_placeArrInTable',
    '_getdTypes',
    '_cleanDataNm'
]

import numpy as np
from vtk.util import numpy_support as nps
import vtk
import os


def _getVTKtype(typ):
    """
    @desc: This looks up the VTK type for a give python data type.

    @notes:
    Types are specified in vtkType.h
    """
    return nps.get_vtk_array_type(typ)


def _placeArrInTable(ndarr, titles, pdo):
    """
    @desc: Takes a 2D numpy array and makes a vtkTable of it
    @params:
        ndarr : np.ndarray : The 1D/2D array to be converted to a table
        titles : list or tuple : The titles for the arrays in the table. Must have same number of elements as columns in input ndarray
        pdo : vtkTable : The output data object pointer
    @returns:
        vtkTable : returns the same input pdo table
    """
    # Put columns into table
    if len(np.shape(ndarr)) > 2:
        raise Exception('Input np.ndarray must be 1D or 2D to be converted to vtkTable.')
    cols = np.shape(ndarr)[1]

    for i in range(cols):
        typ = _getVTKtype(ndarr[:,i].dtype)
        VTK_data = nps.numpy_to_vtk(num_array=ndarr[:,i], deep=True, array_type=typ)
        VTK_data.SetName(titles[i])
        pdo.AddColumn(VTK_data)
    return pdo



def _getdTypes(dtype='', endian=None):
    """
    @desc: This converts char dtypes and an endian to a numpy and VTK data type.
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
        dtype = np.dtype('%sd'%endian) # DOUBLE
        vtktype = vtk.VTK_DOUBLE
    elif dtype is 'f':
        dtype = np.dtype('%sf'%endian) # FLOAT
        vtktype = vtk.VTK_FLOAT
    elif dtype is 'i':
        dtype = np.dtype('%si'%endian) # INTEGER
        vtktype = vtk.VTK_INT
    else:
        raise Exception('dtype \'%s\' unknown/.' % dtype)
    # Return data types
    return dtype, vtktype


def _cleanDataNm(dataNm, FileName):
    if dataNm is None or dataNm == '' or dataNm == 'values':
        dataNm = os.path.splitext(os.path.basename(FileName))[0]
    return dataNm
