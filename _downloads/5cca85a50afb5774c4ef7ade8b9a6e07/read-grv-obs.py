"""
Read UBC Gravity Observations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Read a UBC gravity observations file
"""
# sphinx_gallery_thumbnail_number = 1
import PVGeo
import pyvista
from pyvista import examples

###############################################################################
# Download sample data files and keep track of names:
url = 'https://github.com/OpenGeoVis/PVGeo/raw/master/tests/data/Craig-Chile/LdM_grav_obs.grv'
grav_file, _ = examples.downloads._retrieve_file(url, 'LdM_grav_obs.grv')

###############################################################################
grav = PVGeo.ubc.GravObsReader().apply(grav_file)
print(grav)

###############################################################################
grav.plot(render_points_as_spheres=True, point_size=10)
