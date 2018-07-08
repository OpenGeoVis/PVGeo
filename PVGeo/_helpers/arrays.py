__all__ = [
    'numToVTK',
    'getSelectedArrayName',
    'getSelectedArrayField',
    'copyArraysToPointData',
    'getArray',
    'addArray',
    'getSelectedArray',
    #'GetDecimalPlaces',
]

import vtk
import numpy as np
from vtk.util import numpy_support as nps

def numToVTK(arr, name):
    """@desc: Converts a 1D numpy array to a VTK data array given a nameself.

    @params:
    arr : numpy array : A 1D numpy array
    name : string : the name of the data array for VTK

    @returns:
    vtkDataArray : a converted data array
    """
    c = nps.numpy_to_vtk(num_array=arr, deep=True)
    c.SetName(name)
    return c


def getSelectedArrayName(algorithm, idx):
    """@desc: Gets the name of the input array for a given index on a VTK algorithm

    @params:
    algorithm : vtkAlgorithm : A vtkAlgorithm class instantiation
    idx : int : the input array index

    @returns:
    string : the name of the input array for the given index
    """
    info = algorithm.GetInputArrayInformation(idx)
    return info.Get(vtk.vtkDataObject.FIELD_NAME())


def getSelectedArrayField(algorithm, idx):
    """@desc: Gets the field of the input array for a given index on a VTK algorithm

    @params:
    algorithm : vtkAlgorithm : A vtkAlgorithm class instantiation
    idx : int : the input array index

    @returns:
    int : the field type of the input array for the given index
    """
    info = algorithm.GetInputArrayInformation(idx)
    return info.Get(vtk.vtkDataObject.FIELD_ASSOCIATION())


def copyArraysToPointData(pdi, pdo, field):
    """@desc: Copys arrays from an input to an ouput's point data.

    @params:
    ido : vtkDataObject : The input data object to copy from
    odo : vtkDataObject : The output data object to copy over to
    field : int : the field type id

    @return:
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
        raise Exception('Field association not defined. Try inputing Point, Cell, Field, or Row data.')

    # Field Data
    return pdo


def getArray(wpdi, field, name):
    """
    @desc: Grabs an array from vtkDataObject given its name and field association.

    @params:
    wpdi : wrapped vtkDataObject : the input data object wrapped using vtk dataset adapter
    field : int : the field type id
    name: string : the name of the input array for the given index

    @return:
    numpy array : a wrapped vtkDataArray for NumPy
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
        raise Exception('Field association not defined. Try inputing Point, Cell, Field, or Row data.')
    return arr


def getSelectedArray(algorithm, wpdi, idx):
    """@desc: gets selectected array at index idx wrapped for NumPy

    @params:
    algorithm : vtkAlgorithm : A vtkAlgorithm class instantiation
    wpdi : wrapped vtkDataObject : the input data object wrapped using vtk dataset adapter
    idx : int : the input array index

    @return:
    numpy array : a wrapped vtkDataArray for NumPy
    """
    name = getSelectedArrayName(algorithm, idx)
    field = getSelectedArrayField(algorithm, idx)
    return getArray(wpdi, field, name)

def addArray(pdo, field, vtkArray):
    """@desc: Adds an array to a vtkDataObject given its field association.

    @params:
    pdo : vtkDataObject : the output data object
    field : int : the field type id
    vtkArray : vtkDataArray : the data array to add to the output

    @return:
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
        raise Exception('Field association not defined. Try inputing Point, Cell, Field, or Row data.')
    return pdo


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
