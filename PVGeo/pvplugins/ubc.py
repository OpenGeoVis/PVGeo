"""
This file contains the necessary VTKPythonAlgorithmBase subclasses to implement
functionality in this submodule as filters, sources, readers, and writers in
ParaView.
"""


# This is module to import. It provides VTKPythonAlgorithmBase, the base class
# for all python-based vtkAlgorithm subclasses in VTK and decorators used to
# 'register' the algorithm with ParaView along with information about UI.
#TODO:from paraview.util.vtkAlgorithm import *

import numpy as np
import vtk
from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase
from vtk.util import numpy_support as nps

# Local Imports
from .. import _helpers
from .extent import *
from .tensor_mesh import *
from .octree import *

# TODO: finish implementing
class UBCTensorMeshReader(VTKPythonAlgorithmBase):
    def __init__(self):
        PVTKPythonAlgorithmBase.__init__(self,
            nInputPorts=0,
            nOutputPorts=1, outputType='vtkRectilinearGrid')

        self.__timeStep = 1.0
        # Other Parameters:
        self.__MeshFileName = None
        self.__ModelFileNames = None
        self.__MeshBuilt = False

    def _updateModel(output, model):
        return None


    def RequestData(self, request, inInfo, outInfo):
        # Get requested time index
        i = _helpers.getTimeStepFileIndex(self, self.GetModelFileNames(), dt=self.GetTimeStep())
        output = vtk.vtkRectilinearGrid.GetData(outInfo)
        """if not self.__MeshBuilt:
            # The mesh file has not been read in yet
            ubcTensorMesh(self.__MeshFileName, self.__ModelFileNames[i], pdo=output)
        # Read in desired model for time step
        else:
            model =
            placeModelOnMesh(outp, model, dataNm='Data')"""

        return 1


    def RequestInformation(self, request, inInfo, outInfo):
        _helpers.setOutputTimesteps(self, self.GetFileNames(), dt=self.GetTimeStep())
        # Now set whole output extent
        ext = sgemsExtent(self.GetFileNames(0), deli=self.__delimiter,
            useTab=self.__useTab, comments=self.__comments)
        info = outInfo.GetInformationObject(0)
        # Set WHOLE_EXTENT: This is absolutely necessary
        info.Set(vtk.vtkStreamingDemandDrivenPipeline.WHOLE_EXTENT(), ext, 6)
        return 1


    #### Seters and Geters ####

    def SetTimeStep(self, timeStep):
        if timeStep != self.__timeStep:
            self.__timeStep = timeStep
            self.Modified()

    def GetTimeStep(self):
        return self.__timeStep

    def SetMeshFileName(self, meshfile):
        if type(meshfile) is list or type(meshfile) is tuple:
            raise Exception('Tensor Meshes cannot have a varying mesh file.')
        if meshfile != self.__FileNameModel:
            self.__FileNameModel = meshfile
            self.Modified()

    def GetMeshFileName(self):
        return self.__MeshFileName

    def SetModelFileNames(self, fnames):
        if type(fnames) is not list and type(fnames) is not tuple:
            fnames = [fnames]
        if fnames != self.__fileNames:
            self.__ModelFileNames = fnames
            self.Modified()

    def GetModelFileNames(self, idx=None):
        if idx is None:
            return self.__ModelFileNames
        return self.__ModelFileNames[idx]
