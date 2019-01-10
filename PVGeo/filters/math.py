__all__ = [
    'ArrayMath',
    'NormalizeArray',
    'PercentThreshold',
    'ArraysToRGBA',
]

__displayname__ = 'Math Operations'

import numpy as np
import vtk
from vtk.numpy_interface import dataset_adapter as dsa

from .. import _helpers, interface
from ..base import FilterBase, FilterPreserveTypeBase



###############################################################################

#---- ArrayMath ----#
class ArrayMath(FilterPreserveTypeBase):
    """This filter allows the user to select two input data arrays on which to
    perfrom math operations. The input arrays are used in their order of
    selection for the operations.

    **Available Math Operations:**

    - `add`: This adds the two data arrays together
    - `subtract`: This subtracts input array 2 from input array 1
    - `multiply`: Multiplies the two data arrays together
    - `divide`: Divide input array 1 by input array 2 (arr1/arr2)
    - `correlate`: Use `np.correlate(arr1, arr2, mode='same')`
    """
    __displayname__ = 'Array Math'
    __category__ = 'filter'
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
        """Use ``np.correlate()`` on ``mode='same'`` on two selected arrays
        from one input.
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
        """Returns the math operation methods as callable objects in a
        dictionary
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
        arr1 = _helpers.getNumPyArray(wpdi, field1, name1)
        arr2 = _helpers.getNumPyArray(wpdi, field2, name2)
        # Perform Math Operation
        carr = self.__operation(arr1, arr2)
        # Apply the multiplier
        carr *= self.__multiplier
        # If no name given for data by user, use operator name
        newName = self.__newName
        if newName == '':
            newName = 'Mathed Up'
        # Convert to a VTK array
        c = interface.convertArray(carr, name=newName)
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
        """Used to set the input array(s)

        Args:
            idx (int): the index of the array to process
            port (int): input port (use 0 if unsure)
            connection (int): the connection on the port (use 0 if unsure)
            field (int): the array field (0 for points, 1 for cells, 2 for
                field, and 6 for row)
            name (int): the name of the array
        """
        if idx == 0:
            self._SetInputArray1(field, name)
        elif idx == 1:
            self._SetInputArray2(field, name)
        else:
            raise _helpers.PVGeoError('SetInputArrayToProcess() do not know how to handle idx: %d' % idx)
        return 1

    def Apply(self, inputDataObject, arrayName0, arrayName1):
        self.SetInputDataObject(inputDataObject)
        arr0, field0 = _helpers.searchForArray(inputDataObject, arrayName0)
        arr1, field1 = _helpers.searchForArray(inputDataObject, arrayName1)
        self.SetInputArrayToProcess(0, 0, 0, field0, arrayName0)
        self.SetInputArrayToProcess(1, 0, 0, field1, arrayName1)
        self.Update()
        return interface.wrapvtki(self.GetOutput())

    def SetMultiplier(self, val):
        """This is a static shifter/scale factor across the array after
        normalization.
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
            op (str, int, or callable): The operation as a string key, int
            index, or callable method

        Note:
            This can accept a callable method to set a custom operation as long
            as its signature is: ``<callable>(arr1, arr2)``
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
    """This filter allows the user to select an array from the input data set
    to be normalized. The filter will append another array to that data set for
    the output. The user can specify how they want to rename the array, can
    choose a multiplier, and can choose from several types of common
    normalizations (more functionality added as requested).

    **Normalization Types:**

    - `feature_scale`: Feature Scale
    - `standard_score`: tandard Score
    - `log10`: Natural Log
    - `natural_log`: Log Base 10
    - `just_multiply`: Only Multiply by Multiplier
    """
    __displayname__ = 'Normalize Array'
    __category__ = 'filter'
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
        self.__shift = 0.0


    #### Array normalization methods ####


    @staticmethod
    def _passArray(arr):
        return np.array(arr)

    @staticmethod
    def _featureScale(arr, rng=None):
        # TODO: implement ability to use custom range
        if rng is not None:
            mi = rng[0]
            ma = rng[1]
        else:
            mi = np.nanmin(arr)
            ma = np.nanmax(arr)
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
        """Returns a tuple of the range for a ``vtkDataArray`` on a
        ``vtkDataObject``.
        """
        wpdi = dsa.WrapDataObject(pdi)
        arr = _helpers.getNumPyArray(wpdi, field, name)
        arr = np.array(arr)
        return (np.nanmin(arr), np.nanmax(arr))


    def _Normalize(self, pdi, pdo):
        """Perform normalize on a data array for any given VTK data object.
        """
        # Get input array
        field, name = self.__inputArray[0], self.__inputArray[1]
        #self.__range = NormalizeArray.GetArrayRange(pdi, field, name)
        wpdi = dsa.WrapDataObject(pdi)
        arr = _helpers.getNumPyArray(wpdi, field, name)
        arr = np.array(arr, dtype=float)
        # Take absolute value?
        if self.__absolute:
            arr = np.abs(arr)
        arr += self.__shift
        # Perform normalization scheme
        arr = self.__normalization(arr)
        # Apply the multiplier
        arr *= self.__multiplier
        # If no name given for data by user, use operator name
        newName = self.__newName
        if newName == '':
            newName = 'Normalized ' + name
        # Convert to VTK array
        c = interface.convertArray(arr, name=newName)
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
        """Used to set the input array(s)

        Args:
            idx (int): the index of the array to process
            port (int): input port (use 0 if unsure)
            connection (int): the connection on the port (use 0 if unsure)
            field (int): the array field (0 for points, 1 for cells, 2 for
                field, and 6 for row)
            name (int): the name of the array
        """
        if self.__inputArray[0] != field:
            self.__inputArray[0] = field
            self.Modified()
        if self.__inputArray[1] != name:
            self.__inputArray[1] = name
            self.Modified()
        return 1

    def Apply(self, inputDataObject, arrayName):
        self.SetInputDataObject(inputDataObject)
        arr, field = _helpers.searchForArray(inputDataObject, arrayName)
        self.SetInputArrayToProcess(0, 0, 0, field, arrayName)
        self.Update()
        return interface.wrapvtki(self.GetOutput())

    def SetMultiplier(self, val):
        """This is a static shifter/scale factor across the array after
        normalization.
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
            norm (str, int, or callable): The operation as a string key, int
                index, or callable method

        Note:
            This can accept a callable method to set a custom operation as long
            as its signature is: ``<callable>(arr)``
        """
        if isinstance(norm, str):
            norm = NormalizeArray.GetNormalizations()[norm]
        elif isinstance(norm, int):
            norm = NormalizeArray.GetNormalization(norm)
        if self.__normalization != norm:
            self.__normalization = norm
            self.Modified()

    def SetShift(self, sft):
        """Set a static shifter to the input data array"""
        if self.__shift != sft:
            self.__shift = sft
            self.Modified()


###############################################################################


class PercentThreshold(FilterBase):
    """Allows user to select a percent of the data range to threshold.
    This will find the data range of the selected input array and remove the
    bottom percent. This can be reversed using the invert property.
    """
    __displayname__ = 'Percent Threshold'
    __category__ = 'filter'
    def __init__(self, percent=50, invert=False, **kwargs):
        FilterBase.__init__(self, inputType='vtkDataSet',
                            outputType='vtkUnstructuredGrid', **kwargs)
        self.__invert = invert
        if percent < 1.0: percent *= 100
        self.__percent = percent # NOTE: not decimal percent
        self.__filter = vtk.vtkThreshold()
        self.__inputArray = [None, None]


    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline for execution"""
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        self.__filter.SetInputDataObject(pdi)
        pdo = self.GetOutputData(outInfo, 0)
        # Get Input Array
        field, name = self.__inputArray[0], self.__inputArray[1]
        wpdi = dsa.WrapDataObject(pdi)
        arr = _helpers.getNumPyArray(wpdi, field, name)

        dmin, dmax = np.nanmin(arr), np.nanmax(arr)
        val = dmin + (self.__percent / 100.0) * (dmax - dmin)

        if self.__invert:
            self.__filter.ThresholdByLower(val)
        else:
            self.__filter.ThresholdByUpper(val)

        self.__filter.Update()

        filt = self.__filter.GetOutputDataObject(0)

        pdo.ShallowCopy(filt)
        return 1


    def SetInputArrayToProcess(self, idx, port, connection, field, name):
        """Used to set the input array(s)

        Args:
            idx (int): the index of the array to process
            port (int): input port (use 0 if unsure)
            connection (int): the connection on the port (use 0 if unsure)
            field (int): the array field (0 for points, 1 for cells, 2 for
                field, and 6 for row)
            name (int): the name of the array
        """
        if self.__inputArray[0] != field or self.__inputArray[1] != name:
            self.__inputArray[0] = field
            self.__inputArray[1] = name
            self.__filter.SetInputArrayToProcess(idx, port, connection, field, name)
            self.Modified()
        return 1

    def SetPercent(self, percent):
        """Set the percent for the threshold in range (0, 100).
        Any values falling beneath the set percent of the total data range
        will be removed."""
        if self.__percent != percent:
            self.__percent = percent
            self.Modified()

    def SetUseContinuousCellRange(self, flag):
        """If this is on (default is off), we will use the continuous
        interval [minimum cell scalar, maxmimum cell scalar] to intersect
        the threshold bound , rather than the set of discrete scalar
        values from the vertices"""
        return self.__filter.SetUseContinuousCellRange(flag)

    def SetInvert(self, flag):
        """Use to invert the threshold filter"""
        if self.__invert != flag:
            self.__invert = flag
            self.Modified()


    def Apply(self, inputDataObject, arrayName):
        self.SetInputDataObject(inputDataObject)
        arr, field = _helpers.searchForArray(inputDataObject, arrayName)
        self.SetInputArrayToProcess(0, 0, 0, field, arrayName)
        self.Update()
        return interface.wrapvtki(self.GetOutput())

