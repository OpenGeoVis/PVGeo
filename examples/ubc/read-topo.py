"""
Read UBC Topography File
~~~~~~~~~~~~~~~~~~~~~~~~~

Read a UBC topography file
"""
# sphinx_gallery_thumbnail_number = 1
import PVGeo
import pyvista
from pyvista import examples

###############################################################################
# Download sample data files and keep track of names:
url = 'https://github.com/OpenGeoVis/PVGeo/raw/master/tests/data/Craig-Chile/LdM_topo.topo'
topo_file, _ = examples.downloads._retrieve_file(url, 'LdM_topo.topo')

###############################################################################
topo = PVGeo.ubc.TopoReader().apply(topo_file)
print(topo)

###############################################################################
topo.plot(cmap='terrain')
