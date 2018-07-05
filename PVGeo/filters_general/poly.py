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
from ..base import PVGeoAlgorithmBase, FilterPreserveTypeBase
from .. import _helpers
# NOTE: internal import - from scipy.spatial import cKDTree



###############################################################################

#---- ArrayMath ----#
class ArrayMath(FilterPreserveTypeBase):
    """This filter allows the user to select two input data array on which to perfrom math operations."""
    def __init__(self):
        FilterPreserveTypeBase.__init__(self)
        # Parameters:
        self.__multiplier = 1.0
        self.__newName = 'Mathed Up'
        self.__inputArray1 = [None, None]
        self.__inputArray2 = [None, None]
        self.__operation = ArrayMath._add


    @staticmethod
    def _correlate(arr1, arr2):
        """Use `np.correlate()` on `mode=\'same\'` on two selected arrays from one input."""
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
        ops = dict(
            Add=ArrayMath._add,
            Subtract=ArrayMath._subtract,
            Multiply=ArrayMath._multiply,
            Divide=ArrayMath._divide,
            Correlate=ArrayMath._correlate,
        )
        return ops

    @staticmethod
    def GetOperationNames():
        ops = ArrayMath.GetOperations()
        return list(ops.keys())

    @staticmethod
    def GetOperation(idx):
        n = ArrayMath.GetOperationNames()[idx]
        return ArrayMath.GetOperations()[n]


    def _MathUp(self, pdi, pdo):
        """Make sure to pass array names and integer associated fields.
        Use helpers to get these properties."""
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
        if idx == 0:
            self._SetInputArray1(field, name)
        elif idx == 1:
            self._SetInputArray2(field, name)
        else:
            raise RuntimeError('SetInputArrayToProcess() do not know how to handle idx: %d' % idx)
        return 1

    def SetMultiplier(self, val):
        """This is a static shifter/scale factor across the array after normalization."""
        if self.__multiplier != val:
            self.__multiplier = val
            self.Modified()

    def GetMultiplier(self):
        return self.__multiplier

    def SetNewArrayName(self, name):
        """Give the new normalized array a meaningful name."""
        if self.__newName != name:
            self.__newName = name
            self.Modified()

    def GetNewArrayName(self):
        return self.__newName

    def SetOperation(self, op):
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
    """
    def __init__(self):
        FilterPreserveTypeBase.__init__(self)
        # Parameters:
        self.__multiplier = 1.0
        self.__newName = 'Normalized'
        self.__absolute = False
        self.__inputArray = [None, None]
        self.__normalization = NormalizeArray._featureScale
        #self.__range = None


    #### Array normalization methods ####


    @staticmethod
    def _passArray(arr):
        return arr

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
    def GetOperations():
        ops = dict(
            Feature_Scale=NormalizeArray._featureScale,
            Standard_Score=NormalizeArray._standardScore,
            Log10=NormalizeArray._log10,
            Natural_Log=NormalizeArray._logNat,
            Just_Multiply=NormalizeArray._passArray,
        )
        return ops

    @staticmethod
    def GetOperationNames():
        ops = NormalizeArray.GetOperations()
        return list(ops.keys())

    @staticmethod
    def GetOperation(idx):
        n = NormalizeArray.GetOperationNames()[idx]
        return NormalizeArray.GetOperations()[n]

    @staticmethod
    def GetArrayRange(pdi, field, name):
        wpdi = dsa.WrapDataObject(pdi)
        arr = _helpers.getArray(wpdi, field, name)
        arr = np.array(arr)
        return (np.min(arr), np.max(arr))


    def _Normalize(self, pdi, pdo):
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
        # Get inout array
        field, name = self.__inputArray[0], self.__inputArray[1]
        #self.__range = NormalizeArray.GetArrayRange(pdi, field, name)
        wpdi = dsa.WrapDataObject(pdi)
        arr = _helpers.getArray(wpdi, field, name)
        arr = np.array(arr)
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
        if newName == '' or newName == 'Normalized':
            newName = 'Normalized ' + name
        c.SetName(newName)
        # Build output
        pdo.DeepCopy(pdi)
        pdo = _helpers.addArray(pdo, field, c)
        return pdo

    #### Algorithm Methods ####


    def RequestData(self, request, inInfo, outInfo):
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        pdo = self.GetOutputData(outInfo, 0)
        # Perfrom task
        self._Normalize(pdi, pdo)
        return 1

    #### Seters and Geters ####


    def SetInputArrayToProcess(self, idx, port, connection, field, name):
        if self.__inputArray[0] != field:
            self.__inputArray[0] = field
            self.Modified()
        if self.__inputArray[1] != name:
            self.__inputArray[1] = name
            self.Modified()
        return 1

    def SetMultiplier(self, val):
        """This is a static shifter/scale factor across the array after normalization."""
        if self.__multiplier != val:
            self.__multiplier = val
            self.Modified()


    def GetMultiplier(self):
        return self.__multiplier


    def SetNewArrayName(self, name):
        """Give the new normalized array a meaningful name."""
        if self.__newName != name:
            self.__newName = name
            self.Modified()


    def GetNewArrayName(self):
        return self.__newName

    def SetTakeAbsoluteValue(self, flag):
        """This will take the absolute value of the array before normalization."""
        if self.__absolute != flag:
            self.__absolute = flag
            self.Modified()

    def SetNormalization(self, norm):
        if isinstance(norm, str):
            norm = NormalizeArray.GetOperations()[norm]
        elif isinstance(norm, int):
            norm = NormalizeArray.GetOperation(norm)
        if self.__normalization != norm:
            self.__normalization = norm
            self.Modified()



###############################################################################
#---- Cell Connectivity ----#

class AddCellConnToPoints(PVGeoAlgorithmBase):
    """This filter will add linear cell connectivity between scattered points. You have the option to add VTK_Line or VTK_PolyLine connectivity. VTK_Line connectivity makes a straight line between the points in order (either in the order by index or using a nearest neighbor calculation). The VTK_PolyLine adds a poly line connectivity between all points as one spline (either in the order by index or using a nearest neighbor calculation)."""
    def __init__(self):
        PVGeoAlgorithmBase.__init__(self,
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




###############################################################################


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



###############################################################################
