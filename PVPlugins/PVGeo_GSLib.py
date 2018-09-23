paraview_plugin_version = '1.1.29'
# This is module to import. It provides VTKPythonAlgorithmBase, the base class
# for all python-based vtkAlgorithm subclasses in VTK and decorators used to
# 'register' the algorithm with ParaView along with information about UI.
from paraview.util.vtkAlgorithm import *

# Helpers:
from PVGeo import _helpers
# Classes to Decorate
from PVGeo.gslib import *

###############################################################################


GSLIB_EXTS = "sgems dat geoeas gslib GSLIB txt SGEMS SGeMS"
GSLIB_DESC = "GSLib Table"

@smproxy.reader(name="PVGeoGSLibReader",
       label="PVGeo: GSLib File Format",
       extensions=GSLIB_EXTS,
       file_description=GSLIB_DESC)
class PVGeoGSLibReader(GSLibReader):
    def __init__(self):
        GSLibReader.__init__(self)

    #### Seters and Geters ####

    @smproperty.xml(_helpers.getFileReaderXml(GSLIB_EXTS, readerDescription=GSLIB_DESC))
    def AddFileName(self, fname):
        GSLibReader.AddFileName(self, fname)

    @smproperty.stringvector(name="Delimiter", default_values=" ")
    def SetDelimiter(self, deli):
        GSLibReader.SetDelimiter(self, deli)

    @smproperty.xml(_helpers.getPropertyXml(name='Use Split on Whitespace', command='SetSplitOnWhiteSpace', default_values=False, help='A boolean to override the Delimiter_Field and use whitespace as delimiter.'))
    def SetSplitOnWhiteSpace(self, flag):
        GSLibReader.SetSplitOnWhiteSpace(self, flag)

    @smproperty.intvector(name="SkipRows", default_values=0)
    def SetSkipRows(self, skip):
        GSLibReader.SetSkipRows(self, skip)

    @smproperty.stringvector(name="Comments", default_values="!")
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

SGEMS_DESC = "SGeMS Uniform Grid"

@smproxy.reader(name="PVGeoSGeMSGridReader",
       label="PVGeo: SGeMS Grid Reader",
       extensions=GSLIB_EXTS,
       file_description=SGEMS_DESC)
@smhint.xml('''<RepresentationType view="RenderView" type="Surface" />''')
class PVGeoSGeMSGridReader(SGeMSGridReader):
    def __init__(self):
        SGeMSGridReader.__init__(self)


    #### Seters and Geters ####
    @smproperty.xml(_helpers.getFileReaderXml(GSLIB_EXTS, readerDescription=SGEMS_DESC))
    def AddFileName(self, fname):
        SGeMSGridReader.AddFileName(self, fname)

    @smproperty.stringvector(name="Delimiter", default_values=" ")
    def SetDelimiter(self, deli):
        SGeMSGridReader.SetDelimiter(self, deli)

    @smproperty.xml(_helpers.getPropertyXml(name='Use Split on Whitespace', command='SetSplitOnWhiteSpace', default_values=False, help='A boolean to override the Delimiter_Field and use whitespace as delimiter.'))
    def SetSplitOnWhiteSpace(self, flag):
        SGeMSGridReader.SetSplitOnWhiteSpace(self, flag)

    @smproperty.intvector(name="SkipRows", default_values=0)
    def SetSkipRows(self, skip):
        SGeMSGridReader.SetSkipRows(self, skip)

    @smproperty.stringvector(name="Comments", default_values="!")
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


###############################################################################


@smproxy.writer(extensions="SGeMS", file_description="SGeMS Uniform Grid", support_reload=False)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkImageData"], composite_data_supported=True)
class PVGeoWriteImageDataToSGeMS(WriteImageDataToSGeMS):
    def __init__(self):
        WriteImageDataToSGeMS.__init__(self)

    @smproperty.stringvector(name="FileName", panel_visibility="never")
    @smdomain.filelist()
    def SetFileName(self, fname):
        """Specify filename for the file to write."""
        WriteImageDataToSGeMS.SetFileName(self, fname)

    @smproperty.stringvector(name="Format", default_values='%.9e')
    def SetFormat(self, fmt):
        """Use to set the ASCII format for the writer default is ``'%.9e'``"""
        WriteImageDataToSGeMS.SetFormat(self, fmt)

###############################################################################

@smproxy.writer(extensions="gslib", file_description="GSLib Table", support_reload=False)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkTable"], composite_data_supported=True)
class PVGeoWriteTableToGSLib(WriteTableToGSLib):
    def __init__(self):
        WriteTableToGSLib.__init__(self)

    @smproperty.stringvector(name="FileName", panel_visibility="never")
    @smdomain.filelist()
    def SetFileName(self, fname):
        """Specify filename for the file to write."""
        WriteTableToGSLib.SetFileName(self, fname)

    @smproperty.stringvector(name="Header", default_values='Saved by PVGeo')
    def SetHeader(self, header):
        WriteTableToGSLib.SetHeader(self, header)

    @smproperty.stringvector(name="Format", default_values='%.9e')
    def SetFormat(self, fmt):
        """Use to set the ASCII format for the writer default is ``'%.9e'``"""
        WriteTableToGSLib.SetFormat(self, fmt)

###############################################################################
