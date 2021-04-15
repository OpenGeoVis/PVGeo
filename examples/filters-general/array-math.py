"""
Array Math
~~~~~~~~~~

This example will demonstrate how to perform a mathematical operation
between two input arrays for any given source.

This filter allows the user to select two input data arrays on which to perform
math operations. The input arrays are used in their order of selection for the
operations.


This example demos: :class:`PVGeo.filters.ArrayMath`

"""
import numpy as np
import pyvista
import PVGeo
from PVGeo.filters import ArrayMath

###############################################################################
# Create some input data. This can be any `vtkDataObject`
inp = pyvista.UniformGrid((10, 10, 4))
# Populate the tables
n = 400
arr0 = np.random.random(n)
arr1 = np.random.random(n)
inp['Array 0'] = arr0
inp['Array 1'] = arr1

###############################################################################
# Use the filter:
f = ArrayMath(operation='add', new_name='foo')
# Now get the result
output = f.apply(inp, 'Array 0', 'Array 1')
print(output)

###############################################################################
# Note that the output now has three arrays
arr = output['foo']
assert np.allclose(arr, arr0 + arr1)
###############################################################################

###############################################################################
# Use a custom math operation:
def power(arr0, arr1):
    return arr0 ** arr1


# Use filter generated above
f.set_operation(power)
f.set_new_array_name('powered')
f.update()

# Now get the result
output = f.get_output()
print(output)
###############################################################################
arr = output['powered']
assert np.allclose(arr, arr0 ** arr1)

###############################################################################
output.plot(scalars='powered')
