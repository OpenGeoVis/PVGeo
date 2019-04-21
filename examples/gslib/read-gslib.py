"""
Read GSLib File
~~~~~~~~~~~~~~~

Read GSLib and SGeMS dat file formats
"""
# sphinx_gallery_thumbnail_number = 2
import vtki
from vtki import examples
from PVGeo.gslib import GSLibPointSetReader, SGeMSGridReader

################################################################################
# GSLib Point Set
# +++++++++++++++
points_url = 'http://www.trainingimages.org/uploads/3/4/7/0/34703305/b_100sampledatawl.sgems'
filename, _ = examples.downloads._retrieve_file(points_url, 'b_100sampledatawl.sgems')

point_set = GSLibPointSetReader().apply(filename)
print(point_set)

################################################################################
point_set.plot()


################################################################################
# SGeMS Grid
# ++++++++++
grid_url = 'http://www.trainingimages.org/uploads/3/4/7/0/34703305/a_wlreferencecat.zip'
filename, _ = examples.downloads._retrieve_file(grid_url, 'a_wlreferencecat.sgems.zip')

grid = SGeMSGridReader().apply(filename)
print(grid)

################################################################################
warped = grid.cell_data_to_point_data().warp_by_scalar(scale_factor=5)
warped.plot()
