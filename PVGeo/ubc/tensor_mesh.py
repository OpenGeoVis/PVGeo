__all__ = [
    'ubcTensorMeshReader',
    'ubcTensorMeshAppender',
]

import numpy as np
from vtk.util import numpy_support as nps
import vtk
import os

from ..base import PVGeoAlgorithmBase
from .two_file_base import ubcMeshReaderBase
from .. import _helpers



class ubcTensorMeshReader(ubcMeshReaderBase):
    """UBC Mesh 2D/3D models are defined using a 2-file format. The "mesh" file describes how the data is discretized. The "model" file lists the physical property values for all cells in a mesh. A model file is meaningless without an associated mesh file. The reader will automatically detect if the mesh is 2D or 3D and read the remainder of the data with that dimensionality assumption. If the mesh file is 2D, then then model file must also be in the 2D format (same for 3D).

    Model File is optional. Reader will still construct vtkRectilinearGrid safely."""
    def __init__(self, nOutputPorts=1, outputType='vtkRectilinearGrid'):
        ubcMeshReaderBase.__init__(self,
            nOutputPorts=nOutputPorts, outputType=outputType)
        self.__dataname = 'Data'


    @staticmethod
    def placeModelOnMesh(mesh, model, dataNm='Data'):
        """
        @desc:
        Places model data onto a mesh. This is for the UBC Grid data reaers to associate model data with the mesh grid.

        @params:
        mesh : vtkRectilinearGrid : The vtkRectilinearGrid that is the mesh to place the model data upon.
        model : np.array : A NumPy float array that holds all of the data to place inside of the mesh's cells.
        dataNm : str : opt : The name of the model data array once placed on the vtkRectilinearGrid.

        @returns:
        vtkRectilinearGrid : Returns the input vtkRectilinearGrid with model data appended.

        """
        if type(model) is dict:
            for key in model.keys():
                mesh = ubcTensorMeshReader.placeModelOnMesh(mesh, model[key], dataNm=key)
            return mesh

        # model.GetNumberOfValues() if model is vtkDataArray
        # Make sure this model file fits the dimensions of the mesh
        ext = mesh.GetExtent()
        n1,n2,n3 = ext[1],ext[3],ext[5]
        if (n1*n2*n3 < len(model)):
            raise Exception('Model `%s` has more data than the given mesh has cells to hold.' % dataNm)
        elif (n1*n2*n3 > len(model)):
            raise Exception('Model `%s` does not have enough data to fill the given mesh\'s cells.' % dataNm)

        # Swap axes because VTK structures the coordinates a bit differently
        #-  This is absolutely crucial!
        #-  Do not play with unless you know what you are doing!
        model = np.reshape(model, (n1,n2,n3))
        model = np.swapaxes(model,0,1)
        model = np.swapaxes(model,0,2)
        # Now reverse Z axis
        model = model[::-1,:,:] # Note it is in Fortran ordering
        model = model.flatten()

        # Convert data to VTK data structure and append to output
        c = nps.numpy_to_vtk(num_array=model,deep=True)
        c.SetName(dataNm)
        # THIS IS CELL DATA! Add the model data to CELL data:
        mesh.GetCellData().AddArray(c)
        return mesh

    #------------------------------------------------------------------#
    #----------------------     UBC MESH 2D    ------------------------#
    #------------------------------------------------------------------#

    @staticmethod
    def ubcMesh2D(FileName, output):
        """
        @desc:
        This method reads a UBC 2D Mesh file and builds an empty vtkRectilinearGrid for data to be inserted into. [Format Specs](http://giftoolscookbook.readthedocs.io/en/latest/content/fileFormats/mesh2Dfile.html)

        @params:
        FileName : str : The mesh filename as an absolute path for the input mesh file in UBC 3D Mesh Format.
        output : vtk.vtkRectilinearGrid : The output data object

        @return:
        vtkRectilinearGrid : Returns a vtkRectilinearGrid generated from the UBC 3D Mesh grid. Mesh is defined by the input mesh file. No data attributes here, simply an empty mesh. Use the `placeModelOnMesh()` method to associate with model data.

        """
        # Read in data from file
        xpts, xdisc, zpts, zdisc = ubcMeshReaderBase._ubcMesh2D_part(FileName)

        nx = np.sum(np.array(xdisc,dtype=int))+1
        nz = np.sum(np.array(zdisc,dtype=int))+1

        # Now generate the vtkRectilinear Grid
        def _genCoords(pts, disc, z=False):
            c = [float(pts[0])]
            for i in range(len(pts)-1):
                start = float(pts[i])
                stop = float(pts[i+1])
                num = int(disc[i])
                w = (stop-start)/num

                for j in range(1,num):
                    c.append(start + (j)*w)
                c.append(stop)
            c = np.array(c,dtype=float)
            if z:
                c = -c[::-1]
            return nps.numpy_to_vtk(num_array=c,deep=True)

        xcoords = _genCoords(xpts, xdisc)
        zcoords = _genCoords(zpts, zdisc, z=True)
        ycoords = nps.numpy_to_vtk(num_array=np.zeros(1),deep=True)

        output.SetDimensions(nx,2,nz) # note this subtracts 1
        output.SetXCoordinates(xcoords)
        output.SetYCoordinates(ycoords)
        output.SetZCoordinates(zcoords)

        return output

    @staticmethod
    def ubcModel2D(FileName):
        """
        @desc:
        Reads a 2D model file and returns a 1D NumPy float array. Use the placeModelOnMesh() method to associate with a grid.

        @params:
        FileName : str : The model filename as an absolute path for the input model file in UBCMesh Model Format. Also accepts a list of string file names.

        @returns:
        np.array : Returns a NumPy float array that holds the model data read from the file. Use the `placeModelOnMesh()` method to associate with a grid. If a list of file names is given then it will return a dictionary of NumPy float array with keys as the basenames of the files.
        """
        if type(FileName) is list:
            out = {}
            for f in FileName:
                out[os.path.basename(f)] = ubcTensorMeshReader.ubcModel2D(f)
            return out

        fileLines = np.genfromtxt(FileName, dtype=str, delimiter='\n', comments='!')
        dim = np.array(fileLines[0].split(), dtype=int)
        data = np.genfromtxt((line.encode('utf8') for line in fileLines[1::]), dtype=np.float)
        if np.shape(data)[0] != dim[1] and np.shape(data)[1] != dim[0]:
            raise Exception('Mode file `%s` improperly formatted.' % FileName)
        return data.flatten(order='F')

    @staticmethod
    def _ubcMeshData2D(FileName_Mesh, FileName_Model, output, dataNm='Data'):
        """Helper method to read a 2D mesh"""
        # Construct/read the mesh
        ubcTensorMeshReader.ubcMesh2D(FileName_Mesh, output)
        if ubcTensorMeshReader.HasModels(FileName_Model):
            # Read the model data
            model = ubcTensorMeshReader.ubcModel2D(FileName_Model)
            # Place the model data onto the mesh
            ubcTensorMeshReader.placeModelOnMesh(output, model, dataNm)
        return output


    #------------------------------------------------------------------#
    #----------------------     UBC MESH 3D    ------------------------#
    #------------------------------------------------------------------#

    @staticmethod
    def ubcMesh3D(FileName, output):
        """
        @desc:
        This method reads a UBC 3D Mesh file and builds an empty vtkRectilinearGrid for data to be inserted into.

        @params:
        FileName : str : The mesh filename as an absolute path for the input mesh file in UBC 3D Mesh Format.
        output : vtk.vtkRectilinearGrid : The output data object

        @returns:
        vtkRectilinearGrid : Returns a vtkRectilinearGrid generated from the UBC 3D Mesh grid. Mesh is defined by the input mesh file. No data attributes here, simply an empty mesh. Use the `placeModelOnMesh()` method to associate with model data.

        """

        #--- Read in the mesh ---#
        fileLines = np.genfromtxt(FileName, dtype=str,
            delimiter='\n', comments='!')

        # Get mesh dimensions
        dim = np.array(fileLines[0].split('!')[0].split(), dtype=int)
        dim = (dim[0]+1, dim[1]+1, dim[2]+1)

        # The origin corner (Southwest-top)
        #- Remember UBC format specifies down as the positive Z
        #- Easting, Northing, Altitude
        oo = np.array(
            fileLines[1].split('!')[0].split(),
            dtype=float
        )
        ox,oy,oz = oo[0],oo[1],oo[2]

        # Read cell sizes for each line in the UBC mesh files
        def _readCellLine(line):
            line_list = []
            for seg in line.split():
                if '*' in seg:
                    sp = seg.split('*')
                    seg_arr = np.ones((int(sp[0]),), dtype=float) * float(sp[1])
                else:
                    seg_arr = np.array([float(seg)], dtype=float)
                line_list.append(seg_arr)
            return np.concatenate(line_list)

        # Read the cell sizes
        cx = _readCellLine(fileLines[2].split('!')[0])
        cy = _readCellLine(fileLines[3].split('!')[0])
        cz = _readCellLine(fileLines[4].split('!')[0])
        # Invert the indexing of the vector to start from the bottom.
        cz = cz[::-1]
        # Adjust the reference point to the bottom south west corner
        oz = oz - np.sum(cz)

        # Now generate the coordinates for from cell width and origin
        cox = ox + np.cumsum(cx)
        cox = np.insert(cox,0,ox)
        coy = oy + np.cumsum(cy)
        coy = np.insert(coy,0,oy)
        coz = oz + np.cumsum(cz)
        coz = np.insert(coz,0,oz)

        # Set the dims and coordinates for the output
        output.SetDimensions(dim[0],dim[1],dim[2])
        # Convert to VTK array for setting coordinates
        output.SetXCoordinates(nps.numpy_to_vtk(num_array=cox,deep=True))
        output.SetYCoordinates(nps.numpy_to_vtk(num_array=coy,deep=True))
        output.SetZCoordinates(nps.numpy_to_vtk(num_array=coz,deep=True))

        return output

    @staticmethod
    def ubcModel3D(FileName):
        """
        @desc:
        Reads the 3D model file and returns a 1D NumPy float array. Use the placeModelOnMesh() method to associate with a grid.

        @params:
        FileName : str : The model file name(s) as an absolute path for the input model file in UBC 3D Model Model Format. Also accepts a `list` of string file names.

        @returns:
        np.array : Returns a NumPy float array that holds the model data read from the file. Use the `placeModelOnMesh()` method to associate with a grid. If a list of file names is given then it will return a dictionary of NumPy float array with keys as the basenames of the files.
        """
        if type(FileName) is list:
            out = {}
            for f in FileName:
                out[os.path.basename(f)] = ubcTensorMeshReader.ubcModel3D(f)
            return out

        fileLines = np.genfromtxt(FileName, dtype=str, delimiter='\n', comments='!')
        data = np.genfromtxt((line.encode('utf8') for line in fileLines), dtype=np.float)
        return data

    @staticmethod
    def _ubcMeshData3D(FileName_Mesh, FileName_Model, output, dataNm='Data'):
        """Helper method to read a 3D mesh"""
        # Construct/read the mesh
        ubcTensorMeshReader.ubcMesh3D(FileName_Mesh, output)
        if ubcTensorMeshReader.HasModels(FileName_Model):
            # Read the model data
            model = ubcTensorMeshReader.ubcModel3D(FileName_Model)
            # Place the model data onto the mesh
            ubcTensorMeshReader.placeModelOnMesh(output, model, dataNm)
        return output

    @staticmethod
    def ubcTensorMesh(FileName_Mesh, FileName_Model, output, dataNm='Data'):
        """
        @desc:
        Wrapper to Read UBC GIF 2D and 3D meshes. UBC Mesh 2D/3D models are defined using a 2-file format. The "mesh" file describes how the data is descritized. The "model" file lists the physical property values for all cells in a mesh. A model file is meaningless without an associated mesh file. If the mesh file is 2D, then then model file must also be in the 2D format (same for 3D).

        @params:
        FileName_Mesh : str : The mesh filename as an absolute path for the input mesh file in UBC 2D/3D Mesh Format
        FileName_Model : str : The model filename as an absolute path for the input model file in UBC 2D/3D Model Format.
        output : vtk.vtkRectilinearGrid : The output data object

        @return:
        vtkRectilinearGrid : Returns a vtkRectilinearGrid generated from the UBC 2D/3D Mesh grid. Mesh is defined by the input mesh file. Cell data is defined by the input model file.
        """
        # Read the mesh file as line strings, remove lines with comment = !
        v = np.array(np.__version__.split('.')[0:2], dtype=int)
        if v[0] >= 1 and v[1] >= 10:
            # max_rows in numpy versions >= 1.10
            msh = np.genfromtxt(FileName_Mesh, delimiter='\n', dtype=np.str,comments='!', max_rows=1)
        else:
            # This reads whole file :(
            msh = np.genfromtxt(FileName_Mesh, delimiter='\n', dtype=np.str, comments='!')[0]
        # Fist line is the size of the model
        sizeM = np.array(msh.ravel()[0].split(), dtype=float)
        # Check if the mesh is a UBC 2D mesh
        if sizeM.shape[0] == 1:
            ubcTensorMeshReader._ubcMeshData2D(FileName_Mesh, FileName_Model, output, dataNm)
        # Check if the mesh is a UBC 3D mesh
        elif sizeM.shape[0] == 3:
            ubcTensorMeshReader._ubcMeshData3D(FileName_Mesh, FileName_Model, output, dataNm)
        else:
            raise Exception('File format not recognized')
        return output

    def RequestData(self, request, inInfo, outInfo):
        # Get output:
        output = self.GetOutputData(outInfo, 0)
        # Get requested time index
        i = _helpers.GetRequestedTime(self, outInfo)
        ubcTensorMeshReader.ubcTensorMesh(
            self.GetMeshFileName(),
            self.GetModelFileNames(idx=i),
            output,
            self.__dataname)

        return 1


    def RequestInformation(self, request, inInfo, outInfo):
        # Call parent to handle time stuff
        ubcMeshReaderBase.RequestInformation(self, request, inInfo, outInfo)
        # Now set whole output extent
        ext = self._ReadExtent()
        info = outInfo.GetInformationObject(0)
        # Set WHOLE_EXTENT: This is absolutely necessary
        info.Set(vtk.vtkStreamingDemandDrivenPipeline.WHOLE_EXTENT(), ext, 6)
        return 1


    def SetDataName(self, name):
        if self.__dataname != name:
            self.__dataname = name
            self.Modified()




