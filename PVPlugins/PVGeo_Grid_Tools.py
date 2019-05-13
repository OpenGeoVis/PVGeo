paraview_plugin_version = '2.0.0'
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

    @smproperty.xml(_helpers.get_property_xml(name='Flip X Axis', command='set_flip_x', default_values=True, help='A boolean to set whether to flip the X axis.'))
    def set_flip_x(self, flag):
        ReverseImageDataAxii.set_flip_x(self, flag)

    @smproperty.xml(_helpers.get_property_xml(name='Flip Y Axis', command='set_flip_y', default_values=True, help='A boolean to set whether to flip the Y axis.'))
    def set_flip_y(self, flag):
        ReverseImageDataAxii.set_flip_y(self, flag)

    @smproperty.xml(_helpers.get_property_xml(name='Flip Z Axis', command='set_flip_z', default_values=True, help='A boolean to set whether to flip the Z axis.'))
    def set_flip_z(self, flag):
        ReverseImageDataAxii.set_flip_z(self, flag)


###############################################################################


@smproxy.filter(name='PVGeoTranslateGridOrigin', label=TranslateGridOrigin.__displayname__)
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkImageData"], composite_data_supported=True)
class PVGeoTranslateGridOrigin(TranslateGridOrigin):
    def __init__(self):
        TranslateGridOrigin.__init__(self)

    #### Seters and Geters ####

    @smproperty.xml(_helpers.get_drop_down_xml(name='Corner', command='set_corner',
        labels=['South East Bottom', 'North West Bottom', 'North East Bottom',
        'South West Top', 'South East Top', 'North West Top', 'North East Top'],
        values=[1,2,3,4,5,6,7]))
    def set_corner(self, corner):
        TranslateGridOrigin.set_corner(self, corner)



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
    def set_extent(self, nx, ny, nz, nt):
        TableToTimeGrid.set_extent(self, nx, ny, nz, nt)

    @smproperty.intvector(name="Dimensions", default_values=[0, 1, 2, 3])
    def set_dimensions(self, x, y, z, t):
        TableToTimeGrid.set_dimensions(self, x, y, z, t)

    @smproperty.doublevector(name="Spacing", default_values=[1.0, 1.0, 1.0])
    def set_spacing(self, dx, dy, dz):
        TableToTimeGrid.set_spacing(self, dx, dy, dz)

    @smproperty.doublevector(name="Origin", default_values=[0.0, 0.0, 0.0])
    def set_origin(self, x0, y0, z0):
        TableToTimeGrid.set_origin(self, x0, y0, z0)


    @smproperty.xml(_helpers.get_drop_down_xml(name='Order', command='set_order',
        labels=['C-style: Row-major order', 'Fortran-style: column-major order'],
        values=[0, 1]))
    def set_order(self, order):
        o = ['C', 'F']
        TableToTimeGrid.set_order(self, o[order])

    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def set_time_delta(self, dt):
        TableToTimeGrid.set_time_delta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def get_time_step_values(self):
        """This is critical for registering the timesteps"""
        return TableToTimeGrid.get_time_step_values(self)

    @smproperty.xml(_helpers.get_property_xml(name='Use Point Data', command='set_use_points', default_values=False, panel_visibility='advanced', help='Set whether or not to place the data on the nodes/cells of the grid. In ParaView, switching can be a bit buggy: be sure to turn the visibility of this data object OFF on the pipeline when changing bewteen nodes/cells.'))
    def set_use_points(self, flag):
        TableToTimeGrid.set_use_points(self, flag)




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
    def set_tolerance(self, tol):
        ExtractTopography.set_tolerance(self, tol)

    @smproperty.doublevector(name="Offset", default_values=0.0)
    def set_offset(self, offset):
        ExtractTopography.set_offset(self, offset)

    @smproperty.xml(_helpers.get_drop_down_xml(name='Operation', command='set_operation', labels=ExtractTopography.get_operation_names(), help='This is the type of extraction operation to apply'))
    def set_operation(self, op):
        ExtractTopography.set_operation(self, op)

    @smproperty.xml(_helpers.get_property_xml(name='Invert',
        command='set_invert',
        default_values=False,
        help='A boolean to set whether on whether to invert the extraction.'))
    def set_invert(self, flag):
        ExtractTopography.set_invert(self, flag)

###############################################################################


@smproxy.reader(name="PVGeoSurferGridReader",
       label='PVGeo: %s'%SurferGridReader.__displayname__,
       extensions=SurferGridReader.extensions,
       file_description=SurferGridReader.description)
