"""The ``interface`` module provides functions to convert/cast between common
VTK and NumPy/Pandas data types. These methods provide a simple to use interface
for VTK data types so that users can make changes to VTK data strucutres via
Python data structures that are a bit easier to perform numerical operations
upon.
"""


__all__ = [
    'getVTKtype',
    'convertStringArray',
    'convertArray',
    'dataFrameToTable',
    'tableToDataFrame',
    'placeArrInTable',
    'getdTypes',
    'pointsToPolyData',
]


import numpy as np
import pandas as pd
import vtk
from vtk.numpy_interface import dataset_adapter as dsa
from vtk.util import numpy_support as nps

# Import helpers
from . import _helpers

__displayname__ = 'Interface'


def getVTKtype(typ):
    """This looks up the VTK type for a give python data type.

    Return:
        int : the integer type id specified in vtkType.h
    """
    typ = nps.get_vtk_array_type(typ)
    if typ is 3:
        return 13
    return typ

def convertStringArray(arr):
    """A helper to convert a numpy array of strings to a vtkStringArray

    Return:
        vtkStringArray : the converted array
    """
    vtkarr = vtk.vtkStringArray()
    for val in arr:
        vtkarr.InsertNextValue(val)
    return vtkarr

def convertArray(arr, name='Data', deep=0, array_type=None, pdf=False):
    """A helper to convert a NumPy array to a vtkDataArray or vice versa

    Args:
        arr (ndarray or vtkDataArry) : A numpy array or vtkDataArry to convert
        name (str): the name of the data array for VTK
        deep (bool, int): if input is numpy array then deep copy values
        pdf (bool): if input is vtkDataArry, make a pandas DataFrame of the array

    Return:
        vtkDataArray : the converted array if input is a NumPy ndaray
        ndarray : the converted array if input is a vtkDataArray
        DataFrame : if pdf==True, the vtkDataArry input will be converted to a pandas DataFrame.

    """
    if isinstance(arr, np.ndarray):
        if arr.dtype is np.dtype('O'):
            arr = arr.astype('|S')
        arr = np.ascontiguousarray(arr)
        typ = getVTKtype(arr.dtype)
        if typ is 13:
            VTK_data = convertStringArray(arr)
            return VTK_data
        arr = np.ascontiguousarray(arr)
        VTK_data = nps.numpy_to_vtk(num_array=arr, deep=deep, array_type=array_type)
        VTK_data.SetName(name)
        return VTK_data
    # Otherwise input must be a vtkDataArray
    if not isinstance(arr, vtk.vtkDataArray):
        raise _helpers.PVGeoError('Invalid input array.')
    # Convert from vtkDataArry to NumPy
    num_data = nps.vtk_to_numpy(arr)
    if not pdf:
        return num_data
    return pd.DataFrame(data=num_data, columns=[arr.GetName()])



def dataFrameToTable(df, pdo=None):
    """Converts a pandas DataFrame to a vtkTable"""
    if not isinstance(df, pd.DataFrame):
        raise PVGeoError('Input is not a pandas DataFrame')
    if pdo is None:
        pdo = vtk.vtkTable()
    for key in df.keys():
        VTK_data = convertArray(df[key].values)
        VTK_data.SetName(key)
        pdo.AddColumn(VTK_data)
    return pdo


def tableToDataFrame(table):
    """Converts a vtkTable to a pandas DataFrame"""
    if not isinstance(table, vtk.vtkTable):
        raise PVGeoError('Input is not a vtkTable')
    num = table.GetNumberOfColumns()
    names = [table.GetColumnName(i) for i in range(num)]
    data = dsa.WrapDataObject(table).RowData
    df = pd.DataFrame()
    for i, n in enumerate(names):
        df[n] = np.array(data[n])
    return df


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
        VTK_data = convertArray(ndarr[:,i])
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



def pointsToPolyData(points, copy_z=False):
    """Create ``vtkPolyData`` from a numpy array of XYZ points. If the points have
    more than 3 dimensions, then all dimensions after the third will be added as attributes.
    Assume the first three dimensions are the XYZ coordinates.

    Args:
        points (np.ndarray or pandas.DataFrame): The points and pointdata
        copy_z (bool): A flag on whether to append the z values as a PointData array

    Return:
        vtkPolyData : points with point-vertex cells
    """
    __displayname__ = 'Points to PolyData'
    __category__ = 'filter'
    # Check if input is anything other than a NumPy array and cast it
    # e.g. you could send a Pandas dataframe
    keys = ['Field %d' % i for i in range(points.shape[1] - 3)]
    if not isinstance(points, np.ndarray):
        if isinstance(points, pd.DataFrame):
            # If a pandas data frame, lets grab the keys
            keys = points.keys()[3::]
        points = np.array(points)
    # If points are not 3D
    if points.shape[1] < 2:
        raise RuntimeError('Points must be 3D. Try adding a third dimension of zeros.')

    atts = points[:, 3::]
    points = points[:, 0:3]

    npoints = points.shape[0]

    # Make VTK cells array
    cells = np.hstack((np.ones((npoints, 1)),
                       np.arange(npoints).reshape(-1, 1)))
    cells = np.ascontiguousarray(cells, dtype=np.int64)
    vtkcells = vtk.vtkCellArray()
    vtkcells.SetCells(npoints, nps.numpy_to_vtkIdTypeArray(cells, deep=True))

    # Convert points to vtk object
    pts = vtk.vtkPoints()
    pts.SetData(convertArray(points))

    # Create polydata
    pdata = vtk.vtkPolyData()
    pdata.SetPoints(pts)
    pdata.SetVerts(vtkcells)

    # Add attributes if given
    for i, key in enumerate(keys):
        data = convertArray(atts[:, i], name=key)
        pdata.GetPointData().AddArray(data)
    if copy_z:
        z = convertArray(points[:, 2], name='Elevation')
        pdata.GetPointData().AddArray(z)
    return pdata
