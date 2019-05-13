paraview_plugin_version = '2.0.0'
# This is module to import. It provides VTKPythonAlgorithmBase, the base class
# for all python-based vtkAlgorithm subclasses in VTK and decorators used to
# 'register' the algorithm with ParaView along with information about UI.
from paraview.util.vtkAlgorithm import *

# Classes to Decorate
from PVGeo.model_build import *

MENU_CAT = 'PVGeo: Model Building'



###############################################################################


@smproxy.source(name='PVGeoCreateEvenRectilinearGrid', label='Create Even Rectilinear Grid')
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface With Edges" />''' % MENU_CAT)
class PVGeoCreateEvenRectilinearGrid(CreateEvenRectilinearGrid):
    def __init__(self):
        CreateEvenRectilinearGrid.__init__(self)

    #### Setters / Getters ####

    @smproperty.intvector(name="Extent", default_values=[10, 10, 10])
    def set_extent(self, nx, ny, nz):
        CreateEvenRectilinearGrid.set_extent(self, nx, ny, nz)

    @smproperty.doublevector(name="X Range", default_values=[-1.0, 1.0])
    def set_x_range(self, start, stop):
        CreateEvenRectilinearGrid.set_x_range(self, start, stop)

    @smproperty.doublevector(name="Y Range", default_values=[-1.0, 1.0])
    def set_y_range(self, start, stop):
        CreateEvenRectilinearGrid.set_y_range(self, start, stop)

    @smproperty.doublevector(name="Z Range", default_values=[-1.0, 1.0])
    def set_z_range(self, start, stop):
        CreateEvenRectilinearGrid.set_z_range(self, start, stop)


###############################################################################


@smproxy.source(name='PVGeoCreateTensorMesh', label='Create Tensor Mesh')
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface With Edges" />''' % MENU_CAT)
class PVGeoCreateTensorMesh(CreateTensorMesh):
    def __init__(self):
        CreateTensorMesh.__init__(self)

    @smproperty.stringvector(name="X Cells", default_values='200 100 50 20*50.0 50 100 200')
    def set_x_cells_str(self, xcellstr):
        CreateTensorMesh.set_x_cells_str(self, xcellstr)

    @smproperty.stringvector(name="Y Cells", default_values='200 100 50 21*50.0 50 100 200')
    def set_y_cells_str(self, ycellstr):
        CreateTensorMesh.set_y_cells_str(self, ycellstr)

    @smproperty.stringvector(name="Z Cells", default_values='20*25.0 50 100 200')
    def set_z_cells_str(self, zcellstr):
        CreateTensorMesh.set_z_cells_str(self, zcellstr)

    @smproperty.doublevector(name="Origin", default_values=[-350.0, -400.0, 0.0])
    def set_origin(self, x0, y0, z0):
        CreateTensorMesh.set_origin(self, x0, y0, z0)


###############################################################################


@smproxy.source(name='PVGeoCreateUniformGrid', label='Create Uniform Grid')
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface With Edges" />''' % MENU_CAT)
class PVGeoCreateUniformGrid(CreateUniformGrid):
    def __init__(self):
        CreateUniformGrid.__init__(self)


    #### Setters / Getters ####


    @smproperty.intvector(name="Extent", default_values=[10, 10, 10])
    def set_extent(self, nx, ny, nz):
        CreateUniformGrid.set_extent(self, nx, ny, nz)

    @smproperty.doublevector(name="Spacing", default_values=[1.0, 1.0, 1.0])
    def set_spacing(self, dx, dy, dz):
        CreateUniformGrid.set_spacing(self, dx, dy, dz)

    @smproperty.doublevector(name="Origin", default_values=[0.0, 0.0, 0.0])
    def set_origin(self, x0, y0, z0):
        CreateUniformGrid.set_origin(self, x0, y0, z0)


###############################################################################


@smproxy.source(name='PVGeoOutlineContinents', label=OutlineContinents.__displayname__)
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
class PVGeoOutlineContinents(OutlineContinents):
    def __init__(self):
        OutlineContinents.__init__(self)

    @smproperty.doublevector(name="Radius", default_values=6371.0e6)
    def set_radius(self, radius):
        OutlineContinents.set_radius(self, radius)


###############################################################################


@smproxy.source(name='PVGeoGlobeSource', label=GlobeSource.__displayname__)
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
class PVGeoGlobeSource(GlobeSource):
    def __init__(self):
        GlobeSource.__init__(self)

    @smproperty.doublevector(name="Radius", default_values=6371.0e6)
    def set_radius(self, radius):
        GlobeSource.set_radius(self, radius)

    @smproperty.intvector(name="Meridians", default_values=36)
    @smdomain.intrange(min=2, max=100)
    def set_n_meridians(self, n):
        GlobeSource.set_n_meridians(self, n)

    @smproperty.intvector(name="Parallels", default_values=15)
    @smdomain.intrange(min=2, max=100)
    def set_n_parallels(self, n):
        GlobeSource.set_n_parallels(self, n)


###############################################################################
