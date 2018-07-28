paraview_plugin_version = '1.1.10'
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
@smhint.xml('''<RepresentationType view="RenderView" type="Surface With Edges" />''')
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
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
@smhint.xml('''<RepresentationType view="RenderView" type="Surface With Edges" />''')
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
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
# @smproxy.writer(extensions="mesh", file_description="UBC Tensor Mesh", support_reload=False)
# @smproperty.input(name="Input", port_index=0)
# @smdomain.datatype(dataTypes=["vtkRectilinearGrid"], composite_data_supported=False)
# class vtkUBCTensorMeshWriter(VTKPythonAlgorithmBase):
#     def __init__(self):
#         VTKPythonAlgorithmBase.__init__(self, nInputPorts=1, nOutputPorts=0, inputType='vtkRectilinearGrid')
#         self._filename = None
#
#     @smproperty.stringvector(name="FileName", panel_visibility="never")
#     @smdomain.filelist()
#     def SetFileName(self, fname):
#         """Specify filename for the file to write."""
#         if self._filename != fname:
#             self._filename = fname
#             self.Modified()
#
#     def RequestData(self, request, inInfoVec, outInfoVec):
#         from vtkmodules.vtkCommonDataModel import vtkRectilinearGrid
#         from vtkmodules.numpy_interface import dataset_adapter as dsa
#
#         grid = dsa.WrapDataObject(vtkRectilinearGrid.GetData(inInfoVec[0], 0))
#         print('saving grid not impleneted')
#         return 1
#
#     def Write(self):
#         self.Modified()
#         self.Update()
#
# @smproxy.writer(extensions="gslib", file_description="GSLib Format", support_reload=False)
# @smproperty.input(name="Input", port_index=0)
# @smdomain.datatype(dataTypes=["vtkRectilinearGrid"], composite_data_supported=False)
# class vtkGSLIBMeshWriter(VTKPythonAlgorithmBase):
#     def __init__(self):
#         VTKPythonAlgorithmBase.__init__(self, nInputPorts=1, nOutputPorts=0, inputType='vtkRectilinearGrid')
#         self._filename = None
#
#     @smproperty.stringvector(name="FileName", panel_visibility="never")
#     @smdomain.filelist()
#     def SetFileName(self, fname):
#         """Specify filename for the file to write."""
#         if self._filename != fname:
#             self._filename = fname
#             self.Modified()
#
#     def RequestData(self, request, inInfoVec, outInfoVec):
#         #from vtkmodules.vtkCommonDataModel import vtkTable
#         #from vtkmodules.numpy_interface import dataset_adapter as dsa
#
#         table = dsa.WrapDataObject(vtkTable.GetData(inInfoVec[0], 0))
#         print('saving grid not impleneted')
#         return 1
#
#     def Write(self):
#         self.Modified()
#         self.Update()
#
#
# @smproxy.writer(extensions="bin", file_description="Binary Array (SEPLib/Madagascr)", support_reload=False)
# @smproperty.input(name="Input", port_index=0)
# @smdomain.datatype(dataTypes=["vtkRectilinearGrid"], composite_data_supported=False)
# class vtkBinaryWriter(VTKPythonAlgorithmBase):
#     def __init__(self):
#         VTKPythonAlgorithmBase.__init__(self, nInputPorts=1, nOutputPorts=0, inputType='vtkRectilinearGrid')
#         self._filename = None
#
#     @smproperty.stringvector(name="FileName", panel_visibility="never")
#     @smdomain.filelist()
#     def SetFileName(self, fname):
#         """Specify filename for the file to write."""
#         if self._filename != fname:
#             self._filename = fname
#             self.Modified()
#
#     def RequestData(self, request, inInfoVec, outInfoVec):
#         from vtkmodules.vtkCommonDataModel import vtkImageData
#         from vtkmodules.numpy_interface import dataset_adapter as dsa
#
#         grid = dsa.WrapDataObject(vtkImageData.GetData(inInfoVec[0], 0))
#         print('saving grid not impleneted')
#         return 1
#
#     def Write(self):
#         self.Modified()
#         self.Update()
