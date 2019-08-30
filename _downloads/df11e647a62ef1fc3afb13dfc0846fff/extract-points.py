"""
Extract Points
~~~~~~~~~~~~~~

This example will demonstrate how to extract the points and PointData of
any input data set that has valid PointData into a `vtkPolyData` object.

This example demos :class:`PVGeo.filters.ExtractPoints`
"""
# sphinx_gallery_thumbnail_number = 2
from pyvista import examples
from PVGeo.filters import ExtractPoints

###############################################################################
# Have some input data source with valid PointData
data = examples.load_globe()
data.plot()

###############################################################################
# Apply the filter:
polyData = ExtractPoints().apply(data)
polyData.plot()
