"""
Extract Array to Table
~~~~~~~~~~~~~~~~~~~~~~
This example will demonstrate how to extract an array from any input data set
to make a `vtkTable` of that single data array

This example demos :class:`PVGeo.filters.ExtractArray`
"""
from PVGeo.filters import ExtractArray
from vista import examples
################################################################################
# Create input data
grd = examples.load_rectilinear()

################################################################################
# Construct the filter
filt = ExtractArray()
# Define the array to extract
# Apply the filter on the input
table = filt.apply(grd, 'Random Data')
print(table)
