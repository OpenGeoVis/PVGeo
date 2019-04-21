"""
Read ESRI Grid File
~~~~~~~~~~~~~~~~~~~

Read an ESRI ASCII grid file
"""
import vtki
from PVGeo.grids import EsriGridReader
from vtki import examples

################################################################################
# Download a sample ESRI grid file
filename, _ = examples.downloads._download_file('esri_grid.dem.zip')
dem = EsriGridReader().apply(filename)

################################################################################
# Apply a filter to the DEM to have realistic topography
warped = dem.warp_by_scalar()
warped.plot(cmap='terrain', clim=[-100, 400])
