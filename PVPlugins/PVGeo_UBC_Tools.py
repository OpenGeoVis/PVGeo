paraview_plugin_version = '1.2.3'
# This is module to import. It provides VTKPythonAlgorithmBase, the base class
# for all python-based vtkAlgorithm subclasses in VTK and decorators used to
# 'register' the algorithm with ParaView along with information about UI.
from paraview.util.vtkAlgorithm import *

# Helpers:
from PVGeo import _helpers
# Classes to Decorate
from PVGeo.ubc import *

discretize_available = False
try:
    with _helpers.HiddenPrints():
        import discretize
except ImportError:
    pass
else:
    discretize_available = True

#### GLOBAL VARIABLES ####
MENU_CAT = 'PVGeo: UBC Mesh Tools'



@smproxy.reader(name="PVGeoTensorMeshReader",
       label='PVGeo: %s'%TensorMeshReader.__displayname__,
       extensions=TensorMeshReader.extensions,
       file_description=TensorMeshReader.description)
@smhint.xml('''<RepresentationType view="RenderView" type="Surface With Edges" />''')
class PVGeoTensorMeshReader(TensorMeshReader):
    def __init__(self):
        TensorMeshReader.__init__(self)


    #### Seters and Geters ####

    @smproperty.xml('''
        <StringVectorProperty
            panel_visibility="advanced"
            name="MeshFile"
            label="File Name Mesh"
            command="SetMeshFileName"
            animateable="1"
            clean_command="ClearMesh"
            number_of_elements="1">
            <FileListDomain name="meshfile"/>
            <Documentation>This is the mesh file for a 2D or 3D UBC Mesh grid. This plugin only allows ONE mesh to be defined.</Documentation>
        </StringVectorProperty>''')
    def SetMeshFileName(self, fname):
        TensorMeshReader.SetMeshFileName(self, fname)

    @smproperty.xml('''
        <StringVectorProperty
          panel_visibility="default"
          name="ModelFiles"
          label="File Name(s) Model"
          command="AddModelFileName"
          animateable="1"
          repeat_command="1"
          clean_command="ClearModels"
          number_of_elements="1">
          <FileListDomain name="modelfiles"/>
          <Documentation>This is for a single sets of model files to append to the mesh as data time varying attributes. You can chose as many files as you would like for this for the given attribute.</Documentation>
        </StringVectorProperty>''')
    def AddModelFileName(self, fname):
        """Use to set the file names for the reader. Handles singlt string or list of strings."""
        TensorMeshReader.AddModelFileName(self, fname)


    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def SetTimeDelta(self, dt):
        TensorMeshReader.SetTimeDelta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def GetTimestepValues(self):
        """This is critical for registering the timesteps"""
        return TensorMeshReader.GetTimestepValues(self)

    @smproperty.xml(_helpers.getPropertyXml(name='Use file as data name', command='SetUseFileName', default_values=True, help='A boolean to override the DataName and use model file name as data name.',
    panel_visibility="advanced"))
    def SetUseFileName(self, flag):
        TensorMeshReader.SetUseFileName(self, flag)

    @smproperty.stringvector(name='DataName', default_values='Data', panel_visibility="advanced")
    def SetDataName(self, name):
        TensorMeshReader.SetDataName(self, name)

@smproxy.filter(name="PVGeoTensorMeshAppender",
       label=TensorMeshAppender.__displayname__)
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkRectilinearGrid"], composite_data_supported=False)
class PVGeoTensorMeshAppender(TensorMeshAppender):
    """This assumes the input vtkRectilinearGrid has already handled the timesteps"""
    def __init__(self):
        TensorMeshAppender.__init__(self)

    @smproperty.xml('''
        <StringVectorProperty
          panel_visibility="default"
          name="ModelFiles"
          label="File Name(s) Model"
          command="AddModelFileName"
          animateable="1"
          repeat_command="1"
          clean_command="ClearModels"
          number_of_elements="1">
          <FileListDomain name="modelfiles"/>
          <Documentation>This is for a single sets of model files to append to the mesh as data time varying attributes. You can chose as many files as you would like for this for the given attribute.</Documentation>
        </StringVectorProperty>''')
    def AddModelFileName(self, fname):
        """Use to set the file names for the reader. Handles single string or list of strings."""
        TensorMeshAppender.AddModelFileName(self, fname)

    @smproperty.xml(_helpers.getPropertyXml(name='Use file as data name', command='SetUseFileName', default_values=True, help='A boolean to override the DataName and use model file name as data name.',
    panel_visibility="advanced"))
    def SetUseFileName(self, flag):
        TensorMeshAppender.SetUseFileName(self, flag)

    @smproperty.stringvector(name='DataName', default_values='Appended Data', panel_visibility="advanced")
    def SetDataName(self, name):
        TensorMeshAppender.SetDataName(self, name)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def GetTimestepValues(self):
        """This is critical for registering the timesteps"""
        return TensorMeshAppender.GetTimestepValues(self)



