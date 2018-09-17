__all__ = [
    'numToVTK',
    'getSelectedArrayName',
    'getSelectedArrayField',
    'copyArraysToPointData',
    'getNumPyArray',
    'getVTKArray',
    'addArray',
    'getSelectedArray',
    #'GetDecimalPlaces',
    'SearchForArray',
]

import vtk
import numpy as np
from vtk.util import numpy_support as nps
from . import errors as _helpers

def numToVTK(arr, name=None, deep=0, array_type=None):
    """Converts a 1D numpy array to a VTK data array given a nameself.

    Args:
        arr (np.array) : A 1D numpy array
        name (str): the name of the data array for VTK

    Return:
        vtkDataArray : a converted data array
    """
    arr = np.ascontiguousarray(arr)
    c = nps.numpy_to_vtk(num_array=arr, deep=deep, array_type=array_type)
    if name:
        c.SetName(name)
    return c


def getSelectedArrayName(algorithm, idx):
    """Gets the name of the input array for a given index on a VTK algorithm

    Args:
        algorithm (vtkAlgorithm): A vtkAlgorithm class instantiation
        idx (int): the input array index

    Return:
        str : the name of the input array for the given index
    """
    info = algorithm.GetInputArrayInformation(idx)
    return info.Get(vtk.vtkDataObject.FIELD_NAME())


def getSelectedArrayField(algorithm, idx):
    """Gets the field of the input array for a given index on a VTK algorithm

    Args:
        algorithm (vtkAlgorithm) : A vtkAlgorithm class instantiation
        idx (int) : the input array index

    Return:
        int : the field type of the input array for the given index
    """
    info = algorithm.GetInputArrayInformation(idx)
    return info.Get(vtk.vtkDataObject.FIELD_ASSOCIATION())


def copyArraysToPointData(pdi, pdo, field):
    """Copys arrays from an input to an ouput's point data.

    Args:
        pdi (vtkDataObject) : The input data object to copy from
        pdo (vtkDataObject) : The output data object to copy over to
        field (int) : the field type id

    Return:
        vtkDataObject : returns the output data object parameter
    """
    # Point Data
    if field == 0:
        for i in range(pdi.GetPointData().GetNumberOfArrays()):
            arr = pdi.GetPointData().GetArray(i)
            pdo.GetPointData().AddArray(arr)
    # Cell Data: DO NOT USE
    elif field == 1:
        for i in range(pdi.GetCellData().GetNumberOfArrays()):
            arr = pdi.GetCellData().GetArray(i)
            pdo.GetPointData().AddArray(arr)
    # Field Data:
    elif field == 2:
        for i in range(pdi.GetFieldData().GetNumberOfArrays()):
            arr = pdi.GetFieldData().GetArray(i)
            pdo.GetPointData().AddArray(arr)
    # Row Data:
    elif field == 6:
        for i in range(pdi.GetRowData().GetNumberOfArrays()):
            arr = pdi.GetRowData().GetArray(i)
            pdo.GetPointData().AddArray(arr)
    else:
        raise _helpers.PVGeoError('Field association not defined. Try inputing Point, Cell, Field, or Row data.')

    # Field Data
    return pdo


def getNumPyArray(wpdi, field, name):
    """Grabs an array from vtkDataObject given its name and field association.

    Args:
        wpdi  (wrapped vtkDataObject) : the input data object wrapped using vtk dataset adapter
        field (int) : the field type id
        name (str) : the name of the input array for the given index

    Return:
        numpy.array : a wrapped ``vtkDataArray`` for NumPy
    """
    # Point Data
    if field == 0:
        arr = wpdi.PointData[name]
    # Cell Data:
    elif field == 1:
        arr = wpdi.CellData[name]
    # Field Data:
    elif field == 2:
        arr = wpdi.FieldData[name]
    # Row Data:
    elif field == 6:
        arr = wpdi.RowData[name]
    else:
        raise _helpers.PVGeoError('Field association not defined. Try inputing Point, Cell, Field, or Row data.')
    return arr

