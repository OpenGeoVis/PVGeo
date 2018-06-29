# This is module to import. It provides VTKPythonAlgorithmBase, the base class
# for all python-based vtkAlgorithm subclasses in VTK and decorators used to
# 'register' the algorithm with ParaView along with information about UI.
from paraview.util.vtkAlgorithm import *

import numpy as np
import vtk

# Helpers:
from PVGeo import _helpers
# Classes to Decorate
from PVGeo.model_build import *

MENU_CAT = 'PVGeo: Model Building'



###############################################################################


@smproxy.source(name='PVGeoCreateEvenRectilinearGrid', label='Create Even Rectilinear Grid')
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
class PVGeoCreateEvenRectilinearGrid(CreateEvenRectilinearGrid):
    def __init__(self):
        CreateEvenRectilinearGrid.__init__(self)

    #### Setters / Getters ####

    @smproperty.intvector(name="Extent", default_values=[10, 10, 10])
    def SetExtent(self, nx, ny, nz):
        CreateEvenRectilinearGrid.SetExtent(self, nx, ny, nz)

    @smproperty.doublevector(name="X Range", default_values=[-1.0, 1.0])
    def SetXRange(self, start, stop):
        CreateEvenRectilinearGrid.SetXRange(self, start, stop)

    @smproperty.doublevector(name="Y Range", default_values=[-1.0, 1.0])
    def SetYRange(self, start, stop):
        CreateEvenRectilinearGrid.SetYRange(self, start, stop)

    @smproperty.doublevector(name="Z Range", default_values=[-1.0, 1.0])
    def SetZRange(self, start, stop):
        CreateEvenRectilinearGrid.SetZRange(self, start, stop)


###############################################################################


@smproxy.source(name='PVGeoCreateOddRectilinearGrid', label='Create Odd Rectilinear Grid')
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
class PVGeoCreateOddRectilinearGrid(CreateOddRectilinearGrid):
    def __init__(self):
        CreateOddRectilinearGrid.__init__(self)

    @smproperty.stringvector(name="X Cells", default_values='200 100 50 20*50.0 50 100 200')
    def SetXCellsStr(self, xcellstr):
        CreateOddRectilinearGrid.SetXCellsStr(self, xcellstr)

    @smproperty.stringvector(name="Y Cells", default_values='200 100 50 21*50.0 50 100 200')
    def SetYCellsStr(self, ycellstr):
        CreateOddRectilinearGrid.SetYCellsStr(self, ycellstr)

    @smproperty.stringvector(name="Z Cells", default_values='20*25.0 50 100 200')
    def SetZCellsStr(self, zcellstr):
        CreateOddRectilinearGrid.SetZCellsStr(self, zcellstr)


###############################################################################


@smproxy.source(name='PVGeoCreateUniformGrid', label='Create Uniform Grid')
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
class PVGeoCreateUniformGrid(CreateUniformGrid):
    def __init__(self):
        CreateUniformGrid.__init__(self)


    #### Setters / Getters ####


    @smproperty.intvector(name="Extent", default_values=[10, 10, 10])
    def SetExtent(self, nx, ny, nz):
        CreateUniformGrid.SetExtent(self, nx, ny, nz)

    @smproperty.doublevector(name="Spacing", default_values=[1.0, 1.0, 1.0])
    def SetSpacing(self, dx, dy, dz):
        CreateUniformGrid.SetSpacing(self, dx, dy, dz)

    @smproperty.doublevector(name="Origin", default_values=[0.0, 0.0, 0.0])
    def SetOrigin(self, x0, y0, z0):
        CreateUniformGrid.SetOrigin(self, x0, y0, z0)


###############################################################################


@smproxy.source(name='PVGeoEarthSource', label='Create Earth Source')
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
class PVGeoEarthSource(EarthSource):
    def __init__(self):
        EarthSource.__init__(self)

    @smproperty.doublevector(name="Radius", default_values=6371.0)
    def SetRadius(self, radius):
        EarthSource.SetRadius(self, radius)
