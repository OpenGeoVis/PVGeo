__all__ = [
    'ArrayMath',
    'NormalizeArray',
    'AddCellConnToPoints',
    'PointsToTube',
]

import vtk
from vtk.util import numpy_support as nps
import numpy as np
from vtk.numpy_interface import dataset_adapter as dsa
from datetime import datetime
# Import Helpers:
from ..base import FilterBase, FilterPreserveTypeBase
from .. import _helpers
# NOTE: internal import - from scipy.spatial import cKDTree



###############################################################################

#---- ArrayMath ----#
class ArrayMath(FilterPreserveTypeBase):
    """This filter allows the user to select two input data arrays on which to perfrom math operations. The input arrays are used in their order of selection for the operations.

    **Available Math Operations:**

    - `add`: This adds the two data arrays together
    - `subtract`: This subtracts input array 2 from input array 1
    - `multiply`: Multiplies the two data arrays together
    - `divide`: Divide input array 1 by input array 2 (arr1/arr2)
    - `correlate`: Use `np.correlate(arr1, arr2, mode='same')`
    """
    __displayname__ = 'Array Math'
    __type__ = 'filter'
    def __init__(self, **kwargs):
        FilterPreserveTypeBase.__init__(self)
        # Parameters:
        self.__multiplier = kwargs.get('multiplier', 1.0)
        self.__newName = kwargs.get('newName', 'Mathed Up')
        self.__inputArray1 = [None, None]
        self.__inputArray2 = [None, None]
        # Convert operation to callable method
        op = kwargs.get('operation', 'add')
        if isinstance(op, (str, int)):
            op = self.GetOperation(op)
        self.__operation = op


    @staticmethod
    def _correlate(arr1, arr2):
        """Use ``np.correlate()`` on ``mode='same'`` on two selected arrays from one input.
        """
        return np.correlate(arr1, arr2, mode='same')

    @staticmethod
    def _multiply(arr1, arr2):
        return arr1*arr2

    @staticmethod
    def _divide(arr1, arr2):
        return arr1/arr2

    @staticmethod
    def _add(arr1, arr2):
        return arr1+arr2

    @staticmethod
    def _subtract(arr1, arr2):
        return arr1-arr2

    @staticmethod
    def GetOperations():
        """Returns the math operation methods as callable objects in a dictionary
        """
        ops = dict(
            add=ArrayMath._add,
            subtract=ArrayMath._subtract,
            multiply=ArrayMath._multiply,
            divide=ArrayMath._divide,
            correlate=ArrayMath._correlate,
        )
        return ops

    @staticmethod
    def GetOperationNames():
        """Gets a list of the math operation keys

        Return:
            list(str): the keys for getting the math operations
        """
        ops = ArrayMath.GetOperations()
        return list(ops.keys())

    @staticmethod
    def GetOperation(idx):
        """Gets a math operation based on an index in the keys

        Return:
            callable: the math operation method
        """
        if isinstance(idx, str):
            return ArrayMath.GetOperations()[idx]
        n = ArrayMath.GetOperationNames()[idx]
        return ArrayMath.GetOperations()[n]


    def _MathUp(self, pdi, pdo):
        """Make sure to pass array names and integer associated fields.
        Use helpers to get these properties.
        """
        if pdo is None:
            # TODO: test this
            pdo = pdi.DeepCopy()
        # Get the input arrays
        field1, name1 = self.__inputArray1[0], self.__inputArray1[1]
        field2, name2 = self.__inputArray2[0], self.__inputArray2[1]
        wpdi = dsa.WrapDataObject(pdi)
        arr1 = _helpers.getArray(wpdi, field1, name1)
        arr2 = _helpers.getArray(wpdi, field2, name2)
        # Perform Math Operation
        carr = self.__operation(arr1, arr2)
        # Apply the multiplier
        carr *= self.__multiplier
        # Convert to a VTK array
        c = nps.numpy_to_vtk(num_array=carr,deep=True)
        # If no name given for data by user, use operator name
        newName = self.__newName
        if newName == '':
            newName = 'Mathed Up'
        c.SetName(newName)
        # Build output
        pdo.DeepCopy(pdi)
        pdo = _helpers.addArray(pdo, field1, c)
        return pdo


    #### Algorithm Methods ####


    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to perfrom operation and generate output
        """
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        pdo = self.GetOutputData(outInfo, 0)
        # Perfrom task
        self._MathUp(pdi, pdo)
        return 1


    #### Seters and Geters ####


    def _SetInputArray1(self, field, name):
        if self.__inputArray1[0] != field:
            self.__inputArray1[0] = field
            self.Modified()
        if self.__inputArray1[1] != name:
            self.__inputArray1[1] = name
            self.Modified()

    def _SetInputArray2(self, field, name):
        if self.__inputArray2[0] != field:
            self.__inputArray2[0] = field
            self.Modified()
        if self.__inputArray2[1] != name:
            self.__inputArray2[1] = name
            self.Modified()

    def SetInputArrayToProcess(self, idx, port, connection, field, name):
        """Used by pipeline/paraview GUI wrappings to set the input arrays
        """
        if idx == 0:
            self._SetInputArray1(field, name)
        elif idx == 1:
            self._SetInputArray2(field, name)
        else:
            raise _helpers.PVGeoError('SetInputArrayToProcess() do not know how to handle idx: %d' % idx)
        return 1

    def SetMultiplier(self, val):
        """This is a static shifter/scale factor across the array after normalization.
        """
        if self.__multiplier != val:
            self.__multiplier = val
            self.Modified()

    def GetMultiplier(self):
        """Return the set multiplier/scalar
        """
        return self.__multiplier

    def SetNewArrayName(self, name):
        """Give the new array a meaningful name.
        """
        if self.__newName != name:
            self.__newName = name
            self.Modified()

    def GetNewArrayName(self):
        return self.__newName

    def SetOperation(self, op):
        """Set the math operation to perform

        Args:
            op (str, int, or callable): The operation as a string key, int index, or callable method

        Note:
            This can accept a callable method to set a custom operation as long as its signature is: ``<callable>(arr1, arr2)``
        """
        if isinstance(op, str):
            op = ArrayMath.GetOperations()[op]
        elif isinstance(op, int):
            op = ArrayMath.GetOperation(op)
        if self.__operation != op:
            self.__operation = op
            self.Modified()



###############################################################################

#---- Normalizations ----#

class NormalizeArray(FilterPreserveTypeBase):
    """This filter allows the user to select an array from the input data set to be normalized. The filter will append another array to that data set for the output. The user can specify how they want to rename the array, can choose a multiplier, and can choose from several types of common normalizations (more functionality added as requested).

    **Normalization Types:**

    - `feature_scale`: Feature Scale
    - `standard_score`: tandard Score
    - `log10`: Natural Log
    - `natural_log`: Log Base 10
    - `just_multiply`: Only Multiply by Multiplier
    """
    __displayname__ = 'Normalize Array'
    __type__ = 'filter'
    def __init__(self, **kwargs):
        FilterPreserveTypeBase.__init__(self)
        # Parameters:
        self.__multiplier = kwargs.get('multiplier', 1.0)
        self.__newName = kwargs.get('newName', 'Normalized')
        self.__absolute = kwargs.get('absolute', False)
        self.__inputArray = [None, None]
        # Convert operation to callable method
        op = kwargs.get('normalization', 'feature_scale')
        if isinstance(op, (str, int)):
            op = self.GetNormalization(op)
        self.__normalization = op


    #### Array normalization methods ####


    @staticmethod
    def _passArray(arr):
        return np.array(arr)

    @staticmethod
    def _featureScale(arr):
        # TODO: implement ability to use custom range
        # if rng is not None:
        #     mi = rng[0]
        #     ma = rng[1]
        # else:
        mi = np.min(arr)
        ma = np.max(arr)
        return (arr - mi) / (ma - mi)

    @staticmethod
    def _standardScore(arr):
        return (arr - np.mean(arr)) / (np.std(arr))

    @staticmethod
    def _log10(arr):
        return np.log10(arr)

    @staticmethod
    def _logNat(arr):
        return np.log(arr)

    @staticmethod
    def GetNormalizations():
        """All Available normalizations

        Return:
            dict: dictionary of callable methods for normalizing an array
        """
        ops = dict(
            feature_scale=NormalizeArray._featureScale,
            standard_score=NormalizeArray._standardScore,
            log10=NormalizeArray._log10,
            natural_log=NormalizeArray._logNat,
            just_multiply=NormalizeArray._passArray,
        )
        return ops

    @staticmethod
    def GetNormalizationNames():
        """Gets a list of the normalization keys

        Return:
            list(str): the keys for getting the normalizations
        """
        ops = NormalizeArray.GetNormalizations()
        return list(ops.keys())

    @staticmethod
    def GetNormalization(idx):
        """Gets a normalization based on an index in the keys

        Return:
            callable: the normalization method
        """
        if isinstance(idx, str):
            return NormalizeArray.GetNormalizations()[idx]
        n = NormalizeArray.GetNormalizationNames()[idx]
        return NormalizeArray.GetNormalizations()[n]

    @staticmethod
    def GetArrayRange(pdi, field, name):
        """Returns a tuple of the range for a ``vtkDataArray`` on a ``vtkDataObject``
        """
        wpdi = dsa.WrapDataObject(pdi)
        arr = _helpers.getArray(wpdi, field, name)
        arr = np.array(arr)
        return (np.min(arr), np.max(arr))


    def _Normalize(self, pdi, pdo):
        """Perform normalize on a data array for any given VTK data object.
        """
        # Get inout array
        field, name = self.__inputArray[0], self.__inputArray[1]
        #self.__range = NormalizeArray.GetArrayRange(pdi, field, name)
        wpdi = dsa.WrapDataObject(pdi)
        arr = _helpers.getArray(wpdi, field, name)
        arr = np.array(arr, dtype=float)
        # Take absolute value?
        if self.__absolute:
            arr = np.abs(arr)
        # Perform normalization scheme
        arr = self.__normalization(arr)
        # Apply the multiplier
        arr *= self.__multiplier
        # Convert to VTK array
        c = nps.numpy_to_vtk(num_array=arr,deep=True)
        # If no name given for data by user, use operator name
        newName = self.__newName
        if newName == '':
            newName = 'Normalized ' + name
        c.SetName(newName)
        # Build output
        pdo.DeepCopy(pdi)
        pdo = _helpers.addArray(pdo, field, c)
        return pdo

    #### Algorithm Methods ####


    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output
        """
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        pdo = self.GetOutputData(outInfo, 0)
        # Perfrom task
        self._Normalize(pdi, pdo)
        return 1

    #### Seters and Geters ####


    def SetInputArrayToProcess(self, idx, port, connection, field, name):
        """Used by pipeline/paraview GUI wrappings to set the input arrays
        """
        if self.__inputArray[0] != field:
            self.__inputArray[0] = field
            self.Modified()
        if self.__inputArray[1] != name:
            self.__inputArray[1] = name
            self.Modified()
        return 1

    def SetMultiplier(self, val):
        """This is a static shifter/scale factor across the array after normalization.
        """
        if self.__multiplier != val:
            self.__multiplier = val
            self.Modified()


    def GetMultiplier(self):
        """Return the set multiplier/scalar
        """
        return self.__multiplier


    def SetNewArrayName(self, name):
        """Give the new array a meaningful name.
        """
        if self.__newName != name:
            self.__newName = name
            self.Modified()


    def GetNewArrayName(self):
        return self.__newName

    def SetTakeAbsoluteValue(self, flag):
        """This will take the absolute value of the array before normalization.
        """
        if self.__absolute != flag:
            self.__absolute = flag
            self.Modified()

    def SetNormalization(self, norm):
        """Set the normalization operation to perform

        Args:
            norm (str, int, or callable): The operation as a string key, int index, or callable method

        Note:
            This can accept a callable method to set a custom operation as long as its signature is: ``<callable>(arr)``
        """
        if isinstance(norm, str):
            norm = NormalizeArray.GetNormalizations()[norm]
        elif isinstance(norm, int):
            norm = NormalizeArray.GetNormalization(norm)
        if self.__normalization != norm:
            self.__normalization = norm
            self.Modified()



