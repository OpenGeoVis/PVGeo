"""
Read UBC Gravity Observations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Read a UBC gravity observations file
"""
import pooch
from pyvista import examples

# sphinx_gallery_thumbnail_number = 1
import PVGeo

###############################################################################
# Download sample data files and keep track of names:
url = "https://github.com/OpenGeoVis/PVGeo/raw/main/tests/data/Craig-Chile/LdM_grav_obs.grv"
file_path = pooch.retrieve(url=url, known_hash=None)

###############################################################################
grav = PVGeo.ubc.GravObsReader().apply(file_path)
grav

###############################################################################
grav.plot(render_points_as_spheres=True, point_size=10)
