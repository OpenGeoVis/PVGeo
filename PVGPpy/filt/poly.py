import vtk
from vtk.util import numpy_support as nps
import numpy as np
from vtk.numpy_interface import dataset_adapter as dsa


#---- Normalizations ----#
# Here are some privat functions to encompass the different normalizations
def _featureScaleNorm(arr):
    return (arr - np.min(arr)) / (np.max(arr) - np.min(arr))

def _standardScoreNorm(arr):
    return (arr - np.mean(arr)) / (np.std(arr))


# Here is the public function to call for the normalizations
def normalizeArray(pdi, info, norm, multiplyer=1.0, newName='', pdo=None):
    """
    TODO: Descrption
    Perform normalize on a data array for any given VTK data object.

    Normalization Types:
        0 -> Feature Scale
        1 -> Standard Score

    """
    if pdo is None:
        pdo = vtk.vtkImageData()

    # Get input array name
    name = info.Get(vtk.vtkDataObject.FIELD_NAME())
    field = info.Get(vtk.vtkDataObject.FIELD_ASSOCIATION())

    wpdi = dsa.WrapDataObject(pdi)

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

    arr = np.array(arr)


    # Feature Scale
    if norm == 0:
        print('fs')
        arr = _featureScaleNorm(arr)
    # Standard Score
    elif norm == 1:
        arr = _standardScoreNorm(arr)
    else:
        raise Exception('Normalization %d is not implemented' % norm)

    # Apply the multiplyer
    arr *= multiplyer

    c = nps.numpy_to_vtk(num_array=arr,deep=True)

    # If no name given for data by user, use the basename of the file
    if newName == '':
        newName = 'Normalized ' + name
    c.SetName(newName)

    pdo.DeepCopy(pdi)

    # Point Data
    if field == 0:
        pdo.GetPointData().AddArray(c)
    # Cell Data:
    elif field == 1:
        pdo.GetCellData().AddArray(c)
    # Field Data:
    elif field == 2:
        pdo.GetFieldData().AddArray(c)
    # Row Data:
    elif field == 6:
        pdo.GetRowData().AddArray(c)
    else:
        raise Exception('Field association not defined. Try inputing Point, Cell, Field, or Row data.')

    return pdo
