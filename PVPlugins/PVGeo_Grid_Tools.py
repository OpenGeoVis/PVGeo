paraview_plugin_version = '1.2.3'
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


@smproxy.filter(name='PVGeoReverseImageDataAxii', label=ReverseImageDataAxii.__displayname__)
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


@smproxy.filter(name='PVGeoTranslateGridOrigin', label=TranslateGridOrigin.__displayname__)
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


@smproxy.filter(name='PVGeoTableToTimeGrid', label=TableToTimeGrid.__displayname__)
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkTable"], composite_data_supported=True)
class PVGeoTableToTimeGrid(TableToTimeGrid):
    def __init__(self):
        TableToTimeGrid.__init__(self)


    #### Setters / Getters ####


    @smproperty.intvector(name="Extent", default_values=[10, 10, 10, 1])
    def SetExtent(self, nx, ny, nz, nt):
        TableToTimeGrid.SetExtent(self, nx, ny, nz, nt)

    @smproperty.intvector(name="Dimensions", default_values=[0, 1, 2, 3])
    def SetDimensions(self, x, y, z, t):
        TableToTimeGrid.SetDimensions(self, x, y, z, t)

    @smproperty.doublevector(name="Spacing", default_values=[1.0, 1.0, 1.0])
    def SetSpacing(self, dx, dy, dz):
        TableToTimeGrid.SetSpacing(self, dx, dy, dz)

    @smproperty.doublevector(name="Origin", default_values=[0.0, 0.0, 0.0])
    def SetOrigin(self, x0, y0, z0):
        TableToTimeGrid.SetOrigin(self, x0, y0, z0)


    @smproperty.xml(_helpers.getDropDownXml(name='Order', command='SetOrder',
        labels=['C-style: Row-major order', 'Fortran-style: column-major order'],
        values=[0, 1]))
    def SetOrder(self, order):
        o = ['C', 'F']
        TableToTimeGrid.SetOrder(self, o[order])

    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def SetTimeDelta(self, dt):
        TableToTimeGrid.SetTimeDelta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def GetTimestepValues(self):
        """This is critical for registering the timesteps"""
        return TableToTimeGrid.GetTimestepValues(self)

    @smproperty.xml(_helpers.getPropertyXml(name='Use Point Data', command='SetUsePoints', default_values=False, panel_visibility='advanced', help='Set whether or not to place the data on the nodes/cells of the grid. In ParaView, switching can be a bit buggy: be sure to turn the visibility of this data object OFF on the pipeline when changing bewteen nodes/cells.'))
    def SetUsePoints(self, flag):
        TableToTimeGrid.SetUsePoints(self, flag)




###############################################################################


@smproxy.filter(name='PVGeoExtractTopography', label=ExtractTopography.__displayname__)
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

    @smproperty.doublevector(name="Offset", default_values=0.0)
    def SetOffset(self, offset):
        ExtractTopography.SetOffset(self, offset)

    @smproperty.xml(_helpers.getDropDownXml(name='Operation', command='SetOperation', labels=ExtractTopography.GetOperationNames(), help='This is the type of extraction operation to apply'))
    def SetOperation(self, op):
        ExtractTopography.SetOperation(self, op)

    @smproperty.xml(_helpers.getPropertyXml(name='Invert',
        command='SetInvert',
        default_values=False,
        help='A boolean to set whether on whether to invert the extraction.'))
    def SetInvert(self, flag):
        ExtractTopography.SetInvert(self, flag)

###############################################################################


@smproxy.reader(name="PVGeoSurferGridReader",
       label='PVGeo: %s'%SurferGridReader.__displayname__,
       extensions=SurferGridReader.extensions,
       file_description=SurferGridReader.description)
class PVGeoSurferGridReader(SurferGridReader):
    def __init__(self):
        SurferGridReader.__init__(self)

    #### Seters and Geters ####

    @smproperty.xml(_helpers.getFileReaderXml(SurferGridReader.extensions, readerDescription=SurferGridReader.description))
    def AddFileName(self, fname):
        SurferGridReader.AddFileName(self, fname)

    @smproperty.stringvector(name='DataName', default_values='Data')
    def SetDataName(self, dataName):
        SurferGridReader.SetDataName(self, dataName)

    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def SetTimeDelta(self, dt):
        SurferGridReader.SetTimeDelta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def GetTimestepValues(self):
        """This is critical for registering the timesteps"""
        return SurferGridReader.GetTimestepValues(self)


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


@smproxy.reader(name="PVGeoEsriGridReader",
       label='PVGeo: %s'%EsriGridReader.__displayname__,
       extensions=EsriGridReader.extensions,
       file_description=EsriGridReader.description)
class PVGeoEsriGridReader(EsriGridReader):
    def __init__(self):
        EsriGridReader.__init__(self)

    #### Seters and Geters ####

    @smproperty.xml(_helpers.getFileReaderXml(EsriGridReader.extensions, readerDescription=EsriGridReader.description))
    def AddFileName(self, fname):
        EsriGridReader.AddFileName(self, fname)

    @smproperty.stringvector(name='DataName', default_values='Data')
    def SetDataName(self, dataName):
        EsriGridReader.SetDataName(self, dataName)

    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def SetTimeDelta(self, dt):
        EsriGridReader.SetTimeDelta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def GetTimestepValues(self):
        """This is critical for registering the timesteps"""
        return EsriGridReader.GetTimestepValues(self)



###############################################################################


@smproxy.reader(name="PVGeoLandsatReader",
       label='PVGeo: %s'%LandsatReader.__displayname__,
       extensions=LandsatReader.extensions,
       file_description=LandsatReader.description)
class PVGeoLandsatReader(LandsatReader):
    def __init__(self):
        LandsatReader.__init__(self)

    #### Seters and Geters ####

    @smproperty.xml(_helpers.getFileReaderXml(LandsatReader.extensions, readerDescription=LandsatReader.description))
    def AddFileName(self, fname):
        LandsatReader.AddFileName(self, fname)

    @smproperty.dataarrayselection(name="Available Bands")
    def GetDataSelection(self):
        return LandsatReader.GetDataSelection(self)


    @smproperty.xml(_helpers.getPropertyXml(name='Cast Data Type',
        command='CastDataType',
        default_values=True,
        help='A boolean to set whether to cast the data arrays so invalid points are filled nans.',
        panel_visibility='advanced'))
    def CastDataType(self, flag):
        LandsatReader.CastDataType(self, flag)


    @smproperty.xml(_helpers.getDropDownXml(name='Color Scheme', command='SetColorScheme', labels=LandsatReader.GetColorSchemeNames(), help='Set a color scheme to use.'))
    def SetColorScheme(self, scheme):
        LandsatReader.SetColorScheme(self, scheme)


###############################################################################
