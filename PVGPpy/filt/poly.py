import vtk
from vtk.util import numpy_support as nps
import numpy as np
from vtk.numpy_interface import dataset_adapter as dsa
from datetime import datetime


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
def normalizeArray(pdi, info, norm, multiplyer=1.0, newName='', pdo=None):
    """
    TODO: Descrption
    Perform normalize on a data array for any given VTK data object.

    Normalization Types:
        0 -> Feature Scale
        1 -> Standard Score
        2 -> Natural Log
        3 -> Log Base 10

    """
    if pdo is None:
        pdo = pdi.DeepCopy()

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



#---- Cell Connectivity ----#

def connectCells(pdi, cellType=4, nrNbr=True, pdo=None, logTime=False):
    # NOTE: Type map is specified in vtkCellType.h
    """
    <Entry value="4" text="Poly Line"/>
    <Entry value="3" text="Line"/>
    """
    if pdo is None:
        pdo = vtk.vtkImageData()

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
        pdo = vtk.vtkImageData()
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
        pdo = vtk.vtkImageData()

    numPoints = pdi.GetNumberOfPoints()

    # VTK_POLY_LINE is 4
    # Type map is specified in vtkCellType.h
    connectCells(pdi, cellType=4, nrNbr=nrNbr, pdo=pdo, logTime=logTime)

    # Make a tube from the PolyData line:
    _polyLineToTube(pdi, pdo, radius=radius, numSides=numSides)

    return pdo
