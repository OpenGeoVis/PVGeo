"""
Read Surfer Grid File
~~~~~~~~~~~~~~~~~~~~~

Read an Surfer ASCII grid file
"""
import pooch
from pyvista import examples

from PVGeo.grids import SurferGridReader

###############################################################################
# Download a sample Surfer grid file
fname = "surfer-grid.grd"
url = "https://github.com/OpenGeoVis/PVGeo/raw/main/tests/data/{}".format(fname)
file_path = pooch.retrieve(url=url, known_hash=None)

dem = SurferGridReader().apply(file_path)
dem

###############################################################################
# Apply a filter to the DEM to have realistic topography
warped = dem.warp_by_scalar(scale_factor=300.0)
warped.plot(cmap="terrain")
