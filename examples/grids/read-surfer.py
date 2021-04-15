"""
Read Surfer Grid File
~~~~~~~~~~~~~~~~~~~~~

Read an Surfer ASCII grid file
"""
import pyvista
from PVGeo.grids import SurferGridReader
from pyvista import examples

###############################################################################
# Download a sample Surfer grid file
fname = 'surfer-grid.grd'
url = 'https://github.com/OpenGeoVis/PVGeo/raw/master/tests/data/{}'.format(fname)
filename, _ = examples.downloads._retrieve_file(url, fname)
dem = SurferGridReader().apply(filename)

###############################################################################
# Apply a filter to the DEM to have realistic topography
warped = dem.warp_by_scalar(scale_factor=300.0)
warped.plot(cmap='terrain')
