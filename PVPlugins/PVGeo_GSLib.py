paraview_plugin_version = '1.1.11'
# This is module to import. It provides VTKPythonAlgorithmBase, the base class
# for all python-based vtkAlgorithm subclasses in VTK and decorators used to
# 'register' the algorithm with ParaView along with information about UI.
from paraview.util.vtkAlgorithm import *

# Helpers:
from PVGeo import _helpers
# Classes to Decorate
from PVGeo.gslib import GSLibReader, SGeMSGridReader

###############################################################################

@smproxy.reader(name="PVGeoGSLibReader",
       label="PVGeo: GSLib File Format",
       extensions="sgems dat geoeas gslib GSLIB txt SGEMS",
       file_description="GSLib Table")
class PVGeoGSLibReader(GSLibReader):
    def __init__(self):
        GSLibReader.__init__(self)

    #### Seters and Geters ####
    # @smproperty.stringvector(name="FileNames", panel_visibility="advanced")
    # @smdomain.filelist()
    # @smhint.filechooser(extensions="sgems dat geoeas gslib GSLIB txt SGEMS", file_description="GSLib Tables")
    @smproperty.xml(_helpers.getFileReaderXml("sgems dat geoeas gslib GSLIB txt SGEMS", readerDescription='GSLib Table'))
    def AddFileName(self, fname):
        GSLibReader.AddFileName(self, fname)

    @smproperty.stringvector(name="Delimiter", default_values=" ")
    def SetDelimiter(self, deli):
        GSLibReader.SetDelimiter(self, deli)

    @smproperty.xml(_helpers.getPropertyXml(name='Use Tab Delimiter', command='SetUseTab', default_values=False, help='A boolean to override the Delimiter_Field and use a Tab delimiter.'))
    def SetUseTab(self, flag):
        GSLibReader.SetUseTab(self, flag)

    @smproperty.intvector(name="SkipRows", default_values=0)
    def SetSkipRows(self, skip):
        GSLibReader.SetSkipRows(self, skip)

    @smproperty.stringvector(name="Comments", default_values="#")
    def SetComments(self, identifier):
        GSLibReader.SetComments(self, identifier)

    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def SetTimeDelta(self, dt):
        GSLibReader.SetTimeDelta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def GetTimestepValues(self):
        """This is critical for registering the timesteps"""
        return GSLibReader.GetTimestepValues(self)

    @smproperty.xml("""<Property name="Print File Header" command="PrintFileHeader" panel_widget="command_button"/>""")
    def PrintFileHeader(self):
        print(GSLibReader.GetFileHeader(self))
        return 1




###############################################################################


@smproxy.reader(name="PVGeoSGeMSGridReader",
       label="PVGeo: SGeMS Grid Reader",
       extensions="dat gslib sgems SGEMS",
       file_description="SGeMS Uniform Grid")
@smhint.xml('''<RepresentationType view="RenderView" type="Surface" />''')
class PVGeoSGeMSGridReader(SGeMSGridReader):
    def __init__(self):
        SGeMSGridReader.__init__(self)


    #### Seters and Geters ####
    @smproperty.xml(_helpers.getFileReaderXml("sgems dat geoeas gslib GSLIB txt SGEMS", readerDescription='GSLib Table'))
    def AddFileName(self, fname):
        SGeMSGridReader.AddFileName(self, fname)

    @smproperty.stringvector(name="Delimiter", default_values=" ")
    def SetDelimiter(self, deli):
        SGeMSGridReader.SetDelimiter(self, deli)

    @smproperty.xml(_helpers.getPropertyXml(name='Use Tab Delimiter', command='SetUseTab', default_values=False, help='A boolean to override the Delimiter_Field and use a Tab delimiter.'))
    def SetUseTab(self, flag):
        SGeMSGridReader.SetUseTab(self, flag)

    @smproperty.intvector(name="SkipRows", default_values=0)
    def SetSkipRows(self, skip):
        SGeMSGridReader.SetSkipRows(self, skip)

    @smproperty.stringvector(name="Comments", default_values="#")
    def SetComments(self, identifier):
        SGeMSGridReader.SetComments(self, identifier)

    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def SetTimeDelta(self, dt):
        SGeMSGridReader.SetTimeDelta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def GetTimestepValues(self):
        """This is critical for registering the timesteps"""
        return SGeMSGridReader.GetTimestepValues(self)

    @smproperty.doublevector(name="Spacing", default_values=[1.0, 1.0, 1.0],)
    def SetSpacing(self, dx, dy, dz):
        SGeMSGridReader.SetSpacing(self, dx, dy, dz)

    @smproperty.doublevector(name="Origin", default_values=[0.0, 0.0, 0.0],)
    def SetOrigin(self, ox, oy, oz):
        SGeMSGridReader.SetOrigin(self, ox, oy, oz)