###############################################################################
#---- Cell Connectivity ----#

class AddCellConnToPoints(FilterBase):
    """This filter will add linear cell connectivity between scattered points. You have the option to add ``VTK_Line`` or ``VTK_PolyLine`` connectivity. ``VTK_Line`` connectivity makes a straight line between the points in order (either in the order by index or using a nearest neighbor calculation). The ``VTK_PolyLine`` adds a poly line connectivity between all points as one spline (either in the order by index or using a nearest neighbor calculation). Type map is specified in `vtkCellType.h`.

    **Cell Connectivity Types:**

    - 4: Poly Line
    - 3: Line
    """
    __displayname__ = 'Add Cell Connectivity to Points'
    __type__ = 'filter'
    def __init__(self, **kwargs):
        FilterBase.__init__(self,
            nInputPorts=1, inputType='vtkPolyData',
            nOutputPorts=1, outputType='vtkPolyData')
        # Parameters
        self.__cellType = vtk.VTK_POLY_LINE
        self.__usenbr = kwargs.get('nearestNbr', False)


    def _ConnectCells(self, pdi, pdo, logTime=False):
        """Internal helper to perfrom the connection
        """
        # NOTE: Type map is specified in vtkCellType.h
        cellType = self.__cellType
        nrNbr = self.__usenbr

        if logTime:
            startTime = datetime.now()

        # Get the Points over the NumPy interface
        wpdi = dsa.WrapDataObject(pdi) # NumPy wrapped input
        points = np.array(wpdi.Points) # New NumPy array of poins so we dont destroy input

        def _makePolyCell(ptsi):
            cell = vtk.vtkPolyLine()
            cell.GetPointIds().SetNumberOfIds(len(ptsi))
            for i in ptsi:
                cell.GetPointIds().SetId(i, ptsi[i])
            return cell

        def _makeLineCell(ptsi):
            if len(ptsi) != 2:
                raise _helpers.PVGeoError('_makeLineCell() only handles two points')
            aLine = vtk.vtkLine()
            aLine.GetPointIds().SetId(0, ptsi[0])
            aLine.GetPointIds().SetId(1, ptsi[1])
            return aLine


        cells = vtk.vtkCellArray()
        numPoints = pdi.GetNumberOfPoints()
        if nrNbr:
            from scipy.spatial import cKDTree
            # VTK_Line
            if cellType == vtk.VTK_LINE:
                tree = cKDTree(points)
                ind = tree.query([0.0,0.0,0.0], k=numPoints)[1]
                for i in range(len(ind)-1):
                    # Get indices of k nearest points
                    ptsi = [ind[i], ind[i+1]]
                    cell = _makeLineCell(ptsi)
                    cells.InsertNextCell(cell)
                    points = np.delete(points, 0, 0) # Deletes first row
            # VTK_PolyLine
            elif cellType == vtk.VTK_POLY_LINE:
                tree = cKDTree(points)
                dist, ptsi = tree.query([0.0,0.0,0.0], k=numPoints)
                cell = _makePolyCell(ptsi)
                cells.InsertNextCell(cell)
            else:
                raise _helpers.PVGeoError('Cell Type %d not ye implemented.' % cellType)
        else:
            # VTK_PolyLine
            if cellType == vtk.VTK_POLY_LINE:
                ptsi = [i for i in range(numPoints)]
                cell = _makePolyCell(ptsi)
                cells.InsertNextCell(cell)
            # VTK_Line
            elif cellType == vtk.VTK_LINE:
                for i in range(0, numPoints-1):
                    ptsi = [i, i+1]
                    cell = _makeLineCell(ptsi)
                    cells.InsertNextCell(cell)
            else:
                raise _helpers.PVGeoError('Cell Type %d not ye implemented.' % cellType)

        if logTime:
            print((datetime.now() - startTime))
        # Now add points and cells to output
        pdo.SetPoints(pdi.GetPoints())
        pdo.SetLines(cells)
        # copy point data
        _helpers.copyArraysToPointData(pdi, pdo, 0) # 0 is point data
        return pdo

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output data object
        """
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        pdo = self.GetOutputData(outInfo, 0)
        # Perfrom task
        self._ConnectCells(pdi, pdo)
        return 1


    #### Seters and Geters ####


    def SetCellType(self, cellType):
        """Set the cell typ by the integer id as specified in `vtkCellType.h`
        """
        if cellType != self.__cellType:
            self.__cellType = cellType
            self.Modified()

    def SetUseNearestNbr(self, flag):
        """Set a flag on whether to use SciPy's ``cKDTree`` nearest neighbor algorithms to sort the points to before adding linear connectivity.
        """
        if flag != self.__usenbr:
            self.__usenbr = flag
            self.Modified()




###############################################################################


class PointsToTube(AddCellConnToPoints):
    """Takes points from a vtkPolyData object and constructs a line of those points then builds a polygonal tube around that line with some specified radius and number of sides.
    """
    __displayname__ = 'Points to Tube'
    __type__ = 'filter'
    def __init__(self, **kwargs):
        AddCellConnToPoints.__init__(self, **kwargs)
        # Additional Parameters
        # NOTE: CellType should remain vtk.VTK_POLY_LINE (4) connection
        self.__numSides = 20
        self.__radius = 10.0


    def _ConnectCells(self, pdi, pdo, logTime=False):
        """This uses the parent's ``_ConnectCells()`` to build a tub around
        """
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
        """Set the radius of the tube
        """
        if self.__radius != radius:
            self.__radius = radius
            self.Modified()

    def SetNumberOfSides(self, num):
        """Set the number of sides (resolution) for the tube
        """
        if self.__numSides != num:
            self.__numSides = num
            self.Modified()



###############################################################################
