__all__ = [
    'getSelectedArrayName',
    'getSelectedArrayField',
    'copyArraysToPointData',
    'getArray',
    'addArray',
    'getSelectedArray'
]

import vtk


def getSelectedArrayName(algorithm, idx):
    info = algorithm.GetInputArrayInformation(idx)
    return info.Get(vtk.vtkDataObject.FIELD_NAME())


def getSelectedArrayField(algorithm, idx):
    info = algorithm.GetInputArrayInformation(idx)
    return info.Get(vtk.vtkDataObject.FIELD_ASSOCIATION())


def copyArraysToPointData(pdi, pdo, field):
    """@desc: Copys arrays from an input to an ouput's point data."""
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
    # Point Data

    # Field Data
    return pdo


def getSelectedArray(algorithm, wpdi, idx):
    """@desc: gets selectected array ad index idx wrapped for NumPy"""
    name = getSelectedArrayName(algorithm, idx)
    field = getSelectedArrayField(algorithm, idx)
    return getArray(wpdi, field, name)


def getArray(wpdi, field, name):
    """
    @desc: Grabs an array from vtkDataObject given its name and field association.
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

def addArray(pdo, field, vtkArray):
    """
    @desc: Adds an array to a vtkDataObject given its field association.
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
