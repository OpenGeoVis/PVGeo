import vtk

def getSelectedArrayName(algorithm, idx):
    info = algorithm.GetInputArrayInformation(idx)
    return info.Get(vtk.vtkDataObject.FIELD_NAME())

def getSelectedArrayField(algorithm, idx):
    info = algorithm.GetInputArrayInformation(idx)
    return info.Get(vtk.vtkDataObject.FIELD_ASSOCIATION())

def getArray(wpdi, field, name):
    """
    Grabs an array from vtkDataObject given its name and field association
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
    Adds an array to a vtkDataObject given its field association
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
