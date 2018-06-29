__all__ = [
    'ReshapeTable',
    'correlateArrays',
    'getArrayRange',
    'normalizeArray',
    'AddCellConnToPoints',
    'PointsToTube',
    'CombineTables'
]

import vtk
from vtk.util import numpy_support as nps
import numpy as np
from vtk.numpy_interface import dataset_adapter as dsa
from datetime import datetime
# Import Helpers:
from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase
from .. import _helpers
# NOTE: internal import - from scipy.spatial import cKDTree



#---- Reshape Table ----#

class ReshapeTable(VTKPythonAlgorithmBase):
    """This filter will take a vtkTable object and reshape it. This filter essentially treats vtkTables as 2D matrices and reshapes them using numpy.reshape in a C contiguous manner. Unfortunately, data fields will be renamed arbitrarily because VTK data arrays require a name."""
    def __init__(self):
        VTKPythonAlgorithmBase.__init__(self,
            nInputPorts=1, inputType='vtkTable',
            nOutputPorts=1, outputType='vtkTable')
        # Parameters
        self.__nrows = 4
        self.__ncols = False
        self.__names = []
        self.__order = 'F'

    def _Reshape(self, pdi, pdo):
        """
        Todo Description
        """
        # Get number of columns
        cols = pdi.GetNumberOfColumns()
        # Get number of rows
        rows = pdi.GetColumn(0).GetNumberOfTuples()

        if len(self.__names) is not 0:
            num = len(self.__names)
            if num < self.__ncols:
                for i in range(num, self.__ncols):
                    self.__names.append('Field %d' % i)
            elif num > self.__ncols:
                raise Exception('Too many array names. `ncols` specified as %d and %d names given.' % (self.__ncols, num))
        else:
            self.__names = ['Field %d' % i for i in range(self.__ncols)]

        # Make a 2D numpy array and fill with data from input table
        data = np.empty((cols,rows))
        for i in range(cols):
            c = pdi.GetColumn(i)
            data[i] = nps.vtk_to_numpy(c)

        if ((self.__ncols*self.__nrows) != (cols*rows)):
            raise Exception('Total number of elements must remain %d. Check reshape dimensions.' % (cols*rows))

        # Use numpy.reshape() to reshape data NOTE: only 2D because its a table
        # NOTE: column access of this reshape is not contigous
        data = np.array(np.reshape(data, (self.__nrows,self.__ncols), order=self.__order))
        pdo.SetNumberOfRows(self.__nrows)

        # Add new array to output table and assign incremental names (e.g. Field0)
        for i in range(self.__ncols):
            # Make a contigous array from the column we want
            col = np.array(data[:,i])
            # allow type to be determined by input
            insert = nps.numpy_to_vtk(num_array=col, deep=True) # array_type=vtk.VTK_FLOAT
            # VTK arrays need a name. Set arbitrarily
            insert.SetName(self.__names[i])
            #pdo.AddColumn(insert) # these are not getting added to the output table
            # ... work around:
            pdo.GetRowData().AddArray(insert) # NOTE: this is in the FieldData

        return pdo

    def RequestData(self, request, inInfo, outInfo):
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        pdo = self.GetOutputData(outInfo, 0)
        # Perfrom task
        self._Reshape(pdi, pdo)
        return 1


    #### Seters and Geters ####

    def SetNames(self, names):
        """Set names using a semicolon (;) seperated list"""
        # parse the names (a semicolon seperated list of names)
        names = names.split(';')
        if self.__names != names:
            self.__names = names
            self.Modified()

    def AddName(self, name):
        """Use to append a name to the names list"""
        self.__names.append(name)
        self.Modified()

    def GetNames(self):
        return self.__names

    def SetNumberOfColumns(self, ncols):
        if self.__ncols != ncols:
            self.__ncols = ncols
            self.Modified()

    def SetNumberOfRows(self, nrows):
        if self.__nrows != nrows:
            self.__nrows = nrows
            self.Modified()

    def SetOrder(self, order):
        if self.__order != order:
            self.__order = order
            self.Modified()


