paraview_plugin_version = '2.0.0'
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
            command="set_mesh_filename"
            animateable="1"
            clean_command="clear_mesh"
            number_of_elements="1">
            <FileListDomain name="meshfile"/>
            <Documentation>This is the mesh file for a 2D or 3D UBC Mesh grid. This plugin only allows ONE mesh to be defined.</Documentation>
        </StringVectorProperty>''')
    def set_mesh_filename(self, filename):
        TensorMeshReader.set_mesh_filename(self, filename)

    @smproperty.xml('''
        <StringVectorProperty
          panel_visibility="default"
          name="ModelFiles"
          label="File Name(s) Model"
          command="add_model_file_name"
          animateable="1"
          repeat_command="1"
          clean_command="clear_models"
          number_of_elements="1">
          <FileListDomain name="model_files"/>
          <Documentation>This is for a single sets of model files to append to the mesh as data time varying attributes. You can chose as many files as you would like for this for the given attribute.</Documentation>
        </StringVectorProperty>''')
    def add_model_file_name(self, filename):
        """Use to set the file names for the reader. Handles singlt string or list of strings."""
        TensorMeshReader.add_model_file_name(self, filename)


    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def set_time_delta(self, dt):
        TensorMeshReader.set_time_delta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def get_time_step_values(self):
        """This is critical for registering the timesteps"""
        return TensorMeshReader.get_time_step_values(self)

    @smproperty.xml(_helpers.get_property_xml(name='Use file as data name', command='set_use_filename', default_values=True, help='A boolean to override the DataName and use model file name as data name.',
    panel_visibility="advanced"))
    def set_use_filename(self, flag):
        TensorMeshReader.set_use_filename(self, flag)

    @smproperty.stringvector(name='DataName', default_values='Data', panel_visibility="advanced")
    def set_data_name(self, name):
        TensorMeshReader.set_data_name(self, name)

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
          command="add_model_file_name"
          animateable="1"
          repeat_command="1"
          clean_command="clear_models"
          number_of_elements="1">
          <FileListDomain name="model_files"/>
          <Documentation>This is for a single sets of model files to append to the mesh as data time varying attributes. You can chose as many files as you would like for this for the given attribute.</Documentation>
        </StringVectorProperty>''')
    def add_model_file_name(self, filename):
        """Use to set the file names for the reader. Handles single string or list of strings."""
        TensorMeshAppender.add_model_file_name(self, filename)

    @smproperty.xml(_helpers.get_property_xml(name='Use file as data name', command='set_use_filename', default_values=True, help='A boolean to override the DataName and use model file name as data name.',
    panel_visibility="advanced"))
    def set_use_filename(self, flag):
        TensorMeshAppender.set_use_filename(self, flag)

    @smproperty.stringvector(name='DataName', default_values='Appended Data', panel_visibility="advanced")
    def set_data_name(self, name):
        TensorMeshAppender.set_data_name(self, name)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def get_time_step_values(self):
        """This is critical for registering the timesteps"""
        return TensorMeshAppender.get_time_step_values(self)



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
            command="set_topo_filename"
            animateable="1"
            clean_command="clear_topo_file"
            number_of_elements="1">
            <FileListDomain name="topofile"/>
            <Documentation>This plugin only allows ONE topo file to be defined.</Documentation>
        </StringVectorProperty>''')
    def set_topo_filename(self, filename):
        TopoMeshAppender.set_topo_filename(self, filename)




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
                command="set_mesh_filename"
                animateable="1"
                clean_command="clear_mesh"
                number_of_elements="1">
                <FileListDomain name="meshfile"/>
                <Documentation>This is the mesh file for a OcTree Mesh grid. This plugin only allows ONE mesh to be defined.</Documentation>
            </StringVectorProperty>''')
        def set_mesh_filename(self, filename):
            OcTreeReader.set_mesh_filename(self, filename)

        @smproperty.xml('''
            <StringVectorProperty
              panel_visibility="default"
              name="ModelFiles"
              label="File Name(s) Model"
              command="add_model_file_name"
              animateable="1"
              repeat_command="1"
              clean_command="clear_models"
              number_of_elements="1">
              <FileListDomain name="model_files"/>
              <Documentation>This is for a single sets of model files to append to the mesh as data time varying attributes. You can chose as many files as you would like for this for the given attribute.</Documentation>
            </StringVectorProperty>''')
        def add_model_file_name(self, filename):
            """Use to set the file names for the reader. Handles singlt string or list of strings."""
            OcTreeReader.add_model_file_name(self, filename)


        @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
        def set_time_delta(self, dt):
            OcTreeReader.set_time_delta(self, dt)

        @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
        def get_time_step_values(self):
            """This is critical for registering the timesteps"""
            return OcTreeReader.get_time_step_values(self)

        @smproperty.xml(_helpers.get_property_xml(name='Use file as data name', command='set_use_filename', default_values=True, help='A boolean to override the DataName and use model file name as data name.',
        panel_visibility="advanced"))
        def set_use_filename(self, flag):
            OcTreeReader.set_use_filename(self, flag)

        @smproperty.stringvector(name='DataName', default_values='Data', panel_visibility="advanced")
        def set_data_name(self, name):
            OcTreeReader.set_data_name(self, name)



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
              command="add_model_file_name"
              animateable="1"
              repeat_command="1"
              clean_command="clear_models"
              number_of_elements="1">
              <FileListDomain name="model_files"/>
              <Documentation>This is for a single sets of model files to append to the mesh as data time varying attributes. You can chose as many files as you would like for this for the given attribute.</Documentation>
            </StringVectorProperty>''')
        def add_model_file_name(self, filename):
            """Use to set the file names for the reader. Handles single string or list of strings."""
            OcTreeAppender.add_model_file_name(self, filename)

        @smproperty.xml(_helpers.get_property_xml(name='Use file as data name', command='set_use_filename', default_values=True, help='A boolean to override the DataName and use model file name as data name.',
        panel_visibility="advanced"))
        def set_use_filename(self, flag):
            OcTreeAppender.set_use_filename(self, flag)

        @smproperty.stringvector(name='DataName', default_values='Appended Data', panel_visibility="advanced")
        def set_data_name(self, name):
            OcTreeAppender.set_data_name(self, name)


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
    def SetFileName(self, filename):
        """Specify filename for the file to write."""
        WriteRectilinearGridToUBC.SetFileName(self, filename)

    @smproperty.stringvector(name="Format", default_values='%.9e')
    def set_format(self, fmt):
        """Use to set the ASCII format for the writer default is ``'%.9e'``"""
        WriteRectilinearGridToUBC.set_format(self, fmt)


@smproxy.writer(extensions="msh", file_description="UBC Tensor Mesh", support_reload=False)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkImageData"], composite_data_supported=True)
class PVGeoWriteImageDataToUBC(WriteImageDataToUBC):
    def __init__(self):
        WriteImageDataToUBC.__init__(self)

    @smproperty.stringvector(name="FileName", panel_visibility="never")
    @smdomain.filelist()
    def SetFileName(self, filename):
        """Specify filename for the file to write."""
        WriteImageDataToUBC.SetFileName(self, filename)

    @smproperty.stringvector(name="Format", default_values='%.9e')
    def set_format(self, fmt):
        """Use to set the ASCII format for the writer default is ``'%.9e'``"""
        WriteImageDataToUBC.set_format(self, fmt)


###############################################################################


@smproxy.reader(name="PVGeoTopoReader",
       label='PVGeo: %s'%TopoReader.__displayname__,
       extensions=TopoReader.extensions,
       file_description=TopoReader.description)
class PVGeoTopoReader(TopoReader):
    def __init__(self):
        TopoReader.__init__(self)

    #### Seters and Geters ####
    @smproperty.xml(_helpers.get_file_reader_xml(TopoReader.extensions, reader_description=TopoReader.description))
    def AddFileName(self, filename):
        TopoReader.AddFileName(self, filename)

    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def set_time_delta(self, dt):
        TopoReader.set_time_delta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def get_time_step_values(self):
        """This is critical for registering the timesteps"""
        return TopoReader.get_time_step_values(self)

    @smproperty.intvector(name="SkipRows", default_values=0, panel_visibility="advanced")
    def set_skip_rows(self, skip):
        TopoReader.set_skip_rows(self, skip)

    @smproperty.stringvector(name="Comments", default_values="!", panel_visibility="advanced")
    def set_comments(self, identifier):
        TopoReader.set_comments(self, identifier)



###############################################################################


@smproxy.reader(name="PVGeoGravObsReader",
       label='PVGeo: %s'%GravObsReader.__displayname__,
       extensions=GravObsReader.extensions,
       file_description=GravObsReader.description)
class PVGeoGravObsReader(GravObsReader):
    def __init__(self):
        GravObsReader.__init__(self)

    #### Seters and Geters ####
    @smproperty.xml(_helpers.get_file_reader_xml(GravObsReader.extensions, reader_description=GravObsReader.description))
    def AddFileName(self, filename):
        GravObsReader.AddFileName(self, filename)

    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def set_time_delta(self, dt):
        GravObsReader.set_time_delta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def get_time_step_values(self):
        """This is critical for registering the timesteps"""
        return GravObsReader.get_time_step_values(self)

    @smproperty.intvector(name="SkipRows", default_values=0, panel_visibility="advanced")
    def set_skip_rows(self, skip):
        GravObsReader.set_skip_rows(self, skip)

    @smproperty.stringvector(name="Comments", default_values="!", panel_visibility="advanced")
    def set_comments(self, identifier):
        GravObsReader.set_comments(self, identifier)


###############################################################################


@smproxy.reader(name="PVGeoGravGradReader",
       label='PVGeo: %s'%GravGradReader.__displayname__,
       extensions=GravGradReader.extensions,
       file_description=GravGradReader.description)
class PVGeoGravGradReader(GravGradReader):
    def __init__(self):
        GravGradReader.__init__(self)

    #### Seters and Geters ####
    @smproperty.xml(_helpers.get_file_reader_xml(GravGradReader.extensions, reader_description=GravGradReader.description))
    def AddFileName(self, filename):
        GravGradReader.AddFileName(self, filename)

    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def set_time_delta(self, dt):
        GravGradReader.set_time_delta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def get_time_step_values(self):
        """This is critical for registering the timesteps"""
        return GravGradReader.get_time_step_values(self)

    @smproperty.intvector(name="SkipRows", default_values=0, panel_visibility="advanced")
    def set_skip_rows(self, skip):
        GravGradReader.set_skip_rows(self, skip)

    @smproperty.stringvector(name="Comments", default_values="!", panel_visibility="advanced")
    def set_comments(self, identifier):
        GravGradReader.set_comments(self, identifier)



###############################################################################


@smproxy.reader(name="PVGeoMagObsReader",
       label='PVGeo: %s'%MagObsReader.__displayname__,
       extensions=MagObsReader.extensions,
       file_description=MagObsReader.description)
class PVGeoMagObsReader(MagObsReader):
    def __init__(self):
        MagObsReader.__init__(self)

    #### Seters and Geters ####
    @smproperty.xml(_helpers.get_file_reader_xml(MagObsReader.extensions, reader_description=MagObsReader.description))
    def AddFileName(self, filename):
        MagObsReader.AddFileName(self, filename)

    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def set_time_delta(self, dt):
        MagObsReader.set_time_delta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def get_time_step_values(self):
        """This is critical for registering the timesteps"""
        return MagObsReader.get_time_step_values(self)

    @smproperty.intvector(name="SkipRows", default_values=0, panel_visibility="advanced")
    def set_skip_rows(self, skip):
        MagObsReader.set_skip_rows(self, skip)

    @smproperty.stringvector(name="Comments", default_values="!", panel_visibility="advanced")
    def set_comments(self, identifier):
        MagObsReader.set_comments(self, identifier)


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

    @smproperty.xml(_helpers.get_input_array_xml(nInputPorts=1, n_arrays=1))
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
    def SetFileName(self, filename):
        GeologyMapper.SetFileName(self, filename)

    @smproperty.stringvector(name="Delimiter", default_values=",", panel_visibility="advanced")
    def set_delimiter(self, deli):
        GeologyMapper.set_delimiter(self, deli)


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

        @smproperty.xml(_helpers.get_file_reader_xml(DiscretizeMeshReader.extensions, reader_description=DiscretizeMeshReader.description))
        def AddFileName(self, filename):
            DiscretizeMeshReader.AddFileName(self, filename)

        @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
        def set_time_delta(self, dt):
            DiscretizeMeshReader.set_time_delta(self, dt)

        @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
        def get_time_step_values(self):
            """This is critical for registering the timesteps"""
            return DiscretizeMeshReader.get_time_step_values(self)