@smproxy.filter(name="PVGeoTopoMeshAppender",
       label=TopoMeshAppender.__displayname__)
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkRectilinearGrid"], composite_data_supported=False)
class PVGeoTopoMeshAppender(TopoMeshAppender):
    """This assumes the input vtkRectilinearGrid has already handled the timesteps"""
    def __init__(self):
        TopoMeshAppender.__init__(self)

    @smproperty.xml('''
        <StringVectorProperty
            panel_visibility="advanced"
            name="TopoFile"
            label="File Name Topo"
            command="SetTopoFileName"
            animateable="1"
            clean_command="ClearTopoFile"
            number_of_elements="1">
            <FileListDomain name="topofile"/>
            <Documentation>This plugin only allows ONE topo file to be defined.</Documentation>
        </StringVectorProperty>''')
    def SetTopoFileName(self, fname):
        TopoMeshAppender.SetTopoFileName(self, fname)




#------------------------------------------------------------------------------
# Read OcTree Mesh
#------------------------------------------------------------------------------

if discretize_available:
    @smproxy.reader(name="PVGeoUBCOcTreeMeshReader",
           label='PVGeo: %s'%OcTreeReader.__displayname__,
           extensions=OcTreeReader.extensions,
           file_description=OcTreeReader.description)
    @smhint.xml('''<RepresentationType view="RenderView" type="Surface With Edges" />''')
    class PVGeoUBCOcTreeMeshReader(OcTreeReader):
        def __init__(self):
            OcTreeReader.__init__(self)


        #### Seters and Geters ####

        @smproperty.xml('''
            <StringVectorProperty
                panel_visibility="advanced"
                name="MeshFile"
                label="File Name Mesh"
                command="SetMeshFileName"
                animateable="1"
                clean_command="ClearMesh"
                number_of_elements="1">
                <FileListDomain name="meshfile"/>
                <Documentation>This is the mesh file for a OcTree Mesh grid. This plugin only allows ONE mesh to be defined.</Documentation>
            </StringVectorProperty>''')
        def SetMeshFileName(self, fname):
            OcTreeReader.SetMeshFileName(self, fname)

        @smproperty.xml('''
            <StringVectorProperty
              panel_visibility="default"
              name="ModelFiles"
              label="File Name(s) Model"
              command="AddModelFileName"
              animateable="1"
              repeat_command="1"
              clean_command="ClearModels"
              number_of_elements="1">
              <FileListDomain name="modelfiles"/>
              <Documentation>This is for a single sets of model files to append to the mesh as data time varying attributes. You can chose as many files as you would like for this for the given attribute.</Documentation>
            </StringVectorProperty>''')
        def AddModelFileName(self, fname):
            """Use to set the file names for the reader. Handles singlt string or list of strings."""
            OcTreeReader.AddModelFileName(self, fname)


        @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
        def SetTimeDelta(self, dt):
            OcTreeReader.SetTimeDelta(self, dt)

        @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
        def GetTimestepValues(self):
            """This is critical for registering the timesteps"""
            return OcTreeReader.GetTimestepValues(self)

        @smproperty.xml(_helpers.getPropertyXml(name='Use file as data name', command='SetUseFileName', default_values=True, help='A boolean to override the DataName and use model file name as data name.',
        panel_visibility="advanced"))
        def SetUseFileName(self, flag):
            OcTreeReader.SetUseFileName(self, flag)

        @smproperty.stringvector(name='DataName', default_values='Data', panel_visibility="advanced")
        def SetDataName(self, name):
            OcTreeReader.SetDataName(self, name)



    @smproxy.filter(name="PVGeoOcTreeAppender",
           label=OcTreeAppender.__displayname__)
    @smhint.xml('''<ShowInMenu category="%s"/>
        <RepresentationType view="RenderView" type="Surface With Edges" />''' % MENU_CAT)
    @smproperty.input(name="Input", port_index=0)
    @smdomain.datatype(dataTypes=["vtkUnstructuredGrid"], composite_data_supported=False)
    class PVGeoOcTreeAppender(OcTreeAppender):
        """This assumes the input vtkUnstructuredGrid has already handled the timesteps"""
        def __init__(self):
            OcTreeAppender.__init__(self)

        @smproperty.xml('''
            <StringVectorProperty
              panel_visibility="default"
              name="ModelFiles"
              label="File Name(s) Model"
              command="AddModelFileName"
              animateable="1"
              repeat_command="1"
              clean_command="ClearModels"
              number_of_elements="1">
              <FileListDomain name="modelfiles"/>
              <Documentation>This is for a single sets of model files to append to the mesh as data time varying attributes. You can chose as many files as you would like for this for the given attribute.</Documentation>
            </StringVectorProperty>''')
        def AddModelFileName(self, fname):
            """Use to set the file names for the reader. Handles single string or list of strings."""
            OcTreeAppender.AddModelFileName(self, fname)

        @smproperty.xml(_helpers.getPropertyXml(name='Use file as data name', command='SetUseFileName', default_values=True, help='A boolean to override the DataName and use model file name as data name.',
        panel_visibility="advanced"))
        def SetUseFileName(self, flag):
            OcTreeAppender.SetUseFileName(self, flag)

        @smproperty.stringvector(name='DataName', default_values='Appended Data', panel_visibility="advanced")
        def SetDataName(self, name):
            OcTreeAppender.SetDataName(self, name)


