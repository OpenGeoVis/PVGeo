all = [
    'TwoFileReaderBase',
    'ubcMeshReaderBase',
    'ubcModelAppenderBase',
]

from .. import _helpers
from ..base import PVGeoAlgorithmBase
# Outside Imports:
import numpy as np
import vtk


# Two File Reader Base
class TwoFileReaderBase(PVGeoAlgorithmBase):
    """@desc: A base clase for readers that need to handle two input files. One meta-data file and a series of data files."""
    def __init__(self, nOutputPorts=1, outputType='vtkUnstructuredGrid'):
        PVGeoAlgorithmBase.__init__(self,
            nInputPorts=0,
            nOutputPorts=nOutputPorts, outputType=outputType)
        self.__dt = 1.0
        self.__timesteps = None
        self.__meshFileName = None # Can only be one!
        self.__modelFileNames = [] # Can be many (single attribute, manytimesteps)
        self.__needToReadMesh = True
        self.__needToReadModels = True


    def __UpdateTimeSteps(self):
        """for internal use only"""
        if len(self.__modelFileNames) > 0:
            self.__timesteps = _helpers.UpdateTimeSteps(self, self.__modelFileNames, self.__dt)
        return 1

    def NeedToReadMesh(self, flag=None):
        """@desc: Ask self if the reader needs to read the mesh file again
        if the flag is set then this method will set the read status"""
        if flag is not None and isinstance(flag, (bool, int)):
            self.__needToReadMesh = flag
        return self.__needToReadMesh

    def NeedToReadModels(self, flag=None):
        """@desc: Ask self if the reader needs to read the model files again
        if the flag is set then this method will set the read status"""
        if flag is not None and isinstance(flag, (bool, int)):
            self.__needToReadModels = flag
        return self.__needToReadModels

    def Modified(self, readAgainMesh=True, readAgainModels=True):
        """@desc: Call modified if the files needs to be read again again"""
        if readAgainMesh: self.NeedToReadMesh(flag=readAgainMesh)
        if readAgainModels: self.NeedToReadModels(flag=readAgainModels)
        PVGeoAlgorithmBase.Modified(self)

    def RequestInformation(self, request, inInfo, outInfo):
        self.__UpdateTimeSteps()
        return 1


    #### Seters and Geters ####


    @staticmethod
    def HasModels(modelfiles):
        if isinstance(modelfiles, list):
            return len(modelfiles) > 0
        return modelfiles is not None

    def ThisHasModels(self):
        return TwoFileReaderBase.HasModels(self.__modelFileNames)

    def GetTimestepValues(self):
        """@desc: Use this in ParaView decorator to register timesteps"""
        return self.__timesteps.tolist() if self.__timesteps is not None else None

    def SetTimeDelta(self, dt):
        """An advanced property for the time step in seconds."""
        if dt != self.__dt:
            self.__dt = dt
            self.Modified(readAgainMesh=False, readAgainModels=False)

    def ClearMesh(self):
        """@desc: Use to clear mesh file name"""
        self.__meshFileName = None
        self.Modified(readAgainMesh=True, readAgainModels=False)

    def ClearModels(self):
        """@desc: Use to clear data file names"""
        self.__modelFileNames = []
        self.Modified(readAgainMesh=False, readAgainModels=True)

    def SetMeshFileName(self, fname):
        if self.__meshFileName != fname:
            self.__meshFileName = fname
            self.Modified(readAgainMesh=True, readAgainModels=False)

    def AddModelFileName(self, fname):
        """@desc: Use to set the file names for the reader. Handles singlt string or list of strings."""
        if fname is None:
            return # do nothing if None is passed by a constructor on accident
        if isinstance(fname, list):
            for f in fname:
                self.AddModelFileName(f)
            self.Modified(readAgainMesh=False, readAgainModels=True)
        elif fname not in self.__modelFileNames:
            self.__modelFileNames.append(fname)
            self.Modified(readAgainMesh=False, readAgainModels=True)
        return 1

    def GetModelFileNames(self, idx=None):
        """@desc: Returns the list of file names or given and index returns a specified timestep's filename"""
        if idx is None or not self.ThisHasModels():
            return self.__modelFileNames
        return self.__modelFileNames[idx]

    def GetMeshFileName(self):
        return self.__meshFileName


###############################################################################


