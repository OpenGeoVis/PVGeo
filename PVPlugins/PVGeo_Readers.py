paraview_plugin_version = '2.0.0'
# This is module to import. It provides VTKPythonAlgorithmBase, the base class
# for all python-based vtkAlgorithm subclasses in VTK and decorators used to
# 'register' the algorithm with ParaView along with information about UI.
from paraview.util.vtkAlgorithm import *

# Helpers:
from PVGeo import _helpers
# Classes to Decorate
from PVGeo.readers import PackedBinariesReader, MadagascarReader
from PVGeo.readers import DelimitedTextReader, XYZTextReader


###############################################################################



@smproxy.reader(name="PVGeoPackedBinariesReader",
       label='PVGeo: %s'%PackedBinariesReader.__displayname__,
       extensions=PackedBinariesReader.extensions,
       file_description=PackedBinariesReader.description)
class PVGeoPackedBinariesReader(PackedBinariesReader):
    def __init__(self):
        PackedBinariesReader.__init__(self)

    #### Seters and Geters ####
    @smproperty.xml(_helpers.get_file_reader_xml(PackedBinariesReader.extensions, reader_description=PackedBinariesReader.description))
    def AddFileName(self, filename):
        PackedBinariesReader.AddFileName(self, filename)



    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def set_time_delta(self, dt):
        PackedBinariesReader.set_time_delta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def get_time_step_values(self):
        """This is critical for registering the timesteps"""
        return PackedBinariesReader.get_time_step_values(self)

    @smproperty.xml(_helpers.get_drop_down_xml('Endian','set_endian',
        ['Native', 'Little-Endian', 'Big-Endian'],
        help='This is the type memory endianness.'))
    def set_endian(self, endian):
        PackedBinariesReader.set_endian(self, endian)

    @smproperty.xml(_helpers.get_drop_down_xml('DataType','set_data_type',
        ['Float64', 'Float32', 'Integer4'],
        help='This is data type to read.'))
    def set_data_type(self, dtype):
        PackedBinariesReader.set_data_type(self, dtype)


    @smproperty.stringvector(name='DataName', default_values='Data')
    def set_data_name(self, data_name):
        PackedBinariesReader.set_data_name(self, data_name)


###############################################################################



@smproxy.reader(name="PVGeoMadagascarReader",
       label='PVGeo: %s'%MadagascarReader.__displayname__,
       extensions=MadagascarReader.extensions,
       file_description=MadagascarReader.description)
class PVGeoMadagascarReader(MadagascarReader):
    def __init__(self):
        MadagascarReader.__init__(self)

    #### Seters and Geters ####


    @smproperty.xml(_helpers.get_file_reader_xml(MadagascarReader.extensions, reader_description=MadagascarReader.description))
    def AddFileName(self, filename):
        MadagascarReader.AddFileName(self, filename)


    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def set_time_delta(self, dt):
        MadagascarReader.set_time_delta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def get_time_step_values(self):
        """This is critical for registering the timesteps"""
        return MadagascarReader.get_time_step_values(self)

    @smproperty.xml(_helpers.get_drop_down_xml('Endian','set_endian',
        ['Native', 'Little-Endian', 'Big-Endian'],
        help='This is the type memory endianness.'))
    def set_endian(self, endian):
        MadagascarReader.set_endian(self, endian)

    @smproperty.xml(_helpers.get_drop_down_xml('DataType','set_data_type',
        ['Float64', 'Float32', 'Integer4'],
        help='This is data type to read.'))
    def set_data_type(self, dtype):
        MadagascarReader.set_data_type(self, dtype)


    @smproperty.stringvector(name='DataName', default_values='Data')
    def set_data_name(self, data_name):
        MadagascarReader.set_data_name(self, data_name)



###############################################################################



@smproxy.reader(name="PVGeoDelimitedTextReader",
       label='PVGeo: %s'%DelimitedTextReader.__displayname__,
       extensions=DelimitedTextReader.extensions,
       file_description=DelimitedTextReader.description)
class PVGeoDelimitedTextReader(DelimitedTextReader):
    def __init__(self):
        DelimitedTextReader.__init__(self)


    #### Seters and Geters ####
    @smproperty.xml(_helpers.get_file_reader_xml(DelimitedTextReader.extensions, reader_description=DelimitedTextReader.description))
    def AddFileName(self, filename):
        DelimitedTextReader.AddFileName(self, filename)



    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def set_time_delta(self, dt):
        DelimitedTextReader.set_time_delta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def get_time_step_values(self):
        """This is critical for registering the timesteps"""
        return DelimitedTextReader.get_time_step_values(self)

    @smproperty.stringvector(name="Delimiter", default_values=" ")
    def set_delimiter(self, deli):
        DelimitedTextReader.set_delimiter(self, deli)

    @smproperty.xml(_helpers.get_property_xml(name='Use Split on Whitespace', command='set_split_on_white_space', default_values=False, help='A boolean to override the Delimiter_Field and use whitespace as delimiter.'))
    def set_split_on_white_space(self, flag):
        DelimitedTextReader.set_split_on_white_space(self, flag)

    @smproperty.intvector(name="SkipRows", default_values=0)
    def set_skip_rows(self, skip):
        DelimitedTextReader.set_skip_rows(self, skip)

    @smproperty.stringvector(name="Comments", default_values="!")
    def set_comments(self, identifier):
        DelimitedTextReader.set_comments(self, identifier)

    @smproperty.xml(_helpers.get_property_xml(name='Has Titles', command='set_has_titles', default_values=False, help='A boolean for if the delimited file has header titles for the data arrays.'))
    def set_has_titles(self, flag):
        DelimitedTextReader.set_has_titles(self, flag)



###############################################################################



@smproxy.reader(name="PVGeoXYZTextReader",
       label='PVGeo: %s'%XYZTextReader.__displayname__,
       extensions=XYZTextReader.extensions,
       file_description=XYZTextReader.description)
class PVGeoXYZTextReader(XYZTextReader):
    def __init__(self):
        XYZTextReader.__init__(self)


    #### Seters and Geters ####
    @smproperty.xml(_helpers.get_file_reader_xml(XYZTextReader.extensions, reader_description=XYZTextReader.description))
    def AddFileName(self, filename):
        XYZTextReader.AddFileName(self, filename)



    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def set_time_delta(self, dt):
        XYZTextReader.set_time_delta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def get_time_step_values(self):
        """This is critical for registering the timesteps"""
        return XYZTextReader.get_time_step_values(self)

    @smproperty.stringvector(name="Delimiter", default_values=" ")
    def set_delimiter(self, deli):
        XYZTextReader.set_delimiter(self, deli)

    @smproperty.xml(_helpers.get_property_xml(name='Use Split on Whitespace', command='set_split_on_white_space', default_values=False, help='A boolean to override the Delimiter_Field and use whitespace as delimiter.'))
    def set_split_on_white_space(self, flag):
        XYZTextReader.set_split_on_white_space(self, flag)

    @smproperty.intvector(name="SkipRows", default_values=0)
    def set_skip_rows(self, skip):
        XYZTextReader.set_skip_rows(self, skip)

    @smproperty.stringvector(name="Comments", default_values="!")
    def set_comments(self, identifier):
        XYZTextReader.set_comments(self, identifier)
