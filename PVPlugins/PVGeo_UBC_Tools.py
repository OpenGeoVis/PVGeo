paraview_plugin_version = '1.1.29'
# This is module to import. It provides VTKPythonAlgorithmBase, the base class
# for all python-based vtkAlgorithm subclasses in VTK and decorators used to
# 'register' the algorithm with ParaView along with information about UI.
from paraview.util.vtkAlgorithm import *

# Helpers:
from PVGeo import _helpers
# Classes to Decorate
from PVGeo.ubc import *

#### GLOBAL VARIABLES ####
MENU_CAT = 'PVGeo: UBC Mesh Tools'

MESH_EXTS = 'mesh msh dat txt text'
TMESH_DESC = 'PVGeo: UBC Mesh 2D/3D Two-File Format'


@smproxy.reader(name="PVGeoTensorMeshReader",
       label="PVGeo: UBC Tensor Mesh Reader",
       extensions=MESH_EXTS,
       file_description=TMESH_DESC)
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

    @smproperty.stringvector(name='DataName', default_values='Data')
    def SetDataName(self, name):
        TensorMeshReader.SetDataName(self, name)

@smproxy.filter(name="PVGeoTensorMeshAppender",
       label="Append Model To UBC Tensor Mesh")
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface With Edges" />''' % MENU_CAT)
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

    @smproperty.stringvector(name='DataName', default_values='Appended Data')
    def SetDataName(self, name):
        TensorMeshAppender.SetDataName(self, name)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def GetTimestepValues(self):
        """This is critical for registering the timesteps"""
        return TensorMeshAppender.GetTimestepValues(self)



#------------------------------------------------------------------------------
# Read OcTree Mesh
#------------------------------------------------------------------------------


@smproxy.reader(name="PVGeoUBCOcTreeMeshReader",
       label="PVGeo: UBC OcTree Mesh Reader",
       extensions=MESH_EXTS,
       file_description='PVGeo: UBC OcTree Mesh')
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

    @smproperty.stringvector(name='DataName', default_values='Data')
    def SetDataName(self, name):
        OcTreeReader.SetDataName(self, name)



@smproxy.filter(name="PVGeoOcTreeAppender",
       label="Append Model To UBC OcTree Mesh")
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

    @smproperty.stringvector(name='DataName', default_values='Appended Data')
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

TOPO_EXTS = 'topo txt dat'
TOPO_DESC = 'UBC 3D Topo Files'

@smproxy.reader(name="PVGeoTopoReader",
       label="PVGeo: UBC 3D Topo Files",
       extensions=TOPO_EXTS,
       file_description=TOPO_DESC)
class PVGeoTopoReader(TopoReader):
    def __init__(self):
        TopoReader.__init__(self)

    #### Seters and Geters ####
    @smproperty.xml(_helpers.getFileReaderXml(TOPO_EXTS, readerDescription=TOPO_DESC))
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

GRV_EXTS = 'grv txt dat'
GRV_DESC = 'GIF Gravity Observations'

@smproxy.reader(name="PVGeoGravObsReader",
       label="PVGeo: GIF Gravity Observations",
       extensions=GRV_EXTS,
       file_description=GRV_DESC)
class PVGeoGravObsReader(GravObsReader):
    def __init__(self):
        GravObsReader.__init__(self)

    #### Seters and Geters ####
    @smproperty.xml(_helpers.getFileReaderXml(GRV_EXTS, readerDescription=GRV_DESC))
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


MAG_EXTS = 'mag loc txt dat'
MAG_DESC = 'GIF Magnetic Observations'

@smproxy.reader(name="PVGeoMagObsReader",
       label="PVGeo: GIF Magnetic Observations",
       extensions=MAG_EXTS,
       file_description=MAG_DESC)
class PVGeoMagObsReader(MagObsReader):
    def __init__(self):
        MagObsReader.__init__(self)

    #### Seters and Geters ####
    @smproperty.xml(_helpers.getFileReaderXml(MAG_EXTS, readerDescription=MAG_DESC))
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
