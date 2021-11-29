"""
Read ESRI Grid File
~~~~~~~~~~~~~~~~~~~

Read an ESRI ASCII grid file
"""
import pyvista
from pyvista import examples

from PVGeo.grids import EsriGridReader

###############################################################################
# Download a sample ESRI grid file
filename, _ = examples.downloads._download_file('esri_grid.dem.zip')
dem = EsriGridReader().apply(filename)
dem

###############################################################################
# Apply a filter to the DEM to have realistic topography
warped = dem.warp_by_scalar()
warped.plot(cmap='terrain', clim=[-100, 400])
