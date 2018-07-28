paraview_plugin_version = '1.1.10'
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


PACKED_EXTS = 'H@ bin rsf rsf@ HH npz'
PACKED_DESC = 'Packed Binaries Reader'

@smproxy.reader(name="PVGeoPackedBinariesReader",
       label="PVGeo: Packed Binaries Reader",
       extensions=PACKED_EXTS,
       file_description=PACKED_DESC)
class PVGeoPackedBinariesReader(PackedBinariesReader):
    def __init__(self):
        PackedBinariesReader.__init__(self)

    #### Seters and Geters ####
    @smproperty.xml(_helpers.getFileReaderXml(PACKED_EXTS, readerDescription=PACKED_DESC))
    def AddFileName(self, fname):
        PackedBinariesReader.AddFileName(self, fname)



    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def SetTimeDelta(self, dt):
        PackedBinariesReader.SetTimeDelta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def GetTimestepValues(self):
        """This is critical for registering the timesteps"""
        return PackedBinariesReader.GetTimestepValues(self)

    @smproperty.xml(_helpers.getDropDownXml('Endian','SetEndian',
        ['Native', 'Little-Endian', 'Big-Endian'],
        help='This is the type memory endianness.'))
    def SetEndian(self, endian):
        PackedBinariesReader.SetEndian(self, endian)

    @smproperty.xml(_helpers.getDropDownXml('DataType','SetDataType',
        ['Float64', 'Float32', 'Integer4'],
        help='This is data type to read.'))
    def SetDataType(self, dtype):
        PackedBinariesReader.SetDataType(self, dtype)


    @smproperty.stringvector(name='DataName', default_values='Data')
    def SetDataName(self, dataName):
        PackedBinariesReader.SetDataName(self, dataName)


###############################################################################


MADAGASCAR_EXTS = 'bin H@ rsf rsf@ HH'
MADAGASCAR_DESC = 'Madagascar Single Stream RSF Files'

@smproxy.reader(name="PVGeoMadagascarReader",
       label="PVGeo: Madagascar SSRSF  Reader",
       extensions=MADAGASCAR_EXTS,
       file_description=MADAGASCAR_DESC)
class PVGeoMadagascarReader(MadagascarReader):
    def __init__(self):
        MadagascarReader.__init__(self)

    #### Seters and Geters ####


    @smproperty.xml(_helpers.getFileReaderXml(MADAGASCAR_EXTS, readerDescription=MADAGASCAR_DESC))
    def AddFileName(self, fname):
        MadagascarReader.AddFileName(self, fname)


    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def SetTimeDelta(self, dt):
        MadagascarReader.SetTimeDelta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def GetTimestepValues(self):
        """This is critical for registering the timesteps"""
        return MadagascarReader.GetTimestepValues(self)

    @smproperty.xml(_helpers.getDropDownXml('Endian','SetEndian',
        ['Native', 'Little-Endian', 'Big-Endian'],
        help='This is the type memory endianness.'))
    def SetEndian(self, endian):
        MadagascarReader.SetEndian(self, endian)

    @smproperty.xml(_helpers.getDropDownXml('DataType','SetDataType',
        ['Float64', 'Float32', 'Integer4'],
        help='This is data type to read.'))
    def SetDataType(self, dtype):
        MadagascarReader.SetDataType(self, dtype)


    @smproperty.stringvector(name='DataName', default_values='Data')
    def SetDataName(self, dataName):
        MadagascarReader.SetDataName(self, dataName)



###############################################################################


DELIMITED_EXTS = 'dat csv txt text ascii xyz'
DELIMITED_DESC = 'Delimited Text Files'

@smproxy.reader(name="PVGeoDelimitedTextReader",
       label="PVGeo: Delimited Text Reader",
       extensions=DELIMITED_EXTS,
       file_description=DELIMITED_DESC)
class PVGeoDelimitedTextReader(DelimitedTextReader):
    def __init__(self):
        DelimitedTextReader.__init__(self)


    #### Seters and Geters ####
    @smproperty.xml(_helpers.getFileReaderXml(DELIMITED_EXTS, readerDescription=DELIMITED_DESC))
    def AddFileName(self, fname):
        DelimitedTextReader.AddFileName(self, fname)



    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def SetTimeDelta(self, dt):
        DelimitedTextReader.SetTimeDelta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def GetTimestepValues(self):
        """This is critical for registering the timesteps"""
        return DelimitedTextReader.GetTimestepValues(self)

    @smproperty.stringvector(name="Delimiter", default_values=" ")
    def SetDelimiter(self, deli):
        DelimitedTextReader.SetDelimiter(self, deli)

    @smproperty.xml(_helpers.getPropertyXml(name='Use Tab Delimiter', command='SetUseTab', default_values=False, help='A boolean to override the Delimiter_Field and use a Tab delimiter.'))
    def SetUseTab(self, flag):
        DelimitedTextReader.SetUseTab(self, flag)

    @smproperty.intvector(name="SkipRows", default_values=0)
    def SetSkipRows(self, skip):
        DelimitedTextReader.SetSkipRows(self, skip)

    @smproperty.stringvector(name="Comments", default_values="#")
    def SetComments(self, identifier):
        DelimitedTextReader.SetComments(self, identifier)

    @smproperty.xml(_helpers.getPropertyXml(name='Has Titles', command='SetHasTitles', default_values=True, help='A boolean for if the delimited file has header titles for the data arrays.'))
    def SetHasTitles(self, flag):
        DelimitedTextReader.SetHasTitles(self, flag)



###############################################################################


XYZ_EXTS = 'xyz text txt dat csv tsv'
XYZ_DESC = 'XYZ Delimited Text Files where header has comma delimiter.'

@smproxy.reader(name="PVGeoXYZTextReader",
       label="PVGeo: XYZ File Reader",
       extensions=XYZ_EXTS,
       file_description=XYZ_DESC)
class PVGeoXYZTextReader(XYZTextReader):
    def __init__(self):
        XYZTextReader.__init__(self)


    #### Seters and Geters ####
    @smproperty.xml(_helpers.getFileReaderXml(XYZ_EXTS, readerDescription=XYZ_DESC))
    def AddFileName(self, fname):
        XYZTextReader.AddFileName(self, fname)



    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def SetTimeDelta(self, dt):
        XYZTextReader.SetTimeDelta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def GetTimestepValues(self):
        """This is critical for registering the timesteps"""
        return XYZTextReader.GetTimestepValues(self)

    @smproperty.stringvector(name="Delimiter", default_values=" ")
    def SetDelimiter(self, deli):
        XYZTextReader.SetDelimiter(self, deli)

    @smproperty.xml(_helpers.getPropertyXml(name='Use Tab Delimiter', command='SetUseTab', default_values=False, help='A boolean to override the Delimiter_Field and use a Tab delimiter.'))
    def SetUseTab(self, flag):
        XYZTextReader.SetUseTab(self, flag)

    @smproperty.intvector(name="SkipRows", default_values=0)
    def SetSkipRows(self, skip):
        XYZTextReader.SetSkipRows(self, skip)

    @smproperty.stringvector(name="Comments", default_values="#")
    def SetComments(self, identifier):
        XYZTextReader.SetComments(self, identifier)
