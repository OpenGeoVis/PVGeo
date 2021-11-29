"""
Read UBC Topography File
~~~~~~~~~~~~~~~~~~~~~~~~~

Read a UBC topography file
"""
from pyvista import examples

# sphinx_gallery_thumbnail_number = 1
import PVGeo

###############################################################################
# Download sample data files and keep track of names:
url = 'https://github.com/OpenGeoVis/PVGeo/raw/master/tests/data/Craig-Chile/LdM_topo.topo'
topo_file, _ = examples.downloads._retrieve_file(url, 'LdM_topo.topo')

###############################################################################
topo = PVGeo.ubc.TopoReader().apply(topo_file)
topo

###############################################################################
topo.plot(cmap='terrain')
