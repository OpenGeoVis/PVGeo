__all__ = [

]

# Outside Modules
import numpy as np
import vtk
from vtk.util import numpy_support as nps
import warnings
# Get plugin generator imports
try:
    # This is module to import. It provides VTKPythonAlgorithmBase, the base class
    # for all python-based vtkAlgorithm subclasses in VTK and decorators used to
    # 'register' the algorithm with ParaView along with information about UI.
    from paraview.util.vtkAlgorithm import *
except ImportError:
    from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase
    from PVGeo._detail import *

# PVGeo Imports
from PVGeo import vtkPVGeoReaderBase
from PVGeo import _helpers
from PVGeo.ubc import *

# # TODO: finish implementing
# class vtkUBCTensorMeshReader(VTKPythonAlgorithmBase):
#     def __init__(self):
#         PVTKPythonAlgorithmBase.__init__(self,
#             nInputPorts=0,
#             nOutputPorts=1, outputType='vtkRectilinearGrid')
#
#         self.__timeStep = 1.0
#         # Other Parameters:
#         self.__MeshFileName = None
#         self.__ModelFileNames = None
#         self.__MeshBuilt = False
#
#     def _updateModel(output, model):
#         return None
#
#
#     def RequestData(self, request, inInfo, outInfo):
#         # Get requested time index
#         i = _helpers.getTimeStepFileIndex(self, self.GetModelFileNames(), dt=self.GetTimeStep())
#         output = vtk.vtkRectilinearGrid.GetData(outInfo)
#         """if not self.__MeshBuilt:
#             # The mesh file has not been read in yet
#             ubcTensorMesh(self.__MeshFileName, self.__ModelFileNames[i], pdo=output)
#         # Read in desired model for time step
#         else:
#             model =
#             placeModelOnMesh(outp, model, dataNm='Data')"""
#
#         return 1
#
#
#     def RequestInformation(self, request, inInfo, outInfo):
#         _helpers.setOutputTimesteps(self, self.GetFileNames(), dt=self.GetTimeStep())
#         # Now set whole output extent
#         ext = sgemsExtent(self.GetFileNames(0), deli=self.__delimiter,
#             useTab=self.__useTab, comments=self.__comments)
#         info = outInfo.GetInformationObject(0)
#         # Set WHOLE_EXTENT: This is absolutely necessary
#         info.Set(vtk.vtkStreamingDemandDrivenPipeline.WHOLE_EXTENT(), ext, 6)
#         return 1
#
#
#     #### Seters and Geters ####
#
#     def SetTimeStep(self, timeStep):
#         if timeStep != self.__timeStep:
#             self.__timeStep = timeStep
#             self.Modified()
#
#     def GetTimeStep(self):
#         return self.__timeStep
#
#     def SetMeshFileName(self, meshfile):
#         if type(meshfile) is list or type(meshfile) is tuple:
#             raise Exception('Tensor Meshes cannot have a varying mesh file.')
#         if meshfile != self.__FileNameModel:
#             self.__FileNameModel = meshfile
#             self.Modified()
#
#     def GetMeshFileName(self):
#         return self.__MeshFileName
#
#     def SetModelFileNames(self, fnames):
#         if type(fnames) is not list and type(fnames) is not tuple:
#             fnames = [fnames]
#         if fnames != self.__fileNames:
#             self.__ModelFileNames = fnames
#             self.Modified()
#
#     def GetModelFileNames(self, idx=None):
#         if idx is None:
#             return self.__ModelFileNames
#         return self.__ModelFileNames[idx]


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