#------------------------------------------------------------------------------
# Write Tensor Mesh
#------------------------------------------------------------------------------


@smproxy.writer(extensions="msh", file_description="UBC Tensor Mesh", support_reload=False)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkRectilinearGrid"], composite_data_supported=True)
class PVGeoWriteRectilinearGridToUBC(WriteRectilinearGridToUBC):
    def __init__(self):
        WriteRectilinearGridToUBC.__init__(self)

    @smproperty.stringvector(name="FileName", panel_visibility="never")
    @smdomain.filelist()
    def SetFileName(self, fname):
        """Specify filename for the file to write."""
        WriteRectilinearGridToUBC.SetFileName(self, fname)

    @smproperty.stringvector(name="Format", default_values='%.9e')
    def SetFormat(self, fmt):
        """Use to set the ASCII format for the writer default is ``'%.9e'``"""
        WriteRectilinearGridToUBC.SetFormat(self, fmt)


@smproxy.writer(extensions="msh", file_description="UBC Tensor Mesh", support_reload=False)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkImageData"], composite_data_supported=True)
class PVGeoWriteImageDataToUBC(WriteImageDataToUBC):
    def __init__(self):
        WriteImageDataToUBC.__init__(self)

    @smproperty.stringvector(name="FileName", panel_visibility="never")
    @smdomain.filelist()
    def SetFileName(self, fname):
        """Specify filename for the file to write."""
        WriteImageDataToUBC.SetFileName(self, fname)

    @smproperty.stringvector(name="Format", default_values='%.9e')
    def SetFormat(self, fmt):
        """Use to set the ASCII format for the writer default is ``'%.9e'``"""
        WriteImageDataToUBC.SetFormat(self, fmt)


###############################################################################


@smproxy.reader(name="PVGeoTopoReader",
       label='PVGeo: %s'%TopoReader.__displayname__,
       extensions=TopoReader.extensions,
       file_description=TopoReader.description)
class PVGeoTopoReader(TopoReader):
    def __init__(self):
        TopoReader.__init__(self)

    #### Seters and Geters ####
    @smproperty.xml(_helpers.getFileReaderXml(TopoReader.extensions, readerDescription=TopoReader.description))
    def AddFileName(self, fname):
        TopoReader.AddFileName(self, fname)

    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def SetTimeDelta(self, dt):
        TopoReader.SetTimeDelta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def GetTimestepValues(self):
        """This is critical for registering the timesteps"""
        return TopoReader.GetTimestepValues(self)

    @smproperty.intvector(name="SkipRows", default_values=0, panel_visibility="advanced")
    def SetSkipRows(self, skip):
        TopoReader.SetSkipRows(self, skip)

    @smproperty.stringvector(name="Comments", default_values="!", panel_visibility="advanced")
    def SetComments(self, identifier):
        TopoReader.SetComments(self, identifier)



###############################################################################


@smproxy.reader(name="PVGeoGravObsReader",
       label='PVGeo: %s'%GravObsReader.__displayname__,
       extensions=GravObsReader.extensions,
       file_description=GravObsReader.description)
class PVGeoGravObsReader(GravObsReader):
    def __init__(self):
        GravObsReader.__init__(self)

    #### Seters and Geters ####
    @smproperty.xml(_helpers.getFileReaderXml(GravObsReader.extensions, readerDescription=GravObsReader.description))
    def AddFileName(self, fname):
        GravObsReader.AddFileName(self, fname)

    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def SetTimeDelta(self, dt):
        GravObsReader.SetTimeDelta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def GetTimestepValues(self):
        """This is critical for registering the timesteps"""
        return GravObsReader.GetTimestepValues(self)

    @smproperty.intvector(name="SkipRows", default_values=0, panel_visibility="advanced")
    def SetSkipRows(self, skip):
        GravObsReader.SetSkipRows(self, skip)

    @smproperty.stringvector(name="Comments", default_values="!", panel_visibility="advanced")
    def SetComments(self, identifier):
        GravObsReader.SetComments(self, identifier)


