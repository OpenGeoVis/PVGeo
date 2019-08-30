"""
Read SGeMS Grid
~~~~~~~~~~~~~~~

Read SGeMS Grid file formats.
"""
# sphinx_gallery_thumbnail_number = 2
from pyvista import examples
from PVGeo.gslib import SGeMSGridReader

###############################################################################
grid_url = 'http://www.trainingimages.org/uploads/3/4/7/0/34703305/a_wlreferencecat.zip'
filename, _ = examples.downloads._retrieve_file(grid_url, 'A_WLreferenceCAT.sgems.zip')

grid = SGeMSGridReader().apply(filename)
print(grid)

###############################################################################
warped = grid.cell_data_to_point_data().warp_by_scalar(scale_factor=5)
warped.plot()

###############################################################################
grid_url = 'http://www.trainingimages.org/uploads/3/4/7/0/34703305/maules_creek_3d.zip'
filename, _ = examples.downloads._retrieve_file(grid_url, 'Maules_Creek_3D.SGEMS.zip')

grid = SGeMSGridReader().apply(filename)
grid.plot(categories=True)


###############################################################################
grid_url = 'http://www.trainingimages.org/uploads/3/4/7/0/34703305/ti_horizons_continuous.zip'
filename, _ = examples.downloads._retrieve_file(grid_url, 'TI_horizons_continuous.SGEMS.zip')

grid = SGeMSGridReader().apply(filename)
grid.threshold([-4, 1.06]).plot(clim=grid.get_data_range())


###############################################################################
grid_url = 'http://www.trainingimages.org/uploads/3/4/7/0/34703305/ti.zip'
filename, _ = examples.downloads._retrieve_file(grid_url, 'ti.sgems.zip')

grid = SGeMSGridReader().apply(filename)
grid.plot(scalars='photo', cpos='xy', cmap='bone')

###############################################################################
grid.plot(scalars='seismic', cpos='xy')
