"""
Reshape Table
~~~~~~~~~~~~~

This example will demonstrate how to reshape an input table as though it were a 2D array.

This filter will take a `vtkTable` object and reshape it. This filter essentially treats `vtkTable`s as 2D matrices and reshapes them using `numpy.reshape` in a C contiguous manner. Unfortunately, data fields will be renamed arbitrarily because VTK data arrays require a name.

This example demos :class:`PVGeo.filters.ReshapeTable`

"""
import numpy as np
import pyvista as pv
import PVGeo
from PVGeo.filters import ReshapeTable

###############################################################################
# Create some input table
t0 = pv.Table()
# Populate the tables
arrs = [None, None, None]
n = 400
ncols = 2
nrows = int(n * len(arrs) / ncols)
titles = ('Array 0', 'Array 1', 'Array 2')
arrs[0] = np.random.random(n)
arrs[1] = np.random.random(n)
arrs[2] = np.random.random(n)

t0[titles[0]] = arrs[0]
t0[titles[1]] = arrs[1]
t0[titles[2]] = arrs[2]

###############################################################################
# Use the filter to reshape the table
order = 'F'
newtitles = ['Title %d' % i for i in range(ncols)]
output = ReshapeTable(order=order, ncols=ncols, nrows=nrows, names=newtitles).apply(t0)
print(output)

###############################################################################
# Check the output
tarr = np.zeros((nrows, ncols))
for i in range(ncols):
    tarr[:, i] = output[i]
arrs = np.array(arrs).T
arrs = arrs.flatten()
arrs = np.reshape(arrs, (nrows, ncols), order=order)
assert tarr.shape == arrs.shape
assert np.allclose(tarr, arrs)
