paraview_plugin_version = '1.2.3'
# This is module to import. It provides VTKPythonAlgorithmBase, the base class
# for all python-based vtkAlgorithm subclasses in VTK and decorators used to
# 'register' the algorithm with ParaView along with information about UI.
from paraview.util.vtkAlgorithm import *

# Helpers:
from PVGeo import _helpers
# Classes to Decorate
from PVGeo.gslib import *

###############################################################################


@smproxy.reader(name="PVGeoGSLibReader",
       label='PVGeo: %s'%GSLibReader.__displayname__,
       extensions=GSLibReader.extensions,
       file_description=GSLibReader.description)
class PVGeoGSLibReader(GSLibReader):
    def __init__(self):
        GSLibReader.__init__(self)

    #### Seters and Geters ####

    @smproperty.xml(_helpers.get_file_reader_xml(GSLibReader.extensions, reader_description=GSLibReader.description))
    def AddFileName(self, filename):
        GSLibReader.AddFileName(self, filename)

    @smproperty.stringvector(name="Delimiter", default_values=" ")
    def SetDelimiter(self, deli):
        GSLibReader.SetDelimiter(self, deli)

    @smproperty.xml(_helpers.get_property_xml(name='Use Split on Whitespace', command='SetSplitOnWhiteSpace', default_values=True, help='A boolean to override the Delimiter_Field and use whitespace as delimiter.'))
    def SetSplitOnWhiteSpace(self, flag):
        GSLibReader.SetSplitOnWhiteSpace(self, flag)

    @smproperty.intvector(name="SkipRows", default_values=0)
    def SetSkipRows(self, skip):
        GSLibReader.SetSkipRows(self, skip)

    @smproperty.stringvector(name="Comments", default_values="!")
    def SetComments(self, identifier):
        GSLibReader.SetComments(self, identifier)

    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def set_time_delta(self, dt):
        GSLibReader.set_time_delta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def get_time_step_values(self):
        """This is critical for registering the timesteps"""
        return GSLibReader.get_time_step_values(self)

    @smproperty.xml("""<Property name="Print File Header" command="PrintFileHeader" panel_widget="command_button"/>""")
    def PrintFileHeader(self):
        print(GSLibReader.GetFileHeader(self))
        return 1



###############################################################################


@smproxy.reader(name="PVGeoGSLibPointSetReader",
       label='PVGeo: %s'%GSLibPointSetReader.__displayname__,
       extensions=GSLibPointSetReader.extensions,
       file_description=GSLibPointSetReader.description)
@smhint.xml('''<RepresentationType view="RenderView" type="Points" />''')
class PVGeoGSLibPointSetReader(GSLibPointSetReader):
    def __init__(self):
        GSLibPointSetReader.__init__(self)

    #### Seters and Geters ####

    @smproperty.xml(_helpers.get_file_reader_xml(GSLibPointSetReader.extensions, reader_description=GSLibPointSetReader.description))
    def AddFileName(self, filename):
        GSLibPointSetReader.AddFileName(self, filename)

    @smproperty.stringvector(name="Delimiter", default_values=" ")
    def SetDelimiter(self, deli):
        GSLibPointSetReader.SetDelimiter(self, deli)

    @smproperty.xml(_helpers.get_property_xml(name='Use Split on Whitespace', command='SetSplitOnWhiteSpace', default_values=True, help='A boolean to override the Delimiter_Field and use whitespace as delimiter.'))
    def SetSplitOnWhiteSpace(self, flag):
        GSLibPointSetReader.SetSplitOnWhiteSpace(self, flag)

    @smproperty.intvector(name="SkipRows", default_values=0)
    def SetSkipRows(self, skip):
        GSLibPointSetReader.SetSkipRows(self, skip)

    @smproperty.stringvector(name="Comments", default_values="!")
    def SetComments(self, identifier):
        GSLibPointSetReader.SetComments(self, identifier)

    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def set_time_delta(self, dt):
        GSLibPointSetReader.set_time_delta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def get_time_step_values(self):
        """This is critical for registering the timesteps"""
        return GSLibPointSetReader.get_time_step_values(self)

    @smproperty.xml("""<Property name="Print File Header" command="PrintFileHeader" panel_widget="command_button"/>""")
    def PrintFileHeader(self):
        print(GSLibPointSetReader.GetFileHeader(self))
        return 1


###############################################################################


@smproxy.reader(name="PVGeoSGeMSGridReader",
       label='PVGeo: %s'%SGeMSGridReader.__displayname__,
       extensions=SGeMSGridReader.extensions,
       file_description=SGeMSGridReader.description)
@smhint.xml('''<RepresentationType view="RenderView" type="Surface" />''')
class PVGeoSGeMSGridReader(SGeMSGridReader):
    def __init__(self):
        SGeMSGridReader.__init__(self)


    #### Seters and Geters ####
    @smproperty.xml(_helpers.get_file_reader_xml(SGeMSGridReader.extensions, reader_description=SGeMSGridReader.description))
    def AddFileName(self, filename):
        SGeMSGridReader.AddFileName(self, filename)

    @smproperty.stringvector(name="Delimiter", default_values=" ")
    def SetDelimiter(self, deli):
        SGeMSGridReader.SetDelimiter(self, deli)

    @smproperty.xml(_helpers.get_property_xml(name='Use Split on Whitespace', command='SetSplitOnWhiteSpace', default_values=True, help='A boolean to override the Delimiter_Field and use whitespace as delimiter.'))
    def SetSplitOnWhiteSpace(self, flag):
        SGeMSGridReader.SetSplitOnWhiteSpace(self, flag)

    @smproperty.intvector(name="SkipRows", default_values=0)
    def SetSkipRows(self, skip):
        SGeMSGridReader.SetSkipRows(self, skip)

    @smproperty.stringvector(name="Comments", default_values="!")
    def SetComments(self, identifier):
        SGeMSGridReader.SetComments(self, identifier)

    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def set_time_delta(self, dt):
        SGeMSGridReader.set_time_delta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def get_time_step_values(self):
        """This is critical for registering the timesteps"""
        return SGeMSGridReader.get_time_step_values(self)

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
    def SetFileName(self, filename):
        """Specify filename for the file to write."""
        WriteImageDataToSGeMS.SetFileName(self, filename)

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
    def SetFileName(self, filename):
        """Specify filename for the file to write."""
        WriteTableToGSLib.SetFileName(self, filename)

    @smproperty.stringvector(name="Header", default_values='Saved by PVGeo')
    def SetHeader(self, header):
        WriteTableToGSLib.SetHeader(self, header)

    @smproperty.stringvector(name="Format", default_values='%.9e')
    def SetFormat(self, fmt):
        """Use to set the ASCII format for the writer default is ``'%.9e'``"""
        WriteTableToGSLib.SetFormat(self, fmt)

###############################################################################
