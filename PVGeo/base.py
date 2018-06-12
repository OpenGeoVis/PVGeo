all = [
    'PVGeoReaderBase',
]

from . import _helpers

# Outside Imports:
from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase


# Base Reader
class PVGeoReaderBase(VTKPythonAlgorithmBase):
    def __init__(self, nOutputPorts=1, outputType='vtkTable'):
        VTKPythonAlgorithmBase.__init__(self,
            nInputPorts=0,
            nOutputPorts=nOutputPorts, outputType=outputType)
        self.__timeStep = 1.0
        self.__fileNames = None


    def RequestInformation(self, request, inInfo, outInfo):
        _helpers.setOutputTimesteps(self, self.__fileNames, dt=self.__timeStep)
        return 1


    #### Seters and Geters ####
    def SetTimeStep(self, timeStep):
        if timeStep != self.__timeStep:
            self.__timeStep = timeStep
            self.Modified()

    def GetTimeStep(self):
        return self.__timeStep

    def SetFileNames(self, fnames):
        if type(fnames) is not list and type(fnames) is not tuple:
            fnames = [fnames]
        if fnames != self.__fileNames:
            self.__fileNames = fnames
            self.Modified()

    def GetFileNames(self, idx=None):
        if idx is None:
            return self.__fileNames
        return self.__fileNames[idx]
