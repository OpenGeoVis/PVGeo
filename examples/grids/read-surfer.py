"""
Read ESRI Grid File
~~~~~~~~~~~~~~~~~~~

Read an ESRI ASCII grid file
"""
import vtki
from PVGeo.grids import SurferGridReader
from vtki import examples

################################################################################
# Download a sample ESRI grid file
fname = 'surfer-grid.grd'
url = 'https://github.com/OpenGeoVis/PVGeo/raw/master/tests/data/{}'.format(fname)
filename, _ = examples.downloads._retrieve_file(url, fname)
dem = SurferGridReader().apply(filename)

################################################################################
# Apply a filter to the DEM to have realistic topography
warped = dem.warp_by_scalar(scale_factor=300.)
warped.plot(cmap='terrain')