#---- Correlations ----#
def _corr(arr1, arr2):
    return np.correlate(arr1, arr2, mode='same')

def _mult(arr1, arr2):
    return arr1*arr2


def correlateArrays(pdi, arr1, arr2, multiplier=1.0, newName='', pdo=None):
    """Make sure to pass array names and integer associated fields.
    Use helpers to get these properties."""
    if pdo is None:
        # TODO: test this
        pdo = pdi.DeepCopy()
    # Get the input arrays
    (name1, field1) = arr1[0], arr1[1]
    (name2, field2) = arr2[0], arr2[1]
    wpdi = dsa.WrapDataObject(pdi)
    arr1 = _helpers.getArray(wpdi, field1, name1)
    arr2 = _helpers.getArray(wpdi, field2, name2)
    # Perform correlations
    #carr = _corr(arr1, arr2)
    # TODO
    carr = _mult(arr1, arr2)
    # Apply the multiplier
    carr *= multiplier
    # Convert to a VTK array
    c = nps.numpy_to_vtk(num_array=carr,deep=True)
    # If no name given for data by user, use operator name
    if newName == '':
        newName = 'Correlated'
    c.SetName(newName)
    # Build output
    pdo.DeepCopy(pdi)
    pdo = _helpers.addArray(pdo, field1, c)
    return pdo

#---- Normalizations ----#
# Here are some private functions to encompass the different normalizations
def _featureScaleNorm(arr, rng=None):
    if rng is not None:
        mi = rng[0]
        ma = rng[1]
    else:
        mi = np.min(arr)
        ma = np.max(arr)
    return (arr - mi) / (ma - mi)

def _standardScoreNorm(arr):
    return (arr - np.mean(arr)) / (np.std(arr))

def _log10Norm(arr):
    return np.log10(arr)

def _logNatNorm(arr):
    return np.log(arr)

def getArrayRange(pdi, arr):
    (name, field) = arr[0], arr[1]
    wpdi = dsa.WrapDataObject(pdi)
    arr = _helpers.getArray(wpdi, field, name)
    arr = np.array(arr)
    return [np.min(arr), np.max(arr)]


# Here is the public function to call for the normalizations
def normalizeArray(pdi, arr, norm, multiplier=1.0, newName='', pdo=None, abs=False, rng=None):
    """
    TODO: Descrption
    Perform normalize on a data array for any given VTK data object.
    `abs` will take the absolute value before the normalization

    Normalization Types:
        0 -> Feature Scale
        1 -> Standard Score
        2 -> Natural Log
        3 -> Log Base 10
        4 -> Simple Multiply by Multiplier

    """
    if pdo is None:
        # TODO: test this
        pdo = pdi.DeepCopy()

    # Get inout array
    (name, field) = arr[0], arr[1]
    wpdi = dsa.WrapDataObject(pdi)
    arr = _helpers.getArray(wpdi, field, name)
    arr = np.array(arr)
    # Take absolute value?
    if abs:
        arr = np.abs(arr)
    # Perform normalization scheme
    if norm == 0:
        # Feature Scale
        arr = _featureScaleNorm(arr, rng)
    elif norm == 1:
        # Standard Score
        arr = _standardScoreNorm(arr)
    elif norm == 2:
        # Natural Log
        arr = _logNatNorm(arr)
    elif norm == 3:
        # Log base 10
        arr = _log10Norm(arr)
    # Just multiply (option 4): no function call
    elif norm != 4:
        # Catch bad normalization call
        raise Exception('Normalization %d is not implemented' % norm)

    # Apply the multiplier
    arr *= multiplier
    # Convert to VTK array
    c = nps.numpy_to_vtk(num_array=arr,deep=True)
    # If no name given for data by user, use operator name
    if newName == '' or newName == 'Normalized':
        newName = 'Normalized ' + name
    c.SetName(newName)
    # Build output
    pdo.DeepCopy(pdi)
    pdo = _helpers.addArray(pdo, field, c)
    return pdo



#---- Cell Connectivity ----#