# UBC Mesh Reader Base
class ubcMeshReaderBase(TwoFileReaderBase):
    """@desc: A base class for the UBC mesh readers"""
    def __init__(self, nOutputPorts=1, outputType='vtkUnstructuredGrid'):
        TwoFileReaderBase.__init__(self,
            nOutputPorts=nOutputPorts, outputType=outputType)
        self.__dataname = 'Data'
        # For keeping track of type (2D vs 3D)
        self.__sizeM = None


    def Is3D(self):
        return self.__sizeM.shape[0] >= 3

    def Is2D(self):
        return self.__sizeM.shape[0] == 1

    @staticmethod
    def _ubcMesh2D_part(FileName):
        # This is a helper method to read file contents of mesh
        fileLines = np.genfromtxt(FileName, dtype=str, delimiter='\n', comments='!')

        def _genTup(sft, n):
            # This reads in the data for a dimension
            pts = []
            disc = []
            for i in range(n):
                ln = fileLines[i+sft].split('!')[0].split()
                if i is 0:
                    o = ln[0]
                    pts.append(o)
                    ln = [ln[1],ln[2]]
                pts.append(ln[0])
                disc.append(ln[1])
            return pts, disc

        # Get the number of lines for each dimension
        nx = int(fileLines[0].split('!')[0])
        nz = int(fileLines[nx+1].split('!')[0])

        # Get the origins and tups for both dimensions
        xpts, xdisc = _genTup(1, nx)
        zpts, zdisc = _genTup(2+nx, nz)

        return xpts, xdisc, zpts, zdisc

    def _ReadExtent(self):
        """
        @desc:
        Reads the mesh file for the UBC 2D/3D Mesh or OcTree format to get output extents. Computationally inexpensive method to discover whole output extent.

        @returns:
        tuple : This returns a tuple of the whole extent for the grid to be made of the input mesh file (0,n1-1, 0,n2-1, 0,n3-1). This output should be directly passed to `util.SetOutputWholeExtent()` when used in programmable filters or source generation on the pipeline.

        """
        # Read the mesh file as line strings, remove lines with comment = !
        v = np.array(np.__version__.split('.')[0:2], dtype=int)
        FileName = self.GetMeshFileName()
        if v[0] >= 1 and v[1] >= 10:
            # max_rows in numpy versions >= 1.10
            msh = np.genfromtxt(FileName, delimiter='\n', dtype=np.str,comments='!', max_rows=1)
        else:
            # This reads whole file :(
            msh = np.genfromtxt(FileName, delimiter='\n', dtype=np.str, comments='!')[0]
        # Fist line is the size of the model
        self.__sizeM = np.array(msh.ravel()[0].split(), dtype=int)
        # Check if the mesh is a UBC 2D mesh
        if self.__sizeM.shape[0] == 1:
            # Read in data from file
            xpts, xdisc, zpts, zdisc = ubcMeshReaderBase._ubcMesh2D_part(FileName)
            nx = np.sum(np.array(xdisc,dtype=int))+1
            nz = np.sum(np.array(zdisc,dtype=int))+1
            return (0,nx, 0,1, 0,nz)
        # Check if the mesh is a UBC 3D mesh or OcTree
        elif self.__sizeM.shape[0] >= 3:
            # Get mesh dimensions
            dim = self.__sizeM[0:3]
            ne,nn,nz = dim[0], dim[1], dim[2]
            return (0,ne, 0,nn, 0,nz)
        else:
            raise Exception('File format not recognized')


    @staticmethod
    def ubcModel3D(FileName):
        """
        @desc:
        Reads the 3D model file and returns a 1D NumPy float array. Use the PlaceModelOnMesh() method to associate with a grid.

        @params:
        FileName : str : The model file name(s) as an absolute path for the input model file in UBC 3D Model Model Format. Also accepts a `list` of string file names.

        @returns:
        np.array : Returns a NumPy float array that holds the model data read from the file. Use the `PlaceModelOnMesh()` method to associate with a grid. If a list of file names is given then it will return a dictionary of NumPy float array with keys as the basenames of the files.
        """
        if type(FileName) is list:
            out = {}
            for f in FileName:
                out[os.path.basename(f)] = ubcTensorMeshReader.ubcModel3D(f)
            return out

        fileLines = np.genfromtxt(FileName, dtype=str, delimiter='\n', comments='!')
        data = np.genfromtxt((line.encode('utf8') for line in fileLines), dtype=np.float)
        return data


    def SetDataName(self, name):
        """@desc: Set te data array name for the model data on the output grid"""
        if self.__dataname != name:
            self.__dataname = name
            self.Modified(readAgainMesh=False, readAgainModels=False)

    def GetDataName(self):
        return self.__dataname




