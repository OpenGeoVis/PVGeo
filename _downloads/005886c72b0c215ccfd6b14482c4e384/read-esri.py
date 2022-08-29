"""
Read ESRI Grid File
~~~~~~~~~~~~~~~~~~~

Read an ESRI ASCII grid file
"""
import os

import pooch
from pyvista import examples

from PVGeo.grids import EsriGridReader

###############################################################################
# Download a sample ESRI grid file
url = "https://raw.githubusercontent.com/pyvista/vtk-data/master/Data/esri_grid.dem.zip"
file_paths = pooch.retrieve(url=url, known_hash=None, processor=pooch.Unzip())
file_path = [f for f in file_paths if os.path.basename(f) == "esri_grid.dem"][0]
file_path

###############################################################################
dem = EsriGridReader().apply(file_path)
dem

###############################################################################
# Apply a filter to the DEM to have realistic topography
warped = dem.warp_by_scalar()
warped.plot(cmap="terrain", clim=[-100, 400])
