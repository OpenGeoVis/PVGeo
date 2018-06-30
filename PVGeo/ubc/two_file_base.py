all = [
    'TwoFileReaderBase',
    'ubcMeshReaderBase',
]

from .. import _helpers

# Outside Imports:
from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase
import numpy as np


# Two File Reader Base
class TwoFileReaderBase(VTKPythonAlgorithmBase):
    def __init__(self, nOutputPorts=1, outputType='vtkUnstructuredGrid'):
        VTKPythonAlgorithmBase.__init__(self,
            nInputPorts=0,
            nOutputPorts=nOutputPorts, outputType=outputType)
        self.__dt = 1.0
        self.__timesteps = None
        self.__meshFileName = None # Can only be one!
        self.__modelFileNames = [] # Can be many (single attribute, manytimesteps)


    def _GetTimeSteps(self):
        return self.__timesteps.tolist() if self.__timesteps is not None else None

    def _UpdateTimeSteps(self):
        """for internal use only"""
        if len(self.__modelFileNames) < 1:
            return -1
        self.__timesteps = _helpers.UpdateTimesteps(self, self.__modelFileNames, self.__dt)
        return 1

    def RequestInformation(self, request, inInfo, outInfo):
        self._UpdateTimeSteps()
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
        """Use this in ParaView decorator to register timesteps"""
        return self._GetTimeSteps()

    def SetTimeDelta(self, dt):
        """An advanced property for the time step in seconds."""
        if dt != self.__dt:
            self.__dt = dt
            self.Modified()

    def ClearMeshFileName(self):
        """Use to clear mesh file name"""
        self.__meshFileName = None

    def ClearModelFileNames(self):
        """Use to clear data file names"""
        self.__modelFileNames = []

    def SetMeshFileName(self, fname):
        if self.__meshFileName != fname:
            self.__meshFileName = fname

    def AddModelFileName(self, fname):
        """Use to set the file names for the reader. Handles singlt string or list of strings."""
        if fname is None:
            return # do nothing if None is passed by a constructor on accident
        if isinstance(fname, list):
            for f in fname:
                self.AddModelFileName(f)
        elif fname not in self.__modelFileNames:
            self.__modelFileNames.append(fname)
        self.Modified()

    def GetModelFileNames(self, idx=None):
        """Returns the list of file names or given and index returns a specified timestep's filename"""
        if idx is None or not self.ThisHasModels():
            return self.__modelFileNames
        return self.__modelFileNames[idx]

    def GetMeshFileName(self):
        return self.__meshFileName


###############################################################################


# UBC Mesh Reader Base
class ubcMeshReaderBase(TwoFileReaderBase):
    def __init__(self, nOutputPorts=1, outputType='vtkUnstructuredGrid'):
        TwoFileReaderBase.__init__(self,
            nOutputPorts=nOutputPorts, outputType=outputType)

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

        @params:
        FileName : str : The mesh filename as an absolute path for the input mesh file in a UBC Format with extents defined on the first line.

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
        sizeM = np.array(msh.ravel()[0].split(), dtype=int)
        # Check if the mesh is a UBC 2D mesh
        if sizeM.shape[0] == 1:
            # Read in data from file
            xpts, xdisc, zpts, zdisc = ubcMeshReaderBase._ubcMesh2D_part(FileName)
            nx = np.sum(np.array(xdisc,dtype=int))+1
            nz = np.sum(np.array(zdisc,dtype=int))+1
            return (0,nx, 0,1, 0,nz)
        # Check if the mesh is a UBC 3D mesh or OcTree
        elif sizeM.shape[0] >= 3:
            # Get mesh dimensions
            dim = sizeM[0:3]
            ne,nn,nz = dim[0], dim[1], dim[2]
            return (0,ne, 0,nn, 0,nz)
        else:
            raise Exception('File format not recognized')
