paraview_plugin_version = '1.1.29'
# This is module to import. It provides VTKPythonAlgorithmBase, the base class
# for all python-based vtkAlgorithm subclasses in VTK and decorators used to
# 'register' the algorithm with ParaView along with information about UI.
from paraview.util.vtkAlgorithm import *

# Helpers:
from PVGeo import _helpers
# Classes to Decorate
from PVGeo.grids import *


#### GLOBAL VARIABLES ####
MENU_CAT = 'PVGeo: General Grids'


###############################################################################


@smproxy.filter(name='PVGeoReverseImageDataAxii', label='Reverse Image Data Axii')
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkImageData"], composite_data_supported=True)
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
@smdomain.datatype(dataTypes=["vtkImageData"], composite_data_supported=True)
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
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface With Edges" />''' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkTable"], composite_data_supported=True)
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
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface With Edges" />''' % MENU_CAT)
@smproperty.input(name="Topography", port_index=1)
@smdomain.datatype(dataTypes=["vtkPolyData"], composite_data_supported=False)
@smproperty.input(name="Data Set", port_index=0)
@smdomain.datatype(dataTypes=["vtkDataSet"], composite_data_supported=False)
class PVGeoExtractTopography(ExtractTopography):
    def __init__(self):
        ExtractTopography.__init__(self)

    #### Seters and Geters ####

    @smproperty.doublevector(name="Tolerance", default_values=1.0)
    def SetTolerance(self, tol):
        ExtractTopography.SetTolerance(self, tol)

###############################################################################

SURF_DESC = "Surfer Grid"
SURF_EXTS = "grd GRD"

@smproxy.reader(name="PVGeoSurferGridReader",
       label="PVGeo: Surfer Grid File Format",
       extensions=SURF_EXTS,
       file_description=SURF_DESC)
class PVGeoSurferGridReader(SurferGridReader):
    def __init__(self):
        SurferGridReader.__init__(self)

    #### Seters and Geters ####

    @smproperty.xml(_helpers.getFileReaderXml(SURF_EXTS, readerDescription=SURF_DESC))
    def AddFileName(self, fname):
        SurferGridReader.AddFileName(self, fname)

    @smproperty.stringvector(name='DataName', default_values='Data')
    def SetDataName(self, dataName):
        SurferGridReader.SetDataName(self, dataName)


###############################################################################


@smproxy.writer(extensions="grd", file_description="Surfer Grid (ASCII)", support_reload=False)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkImageData", "vtkMultiBlockDataSet"], composite_data_supported=True)
class PVGeoWriteImageDataToSurfer(WriteImageDataToSurfer):
    def __init__(self):
        WriteImageDataToSurfer.__init__(self)

    @smproperty.stringvector(name="FileName", panel_visibility="never")
    @smdomain.filelist()
    def SetFileName(self, fname):
        """Specify filename for the file to write."""
        WriteImageDataToSurfer.SetFileName(self, fname)

    @smproperty.xml(_helpers.getInputArrayXml(nInputPorts=1, numArrays=1))
    def SetInputArrayToProcess(self, idx, port, connection, field, name):
        return WriteImageDataToSurfer.SetInputArrayToProcess(self, idx, port, connection, field, name)

    @smproperty.stringvector(name="Format", default_values='%.9e')
    def SetFormat(self, fmt):
        """Use to set the ASCII format for the writer default is ``'%.9e'``"""
        WriteImageDataToSurfer.SetFormat(self, fmt)



###############################################################################

@smproxy.writer(extensions="dat", file_description="Cell Centers and Cell Data", support_reload=False)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkDataSet"], composite_data_supported=True)
class PVGeoWriteCellCenterData(WriteCellCenterData):
    def __init__(self):
        WriteCellCenterData.__init__(self)


    @smproperty.stringvector(name="FileName", panel_visibility="never")
    @smdomain.filelist()
    def SetFileName(self, fname):
        """Specify filename for the file to write."""
        WriteCellCenterData.SetFileName(self, fname)

    @smproperty.stringvector(name="Format", default_values='%.9e')
    def SetFormat(self, fmt):
        """Use to set the ASCII format for the writer default is ``'%.9e'``"""
        WriteCellCenterData.SetFormat(self, fmt)

    @smproperty.stringvector(name="Delimiter", default_values=',')
    def SetDelimiter(self, delimiter):
        """The string delimiter to use"""
        WriteCellCenterData.SetDelimiter(self, delimiter)

###############################################################################

ESRI_DESC = "Esri Grid"
ESRI_EXTS = "asc dem txt"

@smproxy.reader(name="PVGeoEsriGridReader",
       label="PVGeo: Esri ASCII Grid Reader",
       extensions=ESRI_EXTS,
       file_description=ESRI_DESC)
class PVGeoEsriGridReader(EsriGridReader):
    def __init__(self):
        EsriGridReader.__init__(self)

    #### Seters and Geters ####

    @smproperty.xml(_helpers.getFileReaderXml(ESRI_EXTS, readerDescription=ESRI_DESC))
    def AddFileName(self, fname):
        EsriGridReader.AddFileName(self, fname)

    @smproperty.stringvector(name='DataName', default_values='Data')
    def SetDataName(self, dataName):
        EsriGridReader.SetDataName(self, dataName)


###############################################################################
