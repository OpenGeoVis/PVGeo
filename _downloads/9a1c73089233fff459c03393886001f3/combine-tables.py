"""
Combine Tables
~~~~~~~~~~~~~~

This example will demonstrate how to to merge to `vtkTable` objects with the
same number of rows into a single `vtkTable`.

This example demos :class:`PVGeo.filters.CombineTables`
"""
import numpy as np
import vtk
from vtk.numpy_interface import dataset_adapter as dsa
import PVGeo
from PVGeo.filters import CombineTables

################################################################################
# Create some input tables
t0 = vtk.vtkTable()
t1 = vtk.vtkTable()
# Populate the tables
n = 100
titles = ('Array 0', 'Array 1', 'Array 2')
arr0 = np.random.random(n) # Table 0
arr1 = np.random.random(n) # Table 0
t0.AddColumn(PVGeo.convert_array(arr0, titles[0]))
t0.AddColumn(PVGeo.convert_array(arr1, titles[1]))
arr2 = np.random.random(n) # Table 1
t1.AddColumn(PVGeo.convert_array(arr2, titles[2]))
arrs = [arr0, arr1, arr2]

################################################################################

# Now use the `CombineTables` filter:
output = CombineTables().apply(t0, t1)


# Here I verify the result
wpdi = dsa.WrapDataObject(output)

for i in range(len(titles)):
    arr = wpdi.RowData[titles[i]]
    assert(np.allclose(arr, arrs[i], rtol=0.0001))
