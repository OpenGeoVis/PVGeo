paraview_plugin_version = '1.1.10'
# This is module to import. It provides VTKPythonAlgorithmBase, the base class
# for all python-based vtkAlgorithm subclasses in VTK and decorators used to
# 'register' the algorithm with ParaView along with information about UI.
from paraview.util.vtkAlgorithm import *

# Helpers:
from PVGeo import _helpers
# Classes to Decorate
from PVGeo.grids import ReverseImageDataAxii, TranslateGridOrigin, TableToGrid, ExtractTopography


#### GLOBAL VARIABLES ####
MENU_CAT = 'PVGeo: General Grids'


###############################################################################


@smproxy.filter(name='PVGeoReverseImageDataAxii', label='Reverse Image Data Axii')
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkImageData"], composite_data_supported=False)
class PVGeoReverseImageDataAxii(ReverseImageDataAxii):
    def __init__(self):
        ReverseImageDataAxii.__init__(self)

    #### Seters and Geters ####

    @smproperty.xml(_helpers.getPropertyXml(name='Flip X Axis', command='SetFlipX', default_values=True, help='A boolean to set whether to flip the X axis.'))
    def SetFlipX(self, flag):
        ReverseImageDataAxii.SetFlipX(self, flag)

    @smproperty.xml(_helpers.getPropertyXml(name='Flip Y Axis', command='SetFlipY', default_values=True, help='A boolean to set whether to flip the Y axis.'))
    def SetFlipY(self, flag):
        ReverseImageDataAxii.SetFlipY(self, flag)

    @smproperty.xml(_helpers.getPropertyXml(name='Flip Z Axis', command='SetFlipZ', default_values=True, help='A boolean to set whether to flip the Z axis.'))
    def SetFlipZ(self, flag):
        ReverseImageDataAxii.SetFlipZ(self, flag)


###############################################################################


@smproxy.filter(name='PVGeoTranslateGridOrigin', label='Translate Grid Origin')
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkImageData"], composite_data_supported=False)
class PVGeoTranslateGridOrigin(TranslateGridOrigin):
    def __init__(self):
        TranslateGridOrigin.__init__(self)

    #### Seters and Geters ####

    @smproperty.xml(_helpers.getDropDownXml(name='Corner', command='SetCorner',
        labels=['South East Bottom', 'North West Bottom', 'North East Bottom',
        'South West Top', 'South East Top', 'North West Top', 'North East Top'],
        values=[1,2,3,4,5,6,7]))
    def SetCorner(self, corner):
        TranslateGridOrigin.SetCorner(self, corner)


###############################################################################


@smproxy.filter(name='PVGeoTableToGrid', label='Table To Grid')
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkTable"], composite_data_supported=False)
@smhint.xml('''<RepresentationType view="RenderView" type="Surface With Edges" />''')
class PVGeoTableToGrid(TableToGrid):
    def __init__(self):
        TableToGrid.__init__(self)


    #### Setters / Getters ####


    @smproperty.intvector(name="Extent", default_values=[10, 10, 10])
    def SetExtent(self, nx, ny, nz):
        TableToGrid.SetExtent(self, nx, ny, nz)

    @smproperty.doublevector(name="Spacing", default_values=[1.0, 1.0, 1.0])
    def SetSpacing(self, dx, dy, dz):
        TableToGrid.SetSpacing(self, dx, dy, dz)

    @smproperty.doublevector(name="Origin", default_values=[0.0, 0.0, 0.0])
    def SetOrigin(self, x0, y0, z0):
        TableToGrid.SetOrigin(self, x0, y0, z0)

    @smproperty.xml(_helpers.getPropertyXml(name='SEPlib', command='SetSEPlib', default_values=False, help='Use the Stanford Exploration Project\'s axial conventions (d1=z, d2=x, d3=y). Parameters would be entered [z,x,y].'))
    def SetSEPlib(self, flag):
        TableToGrid.SetSEPlib(self, flag)

    @smproperty.xml(_helpers.getDropDownXml(name='Order', command='SetOrder',
        labels=['Fortran-style: column-major order', 'C-style: Row-major order'],
        values=[0, 1]))
    def SetOrder(self, order):
        o = ['F', 'C']
        TableToGrid.SetOrder(self, o[order])

    @smproperty.xml(_helpers.getPropertyXml(name='Swap XY', command='SetSwapXY', default_values=False))
    def SetSwapXY(self, flag):
        TableToGrid.SetSwapXY(self, flag)



###############################################################################


@smproxy.filter(name='PVGeoExtractTopography', label='Extract Topography')
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
@smproperty.input(name="Topography", port_index=1)
@smdomain.datatype(dataTypes=["vtkPolyData"], composite_data_supported=False)
@smproperty.input(name="Data Set", port_index=0)
@smdomain.datatype(dataTypes=["vtkDataSet"], composite_data_supported=False)
class PVGeoExtractTopography(ExtractTopography):
    def __init__(self):
        ExtractTopography.__init__(self)

    #### Seters and Geters ####
