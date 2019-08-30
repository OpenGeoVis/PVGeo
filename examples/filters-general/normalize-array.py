"""
Normalize Array
~~~~~~~~~~~~~~~

This example will demonstrate how to perform a normalization or any custom
mathematical operation on a single data array for an input data set.

This filter allow the user to select an array from the input data set to be
normalized. The filter will append another array to that data set for the
output. The user can specify how they want to rename the array, can choose a
multiplier, and can choose from two types of common normalizations:
Feature Scaling and Standard Score.

This example demos :class:`PVGeo.filters.NormalizeArray`

"""
import numpy as np
import pyvista
from pyvista import examples
import PVGeo
from PVGeo.filters import NormalizeArray

###############################################################################
# Create some input data. this can be any `vtkDataObject`
mesh = examples.load_uniform()
title = 'Spatial Point Data'
mesh.plot(scalars=title)
###############################################################################

# Apply the filter
f = NormalizeArray(normalization='feature_scale', new_name='foo')
output = f.apply(mesh, title)
print(output)

###############################################################################
output.plot(scalars='foo')
