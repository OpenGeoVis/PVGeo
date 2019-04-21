"""
Voxelize Points
~~~~~~~~~~~~~~~

This example will demonstrate how to connect a set of points defined on a
regular grid to create a `vtkUnstructuredGrid` which can be used to perform
volumetric operations.


This example demos :class:`PVGeo.filters.VoxelizePoints`
"""
# sphinx_gallery_thumbnail_number = 2
import vtki
import numpy as np
import PVGeo
from PVGeo.filters import VoxelizePoints

################################################################################
# Make a mesh grid
dd = 10
x = y = z = np.arange(0, 100, dd)
xx, yy, zz = np.meshgrid(x, y, z)
points = vtki.PolyData(np.c_[xx.ravel(), yy.ravel(), zz.ravel()])
# points.rotate_z(25.) # TODO: angle recovery isn't working for this dataset

rand = np.random.random(points.n_points)
points['Random'] = rand

points.plot(show_grid=True)

################################################################################
# Use the filter

# Instantiate the algorithm
v = VoxelizePoints()
v.set_estimate_grid(True)

################################################################################
recovered = v.apply(points)
print('Recovered rotation angle: {}'.format(v.get_recovered_angle()))
recovered.plot()