def getVTKArray(pdi, field, name):
    """Grabs an array from vtkDataObject given its name and field association.

    Args:
        pdi  (vtkDataObject) : the input data object
        field (int) : the field type id
        name (str) : the name of the input array for the given index

    Return:
        vtkDataArray : the array from input field and name
    """
    # Point Data
    if field == 0:
        arr = pdi.GetPointData().GetArray(name)
    # Cell Data:
    elif field == 1:
        arr = pdi.GetCellData().GetArray(name)
    # Field Data:
    elif field == 2:
        arr = pdi.GetFieldData().GetArray(name)
    # Row Data:
    elif field == 6:
        arr = pdi.GetRowData().GetArray(name)
    else:
        raise _helpers.PVGeoError('Field association not defined. Try inputing Point, Cell, Field, or Row data.')
    return arr


def getSelectedArray(algorithm, wpdi, idx):
    """Gets selectected array at index idx wrapped for NumPy

    Args:
        algorithm (vtkAlgorithm) : A vtkAlgorithm class instantiation
        wpdi (wrapped vtkDataObject) : the input data object wrapped using vtk dataset adapter
        idx (int) : the input array index

    Return:
        numpy.array : a wrapped ``vtkDataArray`` for NumPy
    """
    name = getSelectedArrayName(algorithm, idx)
    field = getSelectedArrayField(algorithm, idx)
    return getArray(wpdi, field, name)

def addArray(pdo, field, vtkArray):
    """Adds an array to a vtkDataObject given its field association.

    Args:
        pdo (vtkDataObject) : the output data object
        field (int) : the field type id
        vtkArray (vtkDataArray) : the data array to add to the output

    Return:
        vtkDataObject : the output data object with the data array added
    """
    # Point Data
    if field == 0:
        pdo.GetPointData().AddArray(vtkArray)
    # Cell Data:
    elif field == 1:
        pdo.GetCellData().AddArray(vtkArray)
    # Field Data:
    elif field == 2:
        pdo.GetFieldData().AddArray(vtkArray)
    # Row Data:
    elif field == 6:
        pdo.GetRowData().AddArray(vtkArray)
    else:
        raise _helpers.PVGeoError('Field association not defined. Try inputing Point, Cell, Field, or Row data.')
    return pdo

def _getData(pdi, field):
    """Gets data field from input vtkDataObject"""
    data = None
    try:
        # Point Data
        if field == 0:
            data = pdi.GetPointData()
        # Cell Data:
        elif field == 1:
            data = pdi.GetCellData()
        # Field Data:
        elif field == 2:
            data = pdi.GetFieldData()
        # Row Data:
        elif field == 6:
            data = pdi.GetRowData()
        else:
            raise _helpers.PVGeoError('Field association not defined. Try inputing Point, Cell, Field, or Row data.')
    except AttributeError:
        raise _helpers.PVGeoError('Input data does not have field type `%d`.' % field)
    return data


def getArray(pdi, field, name):
    """Gets an array from a vtkDataObject given its field association and name.

    Notes:
        - Point Data: 0
        - Cell Data: 1
        - Field Data: 2
        - Row Data: 6

    Args:
        pdi (vtkDataObject) : the input data object
        field (int) : the field type id
        name (str) : the data array name

    Return:
        vtkDataObject: the output data object
    """
    data = _getData(pdi, field)
    return data.GetArray(name)

# def GetDecimalPlaces(arr, barrier=6):
#     arr = np.array(arr.flatten(), dtype=str)
#     num = 0
#     for val in arr:
#         n = len(str(val).split('.')[1])
#         if n > num:
#             num = n
#     # Now do not let exceed barrier
#     if num > barrier: return barrier
#     return num


def SearchForArray(pdi, name):

    def _SearchField(field):
        data = _getData(pdi, field)
        for i in range(data.GetNumberOfArrays()):
            if data.GetArrayName(i) == name:
                return data.GetArray(i)
        return None

    fields = [0, 1, 2, 6]
    for field in fields:
        try:
            arr = _SearchField(field)
        except _helpers.PVGeoError:
            continue
        if arr is not None:
            # We found it!
            return arr, field

    raise _helpers.PVGeoError('Array `%s` not found in input data.' % name)
    return None
