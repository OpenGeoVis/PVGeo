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

    Args:
        multiplier (float) : a static shifter/scale factor across the array
            after normalization.

        new_name (str): The new array's string name

        operation (str, int, or callable): The operation as a string key, int
            index, or callable method

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
        self.__new_name = kwargs.get('new_name', 'Mathed Up')
        self.__input_array_1 = [None, None]
        self.__input_array_2 = [None, None]
        # Convert operation to callable method
        op = kwargs.get('operation', 'add')
        if isinstance(op, (str, int)):
            op = self.get_operation(op)
        self.__operation = op


    @staticmethod
    def _correlate(arr1, arr2):
        """Use ``np.correlate()`` on ``mode='same'`` on two selected arrays
        from one input.
        """
        return np.correlate(arr1, arr2, mode='same')

    @staticmethod
    def _multiply(arr1, arr2):
        """Mutlipies two input NumPy arrays"""
        return arr1*arr2

    @staticmethod
    def _divide(arr1, arr2):
        """Divides two input NumPy arrays"""
        return arr1/arr2

    @staticmethod
    def _add(arr1, arr2):
        """Adds two input NumPy arrays"""
        return arr1+arr2

    @staticmethod
    def _subtract(arr1, arr2):
        """Subtracts two input NumPy arrays"""
        return arr1-arr2

    @staticmethod
    def get_operations():
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
    def get_operation_names():
        """Gets a list of the math operation keys

        Return:
            list(str): the keys for getting the math operations
        """
        ops = ArrayMath.get_operations()
        return list(ops.keys())

    @staticmethod
    def get_operation(idx):
        """Gets a math operation based on an index in the keys

        Return:
            callable: the math operation method
        """
        if isinstance(idx, str):
            return ArrayMath.get_operations()[idx]
        n = ArrayMath.get_operation_names()[idx]
        return ArrayMath.get_operations()[n]


    def _math_up(self, pdi, pdo):
        """Make sure to pass array names and integer associated fields.
        Use helpers to get these properties.
        """
        if pdo is None:
            # TODO: test this
            pdo = pdi.DeepCopy()
        # Get the input arrays
        field1, name1 = self.__input_array_1[0], self.__input_array_1[1]
        field2, name2 = self.__input_array_2[0], self.__input_array_2[1]
        wpdi = dsa.WrapDataObject(pdi)
        arr1 = _helpers.get_numpy_array(wpdi, field1, name1)
        arr2 = _helpers.get_numpy_array(wpdi, field2, name2)
        # Perform Math Operation
        carr = self.__operation(arr1, arr2)
        # apply the multiplier
        carr *= self.__multiplier
        # If no name given for data by user, use operator name
        new_name = self.__new_name
        if new_name == '':
            new_name = 'Mathed Up'
        # Convert to a VTK array
        c = interface.convert_array(carr, name=new_name)
        # Build output
        pdo.DeepCopy(pdi)
        pdo = _helpers.add_array(pdo, field1, c)
        return pdo


    #### Algorithm Methods ####


    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to perfrom operation and generate output
        """
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        pdo = self.GetOutputData(outInfo, 0)
        # Perfrom task
        self._math_up(pdi, pdo)
        return 1


    #### Seters and Geters ####


    def _set_input_array_1(self, field, name):
        """Set 1st input array by name and field"""
        if self.__input_array_1[0] != field:
            self.__input_array_1[0] = field
            self.Modified()
        if self.__input_array_1[1] != name:
            self.__input_array_1[1] = name
            self.Modified()

    def _set_input_array_2(self, field, name):
        """Set 2nd input array by name and field"""
        if self.__input_array_2[0] != field:
            self.__input_array_2[0] = field
            self.Modified()
        if self.__input_array_2[1] != name:
            self.__input_array_2[1] = name
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
            self._set_input_array_1(field, name)
        elif idx == 1:
            self._set_input_array_2(field, name)
        else:
            raise _helpers.PVGeoError('SetInputArrayToProcess() do not know how to handle idx: %d' % idx)
        return 1

    def apply(self, input_data_object, array_name_0, array_name_1):
        """Run the algorith on an input data object, specifying array names"""
        self.SetInputDataObject(input_data_object)
        arr0, field0 = _helpers.search_for_array(input_data_object, array_name_0)
        arr1, field1 = _helpers.search_for_array(input_data_object, array_name_1)
        self.SetInputArrayToProcess(0, 0, 0, field0, array_name_0)
        self.SetInputArrayToProcess(1, 0, 0, field1, array_name_1)
        self.Update()
        return interface.wrap_pyvista(self.GetOutput())

    def set_multiplier(self, val):
        """This is a static shifter/scale factor across the array after
        normalization.
        """
        if self.__multiplier != val:
            self.__multiplier = val
            self.Modified()

    def get_multiplier(self):
        """Return the set multiplier/scalar
        """
        return self.__multiplier

    def set_new_array_name(self, name):
        """Give the new array a meaningful name.
        """
        if self.__new_name != name:
            self.__new_name = name
            self.Modified()

    def get_new_array_name(self):
        """Get the name used for the new array"""
        return self.__new_name

    def set_operation(self, op):
        """Set the math operation to perform

        Args:
            op (str, int, or callable): The operation as a string key, int
            index, or callable method

        Note:
            This can accept a callable method to set a custom operation as long
            as its signature is: ``<callable>(arr1, arr2)``
        """
        if isinstance(op, str):
            op = ArrayMath.get_operations()[op]
        elif isinstance(op, int):
            op = ArrayMath.get_operation(op)
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

    Args:
        multiplier (float) : a static shifter/scale factor across the array
            after normalization.

        new_name (str): The new array's string name

        absolute (bool):

        normalization (str, int, or callable): The operation as a string key,
            integer index, or callable method

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
        self.__new_name = kwargs.get('new_name', 'Normalized')
        self.__absolute = kwargs.get('absolute', False)
        self.__input_array = [None, None]
        # Convert operation to callable method
        op = kwargs.get('normalization', 'feature_scale')
        if isinstance(op, (str, int)):
            op = self.get_normalization(op)
        self.__normalization = op
        self.__shift = 0.0


    #### Array normalization methods ####


    @staticmethod
    def _pass_array(arr):
        """Cast an input array as a NumPy array"""
        return np.array(arr)

    @staticmethod
    def _feature_scale(arr, rng=None):
        """Returns feature scale normalization of input array"""
        # TODO: implement ability to use custom range
        if rng is not None:
            mi = rng[0]
            ma = rng[1]
        else:
            mi = np.nanmin(arr)
            ma = np.nanmax(arr)
        return (arr - mi) / (ma - mi)

    @staticmethod
    def _standard_score(arr):
        """Returns tandard score normalization of input array"""
        return (arr - np.mean(arr)) / (np.std(arr))

    @staticmethod
    def _log10(arr):
        """Returns log base 10 of input array"""
        return np.log10(arr)

    @staticmethod
    def _log_nat(arr):
        """Returns natural logarithm of input array"""
        return np.log(arr)

    @staticmethod
    def get_normalizations():
        """All Available normalizations

        Return:
            dict: dictionary of callable methods for normalizing an array
        """
        ops = dict(
            feature_scale=NormalizeArray._feature_scale,
            standard_score=NormalizeArray._standard_score,
            log10=NormalizeArray._log10,
            natural_log=NormalizeArray._log_nat,
            just_multiply=NormalizeArray._pass_array,
        )
        return ops

    @staticmethod
    def get_normalization_names():
        """Gets a list of the normalization keys

        Return:
            list(str): the keys for getting the normalizations
        """
        ops = NormalizeArray.get_normalizations()
        return list(ops.keys())

    @staticmethod
    def get_normalization(idx):
        """Gets a normalization based on an index in the keys

        Return:
            callable: the normalization method
        """
        if isinstance(idx, str):
            return NormalizeArray.get_normalizations()[idx]
        n = NormalizeArray.get_normalization_names()[idx]
        return NormalizeArray.get_normalizations()[n]

    @staticmethod
    def get_array_range(pdi, field, name):
        """Returns a tuple of the range for a ``vtkDataArray`` on a
        ``vtkDataObject``.
        """
        wpdi = dsa.WrapDataObject(pdi)
        arr = _helpers.get_numpy_array(wpdi, field, name)
        arr = np.array(arr)
        return (np.nanmin(arr), np.nanmax(arr))


    def _normalize(self, pdi, pdo):
        """Perform normalize on a data array for any given VTK data object.
        """
        # Get input array
        field, name = self.__input_array[0], self.__input_array[1]
        #self.__range = NormalizeArray.get_array_range(pdi, field, name)
        wpdi = dsa.WrapDataObject(pdi)
        arr = _helpers.get_numpy_array(wpdi, field, name)
        arr = np.array(arr, dtype=float)
        # Take absolute value?
        if self.__absolute:
            arr = np.abs(arr)
        arr += self.__shift
        # Perform normalization scheme
        arr = self.__normalization(arr)
        # apply the multiplier
        arr *= self.__multiplier
        # If no name given for data by user, use operator name
        new_name = self.__new_name
        if new_name == '':
            new_name = 'Normalized ' + name
        # Convert to VTK array
        c = interface.convert_array(arr, name=new_name)
        # Build output
        pdo.DeepCopy(pdi)
        pdo = _helpers.add_array(pdo, field, c)
        return pdo

    #### Algorithm Methods ####


    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output
        """
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        pdo = self.GetOutputData(outInfo, 0)
        # Perfrom task
        self._normalize(pdi, pdo)
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
        if self.__input_array[0] != field:
            self.__input_array[0] = field
            self.Modified()
        if self.__input_array[1] != name:
            self.__input_array[1] = name
            self.Modified()
        return 1

    def apply(self, input_data_object, array_name):
        """Run the algorithm on an input data object, specifying the array"""
        self.SetInputDataObject(input_data_object)
        arr, field = _helpers.search_for_array(input_data_object, array_name)
        self.SetInputArrayToProcess(0, 0, 0, field, array_name)
        self.Update()
        return interface.wrap_pyvista(self.GetOutput())

    def set_multiplier(self, val):
        """This is a static shifter/scale factor across the array after
        normalization.
        """
        if self.__multiplier != val:
            self.__multiplier = val
            self.Modified()

    def get_multiplier(self):
        """Return the set multiplier/scalar
        """
        return self.__multiplier


    def set_new_array_name(self, name):
        """Give the new array a meaningful name.
        """
        if self.__new_name != name:
            self.__new_name = name
            self.Modified()

    def get_new_array_name(self):
        """Get the name of the new array"""
        return self.__new_name

    def set_take_absolute_value(self, flag):
        """This will take the absolute value of the array before normalization.
        """
        if self.__absolute != flag:
            self.__absolute = flag
            self.Modified()

    def set_normalization(self, norm):
        """Set the normalization operation to perform

        Args:
            norm (str, int, or callable): The operation as a string key, int
                index, or callable method

        Note:
            This can accept a callable method to set a custom operation as long
            as its signature is: ``<callable>(arr)``
        """
        if isinstance(norm, str):
            norm = NormalizeArray.get_normalizations()[norm]
        elif isinstance(norm, int):
            norm = NormalizeArray.get_normalization(norm)
        if self.__normalization != norm:
            self.__normalization = norm
            self.Modified()

    def set_shift(self, sft):
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
        self.__input_array = [None, None]


    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline for execution"""
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        self.__filter.SetInputDataObject(pdi)
        pdo = self.GetOutputData(outInfo, 0)
        # Get Input Array
        field, name = self.__input_array[0], self.__input_array[1]
        wpdi = dsa.WrapDataObject(pdi)
        arr = _helpers.get_numpy_array(wpdi, field, name)

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
        if self.__input_array[0] != field or self.__input_array[1] != name:
            self.__input_array[0] = field
            self.__input_array[1] = name
            self.__filter.SetInputArrayToProcess(idx, port, connection, field, name)
            self.Modified()
        return 1

    def set_percent(self, percent):
        """Set the percent for the threshold in range (0, 100).
        Any values falling beneath the set percent of the total data range
        will be removed."""
        if self.__percent != percent:
            self.__percent = percent
            self.Modified()

    def set_use_continuous_cell_range(self, flag):
        """If this is on (default is off), we will use the continuous
        interval [minimum cell scalar, maxmimum cell scalar] to intersect
        the threshold bound , rather than the set of discrete scalar
        values from the vertices"""
        return self.__filter.SetUseContinuousCellRange(flag)

    def set_invert(self, flag):
        """Use to invert the threshold filter"""
        if self.__invert != flag:
            self.__invert = flag
            self.Modified()


    def apply(self, input_data_object, array_name):
        """Run the algorithm on an input data object, specifying the array"""
        self.SetInputDataObject(input_data_object)
        arr, field = _helpers.search_for_array(input_data_object, array_name)
        self.SetInputArrayToProcess(0, 0, 0, field, array_name)
        self.Update()
        return interface.wrap_pyvista(self.GetOutput())

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


    def _get_arrays(self, wpdi):
        """Internal helper to fetch RGBA arrays"""
        # Get Red
        fieldr, name = self.__r_array[0], self.__r_array[1]
        r_arr = _helpers.get_numpy_array(wpdi, fieldr, name)
        # Get Green
        fieldg, name = self.__g_array[0], self.__g_array[1]
        g_arr = _helpers.get_numpy_array(wpdi, fieldg, name)
        # Get Blue
        fieldb, name = self.__b_array[0], self.__b_array[1]
        b_arr = _helpers.get_numpy_array(wpdi, fieldb, name)
        # Get Trans
        fielda, name = self.__a_array[0], self.__a_array[1]
        a_arr = _helpers.get_numpy_array(wpdi, fielda, name)
        if fieldr != fieldg != fieldb: # != fielda
            raise _helpers.PVGeoError('Data arrays must be of the same field.')
        self.__field = fieldr
        return r_arr, g_arr, b_arr, a_arr


    def _mask_arrays(self, r_arr, g_arr, b_arr, a_arr):
        """Internal helper to mask RGBA arrays"""
        r_arr = np.ma.masked_where(r_arr==self.__mask, r_arr)
        g_arr = np.ma.masked_where(g_arr==self.__mask, g_arr)
        b_arr = np.ma.masked_where(b_arr==self.__mask, b_arr)
        a_arr = np.ma.masked_where(a_arr==self.__mask, a_arr)
        return r_arr, g_arr, b_arr, a_arr


    def RequestData(self, request, inInfo, outInfo):
        """Execute on pipeline"""
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        wpdi = dsa.WrapDataObject(pdi)
        # Get number of points
        pdo = self.GetOutputData(outInfo, 0)

        # Get the arrays for the RGB values
        r_arr, g_arr, b_arr, a_arr = self._get_arrays(wpdi)
        r_arr, g_arr, b_arr, a_arr = self._mask_arrays(r_arr, g_arr, b_arr, a_arr)

        # normalize each color array bewteen 0 and 255
        r_arr = NormalizeArray._feature_scale(r_arr, [0, 255])
        g_arr = NormalizeArray._feature_scale(g_arr, [0, 255])
        b_arr = NormalizeArray._feature_scale(b_arr, [0, 255])

        # Now concatenate the arrays
        if self.__use_trans:
            a_arr = NormalizeArray._feature_scale(a_arr, [0, 255])
            col = np.array(np.c_[r_arr, g_arr, b_arr, a_arr], dtype=np.uint8)
        else:
            col = np.array(np.c_[r_arr, g_arr, b_arr], dtype=np.uint8)
        colors = interface.convert_array(col, name='Colors')

        # Set the output
        pdo.DeepCopy(pdi)
        # Add new color array
        _helpers.add_array(pdo, self.__field, colors)
        return 1



    #### Seters and Geters ####

    def set_use_transparency(self, flag):
        """Set a boolean flag on whether or not to use a transparency component"""
        if self.__use_trans != flag:
            self.__use_trans = flag
            self.Modified()

    def set_mask_value(self, val):
        """Set the value to mask in the RGBA arrays"""
        if self.__mask != val:
            self.__mask = val
            self.Modified()

    def _set_input_array_red(self, field, name):
        """Set field and name of red array"""
        if self.__r_array[0] != field:
            self.__r_array[0] = field
            self.Modified()
        if self.__r_array[1] != name:
            self.__r_array[1] = name
            self.Modified()

    def _set_input_array_green(self, field, name):
        """Set field and name of green array"""
        if self.__g_array[0] != field:
            self.__g_array[0] = field
            self.Modified()
        if self.__g_array[1] != name:
            self.__g_array[1] = name
            self.Modified()

    def _set_input_array_blue(self, field, name):
        """Set field and name of blue array"""
        if self.__b_array[0] != field:
            self.__b_array[0] = field
            self.Modified()
        if self.__b_array[1] != name:
            self.__b_array[1] = name
            self.Modified()

    def _set_input_array_trans(self, field, name):
        """Set field and name of transparency array"""
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
            self._set_input_array_red(field, name)
        elif idx == 1:
            self._set_input_array_green(field, name)
        elif idx == 2:
            self._set_input_array_blue(field, name)
        elif idx == 3:
            self._set_input_array_trans(field, name)
        else:
            raise _helpers.PVGeoError('SetInputArrayToProcess() do not know how to handle idx: %d' % idx)
        return 1

    def apply(self, input_data_object, r_array, g_array, b_array, a_array=None):
        """Run the algorithm on an input data object, specifying RGBA array names"""
        self.SetInputDataObject(input_data_object)
        r_arr, rField = _helpers.search_for_array(input_data_object, r_array)
        g_arr, gField = _helpers.search_for_array(input_data_object, g_array)
        b_arr, bField = _helpers.search_for_array(input_data_object, b_array)
        if a_array is not None:
            a_arr, aField = _helpers.search_for_array(input_data_object, a_array)
            self.SetInputArrayToProcess(3, 0, 0, aField, a_array)
            self.set_use_transparency(True)
        self.SetInputArrayToProcess(0, 0, 0, rField, r_array)
        self.SetInputArrayToProcess(1, 0, 0, gField, g_array)
        self.SetInputArrayToProcess(2, 0, 0, bField, b_array)
        self.Update()
        return interface.wrap_pyvista(self.GetOutput())



################################################################################