class PVGeoSurferGridReader(SurferGridReader):
    def __init__(self):
        SurferGridReader.__init__(self)

    #### Seters and Geters ####

    @smproperty.xml(_helpers.get_file_reader_xml(SurferGridReader.extensions, reader_description=SurferGridReader.description))
    def AddFileName(self, filename):
        SurferGridReader.AddFileName(self, filename)

    @smproperty.stringvector(name='DataName', default_values='Data')
    def set_data_name(self, data_name):
        SurferGridReader.set_data_name(self, data_name)

    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def set_time_delta(self, dt):
        SurferGridReader.set_time_delta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def get_time_step_values(self):
        """This is critical for registering the timesteps"""
        return SurferGridReader.get_time_step_values(self)


###############################################################################


@smproxy.writer(extensions="grd", file_description="Surfer Grid (ASCII)", support_reload=False)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkImageData", "vtkMultiBlockDataSet"], composite_data_supported=True)
class PVGeoWriteImageDataToSurfer(WriteImageDataToSurfer):
    def __init__(self):
        WriteImageDataToSurfer.__init__(self)

    @smproperty.stringvector(name="FileName", panel_visibility="never")
    @smdomain.filelist()
    def SetFileName(self, filename):
        """Specify filename for the file to write."""
        WriteImageDataToSurfer.SetFileName(self, filename)

    @smproperty.xml(_helpers.get_input_array_xml(nInputPorts=1, n_arrays=1))
    def SetInputArrayToProcess(self, idx, port, connection, field, name):
        return WriteImageDataToSurfer.SetInputArrayToProcess(self, idx, port, connection, field, name)

    @smproperty.stringvector(name="Format", default_values='%.9e')
    def set_format(self, fmt):
        """Use to set the ASCII format for the writer default is ``'%.9e'``"""
        WriteImageDataToSurfer.set_format(self, fmt)



###############################################################################

@smproxy.writer(extensions="dat", file_description="Cell Centers and Cell Data", support_reload=False)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkDataSet"], composite_data_supported=True)
class PVGeoWriteCellCenterData(WriteCellCenterData):
    def __init__(self):
        WriteCellCenterData.__init__(self)


    @smproperty.stringvector(name="FileName", panel_visibility="never")
    @smdomain.filelist()
    def SetFileName(self, filename):
        """Specify filename for the file to write."""
        WriteCellCenterData.SetFileName(self, filename)

    @smproperty.stringvector(name="Format", default_values='%.9e')
    def set_format(self, fmt):
        """Use to set the ASCII format for the writer default is ``'%.9e'``"""
        WriteCellCenterData.set_format(self, fmt)

    @smproperty.stringvector(name="Delimiter", default_values=',')
    def set_delimiter(self, deli):
        """The string delimiter to use"""
        WriteCellCenterData.set_delimiter(self, deli)

###############################################################################


@smproxy.reader(name="PVGeoEsriGridReader",
       label='PVGeo: %s'%EsriGridReader.__displayname__,
       extensions=EsriGridReader.extensions,
       file_description=EsriGridReader.description)
class PVGeoEsriGridReader(EsriGridReader):
    def __init__(self):
        EsriGridReader.__init__(self)

    #### Seters and Geters ####

    @smproperty.xml(_helpers.get_file_reader_xml(EsriGridReader.extensions, reader_description=EsriGridReader.description))
    def AddFileName(self, filename):
        EsriGridReader.AddFileName(self, filename)

    @smproperty.stringvector(name='DataName', default_values='Data')
    def set_data_name(self, data_name):
        EsriGridReader.set_data_name(self, data_name)

    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def set_time_delta(self, dt):
        EsriGridReader.set_time_delta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def get_time_step_values(self):
        """This is critical for registering the timesteps"""
        return EsriGridReader.get_time_step_values(self)



###############################################################################


@smproxy.reader(name="PVGeoLandsatReader",
       label='PVGeo: %s'%LandsatReader.__displayname__,
       extensions=LandsatReader.extensions,
       file_description=LandsatReader.description)
class PVGeoLandsatReader(LandsatReader):
    def __init__(self):
        LandsatReader.__init__(self)

    #### Seters and Geters ####

    @smproperty.xml(_helpers.get_file_reader_xml(LandsatReader.extensions, reader_description=LandsatReader.description))
    def AddFileName(self, filename):
        LandsatReader.AddFileName(self, filename)

    @smproperty.dataarrayselection(name="Available Bands")
    def GetDataSelection(self):
        return LandsatReader.GetDataSelection(self)


    @smproperty.xml(_helpers.get_property_xml(name='Cast Data Type',
        command='set_cast_data_type',
        default_values=True,
        help='A boolean to set whether to cast the data arrays so invalid points are filled nans.',
        panel_visibility='advanced'))
    def set_cast_data_type(self, flag):
        LandsatReader.set_cast_data_type(self, flag)


    @smproperty.xml(_helpers.get_drop_down_xml(name='Color Scheme', command='set_color_scheme', labels=LandsatReader.get_color_scheme_names(), help='Set a color scheme to use.'))
    def set_color_scheme(self, scheme):
        LandsatReader.set_color_scheme(self, scheme)


###############################################################################