class AddCellConnToPoints(VTKPythonAlgorithmBase):
    """This filter will add linear cell connectivity between scattered points. You have the option to add VTK_Line or VTK_PolyLine connectivity. VTK_Line connectivity makes a straight line between the points in order (either in the order by index or using a nearest neighbor calculation). The VTK_PolyLine adds a poly line connectivity between all points as one spline (either in the order by index or using a nearest neighbor calculation)."""
    def __init__(self):
        VTKPythonAlgorithmBase.__init__(self,
            nInputPorts=1, inputType='vtkPolyData',
            nOutputPorts=1, outputType='vtkPolyData')
        # Parameters
        self.__cellType = 4
        self.__usenbr = False


    def _ConnectCells(self, pdi, pdo, logTime=False):
        # NOTE: Type map is specified in vtkCellType.h
        """
        <Entry value="4" text="Poly Line"/>
        <Entry value="3" text="Line"/>
        """
        cellType = self.__cellType
        nrNbr = self.__usenbr

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

    def RequestData(self, request, inInfo, outInfo):
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        pdo = self.GetOutputData(outInfo, 0)
        # Perfrom task
        self._ConnectCells(pdi, pdo)
        return 1


    #### Seters and Geters ####
    def SetCellType(self, cellType):
        if cellType != self.__cellType:
            self.__cellType = cellType
            self.Modified()

    def SetUseNearestNbr(self, flag):
        """A flag on whether to use SciPy's cKDTree nearest neighbor algorithms to sort the points to before adding linear connectivity"""
        if flag != self.__usenbr:
            self.__usenbr = flag
            self.Modified()







class PointsToTube(AddCellConnToPoints):
    """Takes points from a vtkPolyData object and constructs a line of those points then builds a polygonal tube around that line with some specified radius and number of sides."""
    def __init__(self):
        AddCellConnToPoints.__init__(self)
        # Additional Parameters
        # NOTE: CellType should remain 4 for VTK_PolyLine connection
        self.__numSides = 20
        self.__radius = 10.0


    def _ConnectCells(self, pdi, pdo, logTime=False):
        """This uses the parent's _ConnectCells() to build a tub around"""
        AddCellConnToPoints._ConnectCells(self, pdi, pdo, logTime=logTime)
        tube = vtk.vtkTubeFilter()
        tube.SetInputData(pdo)
        tube.SetRadius(self.__radius)
        tube.SetNumberOfSides(self.__numSides)
        tube.Update()
        pdo.ShallowCopy(tube.GetOutput())
        return pdo


    #### Seters and Geters ####

    def SetRadius(self, radius):
        if self.__radius != radius:
            self.__radius = radius
            self.Modified()

    def SetNumberOfSides(self, num):
        if self.__numSides != num:
            self.__numSides = num
            self.Modified()






class CombineTables(VTKPythonAlgorithmBase):
    """Takes two tables and combines them if they have the same number of rows."""
    def __init__(self):
        VTKPythonAlgorithmBase.__init__(self,
            nInputPorts=2, inputType='vtkTable',
            nOutputPorts=1, outputType='vtkTable')
        # Parameters... none

    # CRITICAL for multiple input ports
    def FillInputPortInformation(self, port, info):
        # all are tables so no need to check port
        info.Set(self.INPUT_REQUIRED_DATA_TYPE(), "vtkTable")
        return 1


    def RequestData(self, request, inInfo, outInfo):
        # Inputs from different ports:
        pdi0 = self.GetInputData(inInfo, 0, 0)
        pdi1 = self.GetInputData(inInfo, 1, 0)
        pdo = self.GetOutputData(outInfo, 0)

        pdo.DeepCopy(pdi0)

        # Get number of columns
        ncols1 = pdi1.GetNumberOfColumns()
        # Get number of rows
        nrows = pdi0.GetNumberOfRows()
        nrows1 = pdi1.GetNumberOfRows()
        assert(nrows == nrows1)

        for i in range(pdi1.GetRowData().GetNumberOfArrays()):
            arr = pdi1.GetRowData().GetArray(i)
            pdo.GetRowData().AddArray(arr)
        return 1