###############################################################################


@smproxy.reader(name="PVGeoGravGradReader",
       label='PVGeo: %s'%GravGradReader.__displayname__,
       extensions=GravGradReader.extensions,
       file_description=GravGradReader.description)
class PVGeoGravGradReader(GravGradReader):
    def __init__(self):
        GravGradReader.__init__(self)

    #### Seters and Geters ####
    @smproperty.xml(_helpers.getFileReaderXml(GravGradReader.extensions, readerDescription=GravGradReader.description))
    def AddFileName(self, fname):
        GravGradReader.AddFileName(self, fname)

    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def SetTimeDelta(self, dt):
        GravGradReader.SetTimeDelta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def GetTimestepValues(self):
        """This is critical for registering the timesteps"""
        return GravGradReader.GetTimestepValues(self)

    @smproperty.intvector(name="SkipRows", default_values=0, panel_visibility="advanced")
    def SetSkipRows(self, skip):
        GravGradReader.SetSkipRows(self, skip)

    @smproperty.stringvector(name="Comments", default_values="!", panel_visibility="advanced")
    def SetComments(self, identifier):
        GravGradReader.SetComments(self, identifier)



###############################################################################


@smproxy.reader(name="PVGeoMagObsReader",
       label='PVGeo: %s'%MagObsReader.__displayname__,
       extensions=MagObsReader.extensions,
       file_description=MagObsReader.description)
class PVGeoMagObsReader(MagObsReader):
    def __init__(self):
        MagObsReader.__init__(self)

    #### Seters and Geters ####
    @smproperty.xml(_helpers.getFileReaderXml(MagObsReader.extensions, readerDescription=MagObsReader.description))
    def AddFileName(self, fname):
        MagObsReader.AddFileName(self, fname)

    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def SetTimeDelta(self, dt):
        MagObsReader.SetTimeDelta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def GetTimestepValues(self):
        """This is critical for registering the timesteps"""
        return MagObsReader.GetTimestepValues(self)

    @smproperty.intvector(name="SkipRows", default_values=0, panel_visibility="advanced")
    def SetSkipRows(self, skip):
        MagObsReader.SetSkipRows(self, skip)

    @smproperty.stringvector(name="Comments", default_values="!", panel_visibility="advanced")
    def SetComments(self, identifier):
        MagObsReader.SetComments(self, identifier)


###############################################################################


@smproxy.filter(name='PVGeoGeologyMapper', label=GeologyMapper.__displayname__)
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkDataObject"], composite_data_supported=False)
class PVGeoGeologyMapper(GeologyMapper):
    def __init__(self):
        GeologyMapper.__init__(self)

    #### SETTERS AND GETTERS ####

    @smproperty.xml(_helpers.getInputArrayXml(nInputPorts=1, numArrays=1))
    def SetInputArrayToProcess(self, idx, port, connection, field, name):
        return GeologyMapper.SetInputArrayToProcess(self, idx, port, connection, field, name)

    @smproperty.xml('''
        <StringVectorProperty
            panel_visibility="default"
            name="FileName"
            label="File Name"
            command="SetFileName"
            animateable="1"
            number_of_elements="1">
            <FileListDomain name="filename"/>
            <Documentation>This is the file contating the mapping definitions.</Documentation>
        </StringVectorProperty>''')
    def SetFileName(self, fname):
        GeologyMapper.SetFileName(self, fname)

    @smproperty.stringvector(name="Delimiter", default_values=",", panel_visibility="advanced")
    def SetDelimiter(self, identifier):
        GeologyMapper.SetDelimiter(self, identifier)


###############################################################################


if discretize_available:
    @smproxy.reader(name="PVGeoDiscretizeMeshReader",
           label='PVGeo: %s'%DiscretizeMeshReader.__displayname__,
           extensions=DiscretizeMeshReader.extensions,
           file_description=DiscretizeMeshReader.description)
    class PVGeoDiscretizeMeshReader(DiscretizeMeshReader):
        def __init__(self):
            DiscretizeMeshReader.__init__(self)

        #### Seters and Geters ####

        @smproperty.xml(_helpers.getFileReaderXml(DiscretizeMeshReader.extensions, readerDescription=DiscretizeMeshReader.description))
        def AddFileName(self, fname):
            DiscretizeMeshReader.AddFileName(self, fname)

        @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
        def SetTimeDelta(self, dt):
            DiscretizeMeshReader.SetTimeDelta(self, dt)

        @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
        def GetTimestepValues(self):
            """This is critical for registering the timesteps"""
            return DiscretizeMeshReader.GetTimestepValues(self)