class ubcTensorMeshAppender(PVGeoAlgorithmBase):
    """This assumes the input vtkRectilinearGrid has already handled the timesteps"""
    def __init__(self):
        PVGeoAlgorithmBase.__init__(self,
            nInputPorts=1, inputType='vtkRectilinearGrid',
            nOutputPorts=1, outputType='vtkRectilinearGrid')
        self.__modelFileNames = []
        self.__dataname = 'Appended Data'

    def RequestData(self, request, inInfo, outInfo):
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        output = self.GetOutputData(outInfo, 0)
        output.DeepCopy(pdi) # ShallowCopy if you want changes to propagate upstream
        # Get requested time index
        i = _helpers.getTimeStepFileIndex(self, self.__modelFileNames, dt=1.0)
        # Perfrom task:
        #- Determine if 2D or 3D and read
        if pdi.GetExtent()[3] == 1:
            # Not how in UBC format, 2D grids are specified on an XZ plane (no Y component)
            # This will only work prior to rotations to account for real spatial reference
            model = ubcTensorMeshReader.ubcModel2D(self.__modelFileNames[i])
        else:
            model = ubcTensorMeshReader.ubcModel3D(self.__modelFileNames[i])
        #- Place read model on the mesh
        ubcTensorMeshReader.placeModelOnMesh(output, model, self.__dataname)
        return 1

    #### Setters and Getters ####

    def HasModels(self):
        return len(self.__modelFileNames) > 0

    def ClearModelFileNames(self):
        """Use to clear data file names"""
        self.__modelFileNames = []

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
        if idx is None or not self.HasModels():
            return self.__modelFileNames
        return self.__modelFileNames[idx]

    def SetDataName(self, name):
        if self.__dataname != name:
            self.__dataname = name
            self.Modified()
