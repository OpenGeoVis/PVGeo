__all__ = [
    'get_selected_array_name',
    'get_selected_array_field',
    'copy_arrays_to_point_data',
    'get_numpy_array',
    'get_vtk_array',
    'add_array',
    'get_selected_array',
    'search_for_array',
    'get_all_array_names',
]

import numpy as np
import vtk
from vtk.numpy_interface import dataset_adapter as dsa
from . import errors as _helpers


def get_selected_array_name(algorithm, idx):
    """Gets the name of the input array for a given index on a VTK algorithm

    Args:
        algorithm (vtkAlgorithm): A vtkAlgorithm class instantiation
        idx (int): the input array index

    Return:
        str : the name of the input array for the given index
    """
    info = algorithm.GetInputArrayInformation(idx)
    return info.Get(vtk.vtkDataObject.FIELD_NAME())


def get_selected_array_field(algorithm, idx):
    """Gets the field of the input array for a given index on a VTK algorithm

    Args:
        algorithm (vtkAlgorithm) : A vtkAlgorithm class instantiation
        idx (int) : the input array index

    Return:
        int : the field type of the input array for the given index
    """
    info = algorithm.GetInputArrayInformation(idx)
    return info.Get(vtk.vtkDataObject.FIELD_ASSOCIATION())


def get_field_id_by_name(field):
    """Get the field ID by name."""
    fields = dict(
        point=0,
        pt=0,
        p=0,
        cell=1,
        c=1,
        field=2,
        f=2,
        row=6,
        r=6,
    )
    field = field.lower()
    try:
        return fields[field]
    except KeyError:
        raise _helpers.PVGeoError('Field association not defined. Try inputing `point`, `cell`, `field`, or `row`.')



def copy_arrays_to_point_data(pdi, pdo, field):
    """Copys arrays from an input to an ouput's point data.

    Args:
        pdi (vtkDataObject) : The input data object to copy from
        pdo (vtkDataObject) : The output data object to copy over to
        field (int or str) : the field type id or name

    Return:
        vtkDataObject : returns the output data object parameter
    """
    if isinstance(field, str):
        field = get_field_id_by_name(field)
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
        raise _helpers.PVGeoError('Field association ({}) not defined. Try inputing Point, Cell, Field, or Row data.'.format(field))

    # Field Data
    return pdo


def get_numpy_array(wpdi, field, name):
    """Grabs an array from vtkDataObject given its name and field association.

    Args:
        wpdi  (wrapped vtkDataObject) : the input data object wrapped using
            vtk dataset adapter
        field (int or str) : the field type id or name
        name (str) : the name of the input array for the given index

    Return:
        numpy.array : a wrapped ``vtkDataArray`` for NumPy
    """
    if isinstance(field, str):
        field = get_field_id_by_name(field)
    if not isinstance(wpdi, vtk.numpy_interface.dataset_adapter.DataObject):
        wpdi = dsa.WrapDataObject(wpdi)
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
        raise _helpers.PVGeoError('Field association ({}) not defined. Try inputing Point, Cell, Field, or Row data.'.format(field))
    return arr

def get_vtk_array(pdi, field, name):
    """Grabs an array from vtkDataObject given its name and field association.

    Args:
        pdi  (vtkDataObject) : the input data object
        field (int or str) : the field type id or name
        name (str) : the name of the input array for the given index

    Return:
        vtkDataArray : the array from input field and name
    """
    if isinstance(field, str):
        field = get_field_id_by_name(field)
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
        raise _helpers.PVGeoError('Field association ({}) not defined. Try inputing Point, Cell, Field, or Row data.'.format(field))
    return arr


def get_selected_array(algorithm, wpdi, idx):
    """Gets selectected array at index idx wrapped for NumPy

    Args:
        algorithm (vtkAlgorithm) : A vtkAlgorithm class instantiation
        wpdi (wrapped vtkDataObject) : the input data object wrapped using vtk
            dataset adapter
        idx (int) : the input array index

    Return:
        numpy.array : a wrapped ``vtkDataArray`` for NumPy
    """
    name = get_selected_array_name(algorithm, idx)
    field = get_selected_array_field(algorithm, idx)
    return get_array(wpdi, field, name)

def add_array(pdo, field, vtkArray):
    """Adds an array to a vtkDataObject given its field association.

    Args:
        pdo (vtkDataObject) : the output data object
        field (int or str) : the field type id or name
        vtkArray (vtkDataArray) : the data array to add to the output

    Return:
        vtkDataObject : the output data object with the data array added
    """
    if isinstance(field, str):
        field = get_field_id_by_name(field)
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
        raise _helpers.PVGeoError('Field association ({}) not defined. Try inputing Point, Cell, Field, or Row data.'.format(field))
    return pdo

def _get_data(pdi, field):
    """Gets data field from input vtkDataObject"""
    data = None
    if isinstance(field, str):
        field = get_field_id_by_name(field)
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
            raise _helpers.PVGeoError('Field association ({}) not defined. Try inputing Point, Cell, Field, or Row data.'.format(field))
    except AttributeError:
        raise _helpers.PVGeoError('Input data does not have field type `{}`.'.format(field))
    return data


def get_array(pdi, field, name):
    """Gets an array from a vtkDataObject given its field association and name.

    Notes:
        - Point Data: 0
        - Cell Data: 1
        - Field Data: 2
        - Row Data: 6

    Args:
        pdi (vtkDataObject) : the input data object
        field (int or str) : the field type id or name
        name (str) : the data array name

    Return:
        vtkDataObject: the output data object
    """
    if isinstance(field, str):
        field = get_field_id_by_name(field)
    data = _get_data(pdi, field)
    return data.GetArray(name)


def search_for_array(pdi, name):

    def _search_field(field):
        data = _get_data(pdi, field)
        for i in range(data.GetNumberOfArrays()):
            if data.GetArrayName(i) == name:
                return data.GetArray(i)
        return None

    fields = [0, 1, 2, 6]
    for field in fields:
        try:
            arr = _search_field(field)
        except _helpers.PVGeoError:
            continue
        if arr is not None:
            # We found it!
            return arr, field

    raise _helpers.PVGeoError('Array `{}` not found in input data.'.format(name))
    return None


def get_all_array_names(dataset, field):
    if isinstance(field, str):
        field = get_field_id_by_name(field)
    if not isinstance(dataset, vtk.numpy_interface.dataset_adapter.DataObject):
        wpdi = dsa.WrapDataObject(dataset)
    else:
        wpdi = dataset
    # Point Data
    if field == 0:
        return wpdi.PointData.keys()
    # Cell Data:
    elif field == 1:
        return wpdi.CellData.keys()
    # Field Data:
    elif field == 2:
        return wpdi.FieldData.keys()
    # Row Data:
    elif field == 6:
        return wpdi.RowData.keys()
    else:
        raise _helpers.PVGeoError('Field association ({}) not defined. Try inputing Point, Cell, Field, or Row data.'.format(field))
    return None