###############################################################################


# UBC Model Appender Base
class ubcModelAppenderBase(PVGeoAlgorithmBase):
    def __init__(self, inputType='vtkRectilinearGrid', outputType='vtkRectilinearGrid'):
        PVGeoAlgorithmBase.__init__(self,
            nInputPorts=1, inputType=inputType,
            nOutputPorts=1, outputType=outputType)
        self._modelFileNames = []
        self._dataname = 'Appended Data'
        self._models = []
        self.__needToRead = True
        self._is3D = None
        # For the VTK/ParaView pipeline
        self.__dt = 1.0
        self.__timesteps = None
        self.__inTimesteps = None

    def __SetInputTimesteps(self):
        ints = _helpers.GetInputTimeSteps(self)
        self.__inTimesteps = ints if ints is not None else []
        return self.__inTimesteps

    def NeedToRead(self, flag=None):
        """Ask self if the reader needs to read the files again
        if the flag is set then this method will set the read status"""
        if flag is not None and isinstance(flag, (bool, int)):
            self.__needToRead = flag
            self.__UpdateTimeSteps()
        return self.__needToRead

    def Modified(self, readAgain=True):
        """Call modified if the files needs to be read again again"""
        if readAgain: self.__needToRead = readAgain
        PVGeoAlgorithmBase.Modified(self)

    def __UpdateTimeSteps(self):
        """for internal use only: appropriately sets the timesteps"""
        if len(self._modelFileNames) > 0 and len(self._modelFileNames) > len(self.__inTimesteps):
            self.__timesteps = _helpers.UpdateTimeSteps(self, self._modelFileNames, self.__dt)
        # Just use input's time steps which is set by pipeline
        return 1

    def _ReadUpFront(self):
        raise NotImpelementedError()

    def _PlaceOnMesh(self, output, idx=0):
        raise NotImplementedError()


    def RequestData(self, request, inInfo, outInfo):
        """DO NOT OVERRIDE"""
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        output = self.GetOutputData(outInfo, 0)
        output.DeepCopy(pdi) # ShallowCopy if you want changes to propagate upstream
        # Get requested time index
        i = _helpers.GetRequestedTime(self, outInfo)
        # Perfrom task:
        if self.__needToRead:
            self._ReadUpFront()
        # Place the model data for given timestep onto the mesh
        if len(self._models) > i:
            self._PlaceOnMesh(output, idx=i)
        return 1

    def RequestInformation(self, request, inInfo, outInfo):
        """DO NOT OVERRIDE"""
        self.__SetInputTimesteps()
        self.__UpdateTimeSteps()
        pdi = self.GetInputData(inInfo, 0, 0)
        # Determine if 2D or 3D and read
        if isinstance(pdi, vtk.vtkRectilinearGrid) and pdi.GetExtent()[3] == 1:
            self._is3D = False
        else:
            self._is3D = True
        return 1

    #### Setters and Getters ####

    def HasModels(self):
        return len(self._modelFileNames) > 0

    def GetTimestepValues(self):
        """Use this in ParaView decorator to register timesteps"""
        if self.__timesteps is None: self.__timesteps = self.__SetInputTimesteps()
        return self.__timesteps.tolist() if self.__timesteps is not None else None

    def ClearModels(self):
        """Use to clear data file names"""
        self._modelFileNames = []
        self._models = []
        self.Modified(readAgain=True)

    def AddModelFileName(self, fname):
        """Use to set the file names for the reader. Handles singlt string or list of strings."""
        if fname is None:
            return # do nothing if None is passed by a constructor on accident
        if isinstance(fname, list):
            for f in fname:
                self.AddModelFileName(f)
            self.Modified()
        elif fname not in self._modelFileNames:
            self._modelFileNames.append(fname)
            self.Modified()
        return 1

    def GetModelFileNames(self, idx=None):
        """Returns the list of file names or given and index returns a specified timestep's filename"""
        if idx is None or not self.HasModels():
            return self._modelFileNames
        return self._modelFileNames[idx]

    def SetDataName(self, name):
        if self._dataname != name:
            self._dataname = name
            self.Modified(readAgain=False)
