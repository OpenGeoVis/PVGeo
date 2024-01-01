"""
Read GSLib Table
~~~~~~~~~~~~~~~~

Read any GSLib file as a table :class:`pyvist.Table`

"""
import os

import pooch

from PVGeo.grids import TableToTimeGrid
from PVGeo.gslib import GSLibReader

###############################################################################

# points_url = 'http://www.trainingimages.org/uploads/3/4/7/0/34703305/sundarbans.zip'
url = "https://raw.githubusercontent.com/pyvista/vtk-data/master/Data/sundarbans.SGEMS.zip"
file_paths = pooch.retrieve(url=url, known_hash=None, processor=pooch.Unzip())
file_path = [f for f in file_paths if os.path.basename(f) == "sundarbans.SGEMS"][0]
file_path

###############################################################################
reader = GSLibReader()
table = reader.apply(file_path)
# Print the file header
print(reader.get_file_header())

###############################################################################
table

###############################################################################
# From inspecting the header, we realize that this dataset is gridded, so let's
# use the :class:`PVGeo.grid.TableToTimeGrid` filter to create a
# :class:`pyvista.ImageData` of that dataset.

# 1200 x, 1750 y, 1 z, 1 t
grid = TableToTimeGrid(extent=(1200, 1750, 1, 1), order="F").apply(table)
grid

###############################################################################
grid.plot(cpos="xy")
