"""
Read GSLib Point Set
~~~~~~~~~~~~~~~~~~~~

Read GSLib point set file
"""
# sphinx_gallery_thumbnail_number = 1
import pooch

from PVGeo.gslib import GSLibPointSetReader

###############################################################################

# points_url = 'http://www.trainingimages.org/uploads/3/4/7/0/34703305/b_100sampledatawl.sgems'
url = "https://raw.githubusercontent.com/pyvista/vtk-data/master/Data/b_100sampledatawl.sgems"
file_path = pooch.retrieve(url=url, known_hash=None)

point_set = GSLibPointSetReader().apply(file_path)
point_set

###############################################################################
point_set.plot()
