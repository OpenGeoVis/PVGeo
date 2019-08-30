"""
Extract Array to Table
~~~~~~~~~~~~~~~~~~~~~~
This example will demonstrate how to extract an array from any input data set
to make a :class:`pyvista.Table` of that single data array. Aftwards, we plot
a histogram of that data array.

This example demos :class:`PVGeo.filters.ExtractArray`
"""
from PVGeo.filters import ExtractArray
from pyvista import examples
import matplotlib.pyplot as plt

###############################################################################
# Create input data
dataset = examples.download_st_helens()

###############################################################################
# Construct the filter
filt = ExtractArray()
# Define the array to extract
# Apply the filter on the input
table = filt.apply(dataset, 'Elevation')
print(table)

###############################################################################
plt.hist(table['Elevation'])
