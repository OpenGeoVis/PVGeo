"""
Add Cell Connectivity To Points
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example for :class:`PVGeo.filters.AddCellConnToPoints`

This filter will add **linear** cell connectivity between scattered points.
You have the option to add ``VTK_LINE`` or ``VTK_POLYLINE`` connectivity.
``VTK_LINE`` connectivity makes a straight line between the points in order
(either in the order by index or using a nearest neighbor calculation).
The ``VTK_POLYLINE`` adds polyline connectivity between all points as one
spline (either in the order by index or using a nearest neighbor calculation).

"""
###############################################################################
# sphinx_gallery_thumbnail_number = 2
import numpy as np
import pyvista
from PVGeo import points_to_poly_data
from PVGeo.filters import AddCellConnToPoints

###############################################################################
# First, lets generate some points which we'd like to connect


def path1(y):
    """Equation: x = a(y-h)^2 + k"""
    a = -110.0 / 160.0 ** 2
    x = a * y ** 2 + 110.0
    idxs = np.argwhere(x > 0)
    return x[idxs][:, 0], y[idxs][:, 0]


x, y = path1(np.arange(0.0, 200.0, 25.0))
zo = np.linspace(9.0, 11.0, num=len(y))
coords = np.vstack((x, y, zo)).T
# Shuffle points to demonstrate value of Nearest Neighbor
np.random.shuffle(coords)

# Make a VTK data object for the filter to use
vtkPoints = points_to_poly_data(coords)

###############################################################################
# Apply the Filter
# ++++++++++++++++
#
# Now that you have the points generated, lets go ahead and apply
# the **Add Cell Connectivity To Points** filter from
# *Filters->PVGeo: General Filters->Add Cell Connectivity To Points*.
# The output data should look really wacky and incorrectly built like the image
# below; this is good.
line = AddCellConnToPoints().apply(vtkPoints)

p = pyvista.Plotter()
p.add_mesh(line, line_width=5, point_size=10)
p.show()


###############################################################################
# Remember that in the script given above we shuffle the points to demonstrate
# that the points make a useable line but we need to reconstruct the order of the
# points. We do this by using the *Use Nearest Nbr Approx* checkbox; this will
# ensure that a useable path is generate from the points.
# Go ahead and use the ``nearest_nbr`` argument for the algorith.
# Now it looks good (see image below)!


# Use the filter: Here is vtkPolyData containing the connected line:
line_o = AddCellConnToPoints(nearest_nbr=True).apply(vtkPoints)

p = pyvista.Plotter()
p.add_mesh(line_o, line_width=5, point_size=10)
p.show()