################################################################################

class ArraysToRGBA(FilterPreserveTypeBase):
    """Use arrays from input data object to set an RGBA array. Sets colors and
    transparencies.
    """
    __displayname__ = 'Arrays To RGBA'
    __category__ = 'filter'
    def __init__(self, **kwargs):
        FilterPreserveTypeBase.__init__(self, **kwargs)
        self.__use_trans = False
        self.__r_array = [None, None]
        self.__g_array = [None, None]
        self.__b_array = [None, None]
        self.__a_array = [None, None]
        self.__field = None
        self.__mask = -9999


    def _GetArrays(self, wpdi):
        # Get Red
        fieldr, name = self.__r_array[0], self.__r_array[1]
        rArr = _helpers.getNumPyArray(wpdi, fieldr, name)
        # Get Green
        fieldg, name = self.__g_array[0], self.__g_array[1]
        gArr = _helpers.getNumPyArray(wpdi, fieldg, name)
        # Get Blue
        fieldb, name = self.__b_array[0], self.__b_array[1]
        bArr = _helpers.getNumPyArray(wpdi, fieldb, name)
        # Get Trans
        fielda, name = self.__a_array[0], self.__a_array[1]
        aArr = _helpers.getNumPyArray(wpdi, fielda, name)
        if fieldr != fieldg != fieldb: # != fielda
            raise _helpers.PVGeoError('Data arrays must be of the same field.')
        self.__field = fieldr
        return rArr, gArr, bArr, aArr


    def _MaskArrays(self, rArr, gArr, bArr, aArr):
        rArr = np.ma.masked_where(rArr==self.__mask, rArr)
        gArr = np.ma.masked_where(gArr==self.__mask, gArr)
        bArr = np.ma.masked_where(bArr==self.__mask, bArr)
        aArr = np.ma.masked_where(aArr==self.__mask, aArr)
        return rArr, gArr, bArr, aArr


    def RequestData(self, request, inInfo, outInfo):
        """Execute on pipeline"""
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        wpdi = dsa.WrapDataObject(pdi)
        # Get number of points
        pdo = self.GetOutputData(outInfo, 0)

        # Get the arrays for the RGB values
        rArr, gArr, bArr, aArr = self._GetArrays(wpdi)
        rArr, gArr, bArr, aArr = self._MaskArrays(rArr, gArr, bArr, aArr)

        # normalize each color array bewteen 0 and 255
        rArr = NormalizeArray._featureScale(rArr, [0, 255])
        gArr = NormalizeArray._featureScale(gArr, [0, 255])
        bArr = NormalizeArray._featureScale(bArr, [0, 255])

        # Now concatenate the arrays
        if self.__use_trans:
            aArr = NormalizeArray._featureScale(aArr, [0, 255])
            col = np.array(np.c_[rArr, gArr, bArr, aArr], dtype=np.uint8)
        else:
            col = np.array(np.c_[rArr, gArr, bArr], dtype=np.uint8)
        colors = interface.convertArray(col, name='Colors')

        # Set the output
        pdo.DeepCopy(pdi)
        # Add new color array
        _helpers.addArray(pdo, self.__field, colors)
        return 1



    #### Seters and Geters ####

    def SetUseTransparency(self, flag):
        if self.__use_trans != flag:
            self.__use_trans = flag
            self.Modified()

    def SetMaskValue(self, val):
        if self.__mask != val:
            self.__mask = val
            self.Modified()

    def _SetInputArrayRed(self, field, name):
        if self.__r_array[0] != field:
            self.__r_array[0] = field
            self.Modified()
        if self.__r_array[1] != name:
            self.__r_array[1] = name
            self.Modified()

    def _SetInputArrayGreen(self, field, name):
        if self.__g_array[0] != field:
            self.__g_array[0] = field
            self.Modified()
        if self.__g_array[1] != name:
            self.__g_array[1] = name
            self.Modified()

    def _SetInputArrayBlue(self, field, name):
        if self.__b_array[0] != field:
            self.__b_array[0] = field
            self.Modified()
        if self.__b_array[1] != name:
            self.__b_array[1] = name
            self.Modified()

    def _SetInputArrayTrans(self, field, name):
        if self.__a_array[0] != field:
            self.__a_array[0] = field
            self.Modified()
        if self.__a_array[1] != name:
            self.__a_array[1] = name
            self.Modified()

    def SetInputArrayToProcess(self, idx, port, connection, field, name):
        """Used to set the input array(s)

        Args:
            idx (int): the index of the array to process
            port (int): input port (use 0 if unsure)
            connection (int): the connection on the port (use 0 if unsure)
            field (int): the array field (0 for points, 1 for cells, 2 for
                field, and 6 for row)
            name (int): the name of the array
        """
        if idx == 0:
            self._SetInputArrayRed(field, name)
        elif idx == 1:
            self._SetInputArrayGreen(field, name)
        elif idx == 2:
            self._SetInputArrayBlue(field, name)
        elif idx == 3:
            self._SetInputArrayTrans(field, name)
        else:
            raise _helpers.PVGeoError('SetInputArrayToProcess() do not know how to handle idx: %d' % idx)
        return 1

    def Apply(self, inputDataObject, rArray, gArray, bArray, aArray=None):
        self.SetInputDataObject(inputDataObject)
        rArr, rField = _helpers.searchForArray(inputDataObject, rArray)
        gArr, gField = _helpers.searchForArray(inputDataObject, gArray)
        bArr, bField = _helpers.searchForArray(inputDataObject, bArray)
        if aArray is not None:
            aArr, aField = _helpers.searchForArray(inputDataObject, aArray)
            self.SetInputArrayToProcess(3, 0, 0, aField, aArray)
            self.SetUseTransparency(True)
        self.SetInputArrayToProcess(0, 0, 0, rField, rArray)
        self.SetInputArrayToProcess(1, 0, 0, gField, gArray)
        self.SetInputArrayToProcess(2, 0, 0, bField, bArray)
        self.Update()
        return interface.wrapvtki(self.GetOutput())



################################################################################
