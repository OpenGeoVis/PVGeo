"""
Combine Tables
~~~~~~~~~~~~~~

This example will demonstrate how to to merge to `vtkTable` objects with the
same number of rows into a single `vtkTable`.

This example demos :class:`PVGeo.filters.CombineTables`

Please note that this example only works on version of PyVista>=0.22.0
"""
import numpy as np
import pyvista as pv
import PVGeo
from PVGeo.filters import CombineTables

###############################################################################
# Create some input tables
t0 = pv.Table()
t1 = pv.Table()

# Populate the tables
n = 100
titles = ('Array 0', 'Array 1', 'Array 2')
arr0 = np.random.random(n)  # Table 0
arr1 = np.random.random(n)  # Table 0
t0[titles[0]] = arr0
t0[titles[1]] = arr1
arr2 = np.random.random(n)  # Table 1
t1[titles[2]] = arr2
arrs = [arr0, arr1, arr2]

###############################################################################
print(t0)

###############################################################################
print(t1)

###############################################################################

# Now use the `CombineTables` filter:
output = CombineTables().apply(t0, t1)
print(output)

###############################################################################

# Here I verify the result
for i in range(len(titles)):
    arr = output[titles[i]]
    assert np.allclose(arr, arrs[i], rtol=0.0001)
