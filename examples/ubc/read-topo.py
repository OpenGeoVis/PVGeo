"""
Read UBC Topography File
~~~~~~~~~~~~~~~~~~~~~~~~~

Read a UBC topography file
"""
# sphinx_gallery_thumbnail_number = 1
import pooch

import PVGeo

###############################################################################
# Download sample data files and keep track of names:
url = "https://github.com/OpenGeoVis/PVGeo/raw/main/tests/data/Craig-Chile/LdM_topo.topo"
file_path = pooch.retrieve(url=url, known_hash=None)

###############################################################################
topo = PVGeo.ubc.TopoReader().apply(file_path)
topo

###############################################################################
topo.plot(cmap="terrain", notebook=0)
