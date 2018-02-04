import vtk
from vtk.util import numpy_support as nps
import numpy as np
from vtk.numpy_interface import dataset_adapter as dsa
from datetime import datetime
# NOTE: internal import - from scipy.spatial import cKDTree

#---- Helpers ----#
def _getArray(wpdi, field, name):
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

def _addArray(pdo, field, vtkArray):
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

#---- Correlations ----#
def _corr(arr1, arr2):
    return np.correlate(arr1, arr2, mode='same')


def correlateArrays(pdi, info1, info2, multiplyer=1.0, newName='', pdo=None):
    # TODO make arguments pass names not info
    if pdo is None:
        # TODO: test this
        pdo = pdi.DeepCopy()

    # Get input array names
    name1 = info1.Get(vtk.vtkDataObject.FIELD_NAME())
    name2 = info2.Get(vtk.vtkDataObject.FIELD_NAME())
    # Get field associations
    field1 = info1.Get(vtk.vtkDataObject.FIELD_ASSOCIATION())
    field2 = info2.Get(vtk.vtkDataObject.FIELD_ASSOCIATION())
    # Get the input arrays
    wpdi = dsa.WrapDataObject(pdi)
    arr1 = _getArray(wpdi, field1, name1)
    arr2 = _getArray(wpdi, field2, name2)
    # Perform correlations
    carr = _corr(arr1, arr2)
    # Apply the multiplyer
    carr *= multiplyer
    # Convert to a VTK array
    c = nps.numpy_to_vtk(num_array=carr,deep=True)
    # If no name given for data by user, use operator name
    if newName == '':
        newName = 'Correlated'
    c.SetName(newName)
    # Build output
    pdo.DeepCopy(pdi)
    pdo = _addArray(pdo, field, c)
    return pdo

#---- Normalizations ----#
# Here are some private functions to encompass the different normalizations
def _featureScaleNorm(arr):
    return (arr - np.min(arr)) / (np.max(arr) - np.min(arr))

def _standardScoreNorm(arr):
    return (arr - np.mean(arr)) / (np.std(arr))

def _log10Norm(arr):
    return np.log10(arr)

def _logNatNorm(arr):
    return np.log(arr)


# Here is the public function to call for the normalizations
def normalizeArray(pdi, info, norm, multiplyer=1.0, newName='', pdo=None, abs=False):
    """
    TODO: Descrption
    Perform normalize on a data array for any given VTK data object.
    `abs` will take the absolute value before the normalization

    Normalization Types:
        0 -> Feature Scale
        1 -> Standard Score
        2 -> Natural Log
        3 -> Log Base 10

    """
    if pdo is None:
        # TODO: test this
        pdo = pdi.DeepCopy()

    # Get input array name
    name = info.Get(vtk.vtkDataObject.FIELD_NAME())
    # Get field assocaition
    field = info.Get(vtk.vtkDataObject.FIELD_ASSOCIATION())
    # Get inout array
    wpdi = dsa.WrapDataObject(pdi)
    arr = _getArray(wpdi, field, name)
    arr = np.array(arr)
    # Take absolute value?
    if abs:
        arr = np.abs(arr)
    # Perform normalization scheme
    # Feature Scale
    if norm == 0:
        arr = _featureScaleNorm(arr)
    # Standard Score
    elif norm == 1:
        arr = _standardScoreNorm(arr)
    elif norm == 2:
        arr = _logNatNorm(arr)
    elif norm == 3:
        arr = _log10Norm(arr)
    else:
        raise Exception('Normalization %d is not implemented' % norm)

    # Apply the multiplyer
    arr *= multiplyer
    # Convert to VTK array
    c = nps.numpy_to_vtk(num_array=arr,deep=True)
    # If no name given for data by user, use operator name
    if newName == '' or newName == 'Normalized':
        newName = 'Normalized ' + name
    c.SetName(newName)
    # Build output
    pdo.DeepCopy(pdi)
    pdo = _addArray(pdo, field, c)
    return pdo



#---- Cell Connectivity ----#

def connectCells(pdi, cellType=4, nrNbr=True, pdo=None, logTime=False):
    # NOTE: Type map is specified in vtkCellType.h
    """
    <Entry value="4" text="Poly Line"/>
    <Entry value="3" text="Line"/>
    """
    if pdo is None:
        pdo = vtk.vtkPolyData()

    if logTime:
        startTime = datetime.now()

    # Get the Points over the NumPy interface
    wpdi = dsa.WrapDataObject(pdi) # NumPy wrapped input
    points = np.array(wpdi.Points) # New NumPy array of poins so we dont destroy input

    pdo.DeepCopy(pdi)
    numPoints = pdi.GetNumberOfPoints()

    if nrNbr:
        from scipy.spatial import cKDTree
        # VTK_Line
        if cellType == 3:
            sft = 0
            while(len(points) > 1):
                tree = cKDTree(points)
                # Get indices of k nearest points
                dist, ind = tree.query(points[0], k=2)
                ptsi = [ind[0]+sft, ind[1]+sft]
                pdo.InsertNextCell(cellType, 2, ptsi)
                points = np.delete(points, 0, 0) # Deletes first row
                del(tree)
                sft += 1
        # VTK_PolyLine
        elif cellType == 4:
            tree = cKDTree(points)
            dist, ptsi = tree.query(points[0], k=numPoints)
            pdo.InsertNextCell(cellType, numPoints, ptsi)
        else:
            raise Exception('Cell Type %d not ye implemented.' % cellType)
    else:
        # VTK_PolyLine
        if cellType == 4:
            ptsi = [i for i in range(numPoints)]
            pdo.InsertNextCell(cellType, numPoints, ptsi)
        # VTK_Line
        elif cellType == 3:
            for i in range(0, numPoints-1):
                ptsi = [i, i+1]
                pdo.InsertNextCell(cellType, 2, ptsi)
        else:
            raise Exception('Cell Type %d not ye implemented.' % cellType)

    if logTime:
        print((datetime.now() - startTime))

    return pdo

def _polyLineToTube(pdi, pdo, radius=10.0, numSides=20):
    """
    Takes points from a vtkPolyData with associated poly lines in cell data and builds a polygonal tube around that line with some specified radius and number of sides.
    """
    if pdo is None:
        pdo = vtk.vtkPolyData()
        pdo.DeepCopy(pdi)

    # Make a tube from the PolyData line:
    tube = vtk.vtkTubeFilter()
    tube.SetInputData(pdo)
    tube.SetRadius(radius)
    tube.SetNumberOfSides(numSides)
    tube.Update()
    pdo.ShallowCopy(tube.GetOutput())

    return pdo

def pointsToTube(pdi, radius=10.0, numSides=20, nrNbr=False, pdo=None, logTime=False):
    """
    TODO: Descrption
    """
    if pdo is None:
        pdo = vtk.vtkPolyData()

    numPoints = pdi.GetNumberOfPoints()

    # VTK_POLY_LINE is 4
    # Type map is specified in vtkCellType.h
    connectCells(pdi, cellType=4, nrNbr=nrNbr, pdo=pdo, logTime=logTime)

    # Make a tube from the PolyData line:
    _polyLineToTube(pdi, pdo, radius=radius, numSides=numSides)

    return pdo
