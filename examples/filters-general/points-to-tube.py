"""
Points to Tube
~~~~~~~~~~~~~~

This example will demonstrate how to to build a tube from a set of points in
`vtkPolyData`.

Takes points from a `vtkPolyData` object and constructs a line of those points
then builds a polygonal tube around that line with some specified radius and number of sides.
"""
# sphinx_gallery_thumbnail_number = 2
import pyvista
import numpy as np
from PVGeo.filters import PointsToTube

###############################################################################


def path(y):
    """Equation: x = a(y-h)^2 + k"""
    a = -110.0 / 160.0 ** 2
    x = a * y ** 2 + 110.0
    return x, y


x, y = path(np.arange(0.0, 200.0, 25.0))
zo = np.linspace(9.0, 11.0, num=len(y))
points = pyvista.PolyData(np.c_[x, y, zo])

points.plot(point_size=10)

###############################################################################

# Use the filter: here is vtkPolyData containing the tube
tube = PointsToTube(nearestNbr=True).apply(points)
tube.plot(color=True)
