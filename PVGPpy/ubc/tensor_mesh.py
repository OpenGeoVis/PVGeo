__all__ = [
    # 2D Mesh
    'ubcMesh2D',
    'ubcModel2D',

    # 3D Mesh
    'ubcMesh3D',
    'ubcModel3D',

    # Both
    'placeModelOnMesh',
    'ubcTensorMesh',
]

import numpy as np
import struct
import csv
import os
from vtk.util import numpy_support as nps
import vtk
# Import Helpers:
from ._helpers import *


#------------------------------------------------------------------#
#----------------------     UBC MESH 2D    ------------------------#
#------------------------------------------------------------------#

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

def ubcMesh2D(FileName, pdo=None):
    """
    @desc:
    This method reads a UBC 2D Mesh file and builds an empty vtkRectilinearGrid for data to be inserted into. [Format Specs](http://giftoolscookbook.readthedocs.io/en/latest/content/fileFormats/mesh2Dfile.html)

    @params:
    FileName : str : The mesh filename as an absolute path for the input mesh file in UBC 3D Mesh Format.
    pdo : vtk.vtkRectilinearGrid : opt : The output data object

    @return:
    vtkRectilinearGrid : Returns a vtkRectilinearGrid generated from the UBC 3D Mesh grid. Mesh is defined by the input mesh file. No data attributes here, simply an empty mesh. Use the `placeModelOnMesh()` method to associate with model data.

    """
    if pdo is None:
        pdo = vtk.vtkRectilinearGrid() # vtkRectilinearGrid

    # Read in data from file
    xpts, xdisc, zpts, zdisc = _ubcMesh2D_part(FileName)

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

    pdo.SetDimensions(nx,2,nz) # note this subtracts 1
    pdo.SetXCoordinates(xcoords)
    pdo.SetYCoordinates(ycoords)
    pdo.SetZCoordinates(zcoords)

    return pdo

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
            out[os.path.basename(f)] = ubcModel2D(f)
        return out

    fileLines = np.genfromtxt(FileName, dtype=str, delimiter='\n', comments='!')
    dim = np.array(fileLines[0].split(), dtype=int)
    data = np.genfromtxt((line.encode('utf8') for line in fileLines[1::]), dtype=np.float)
    if np.shape(data)[0] != dim[1] and np.shape(data)[1] != dim[0]:
        raise Exception('Mode file `%s` improperly formatted.' % FileName)
    return data.flatten(order='F')

def _ubcMeshData2D(FileName_Mesh, FileName_Model, pdo=None):
    """Helper method to read a 2D mesh"""
    # Construct/read the mesh
    mesh = ubcMesh2D(FileName_Mesh, pdo=pdo)
    # Read the model data
    model = ubcModel2D(FileName_Model)
    # Place the model data onto the mesh
    grd = placeModelOnMesh(mesh, model)
    return grd


#------------------------------------------------------------------#
#----------------------     UBC MESH 3D    ------------------------#
#------------------------------------------------------------------#

def ubcMesh3D(FileName, pdo=None):
    """
    @desc:
    This method reads a UBC 3D Mesh file and builds an empty vtkRectilinearGrid for data to be inserted into.

    @params:
    FileName : str : The mesh filename as an absolute path for the input mesh file in UBC 3D Mesh Format.
    pdo : vtk.vtkRectilinearGrid : opt : The output data object

    @returns:
    vtkRectilinearGrid : Returns a vtkRectilinearGrid generated from the UBC 3D Mesh grid. Mesh is defined by the input mesh file. No data attributes here, simply an empty mesh. Use the `placeModelOnMesh()` method to associate with model data.

    """
    if pdo is None:
        pdo = vtk.vtkRectilinearGrid() # vtkRectilinearGrid

    #--- Read in the mesh ---#
    fileLines = np.genfromtxt(FileName, dtype=str,
        delimiter='\n', comments='!')

    # Get mesh dimensions
    dim = np.array(fileLines[0].
        split('!')[0].split(), dtype=int)
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
    pdo.SetDimensions(dim[0],dim[1],dim[2])
    # Convert to VTK array for setting coordinates
    pdo.SetXCoordinates(nps.numpy_to_vtk(num_array=cox,deep=True))
    pdo.SetYCoordinates(nps.numpy_to_vtk(num_array=coy,deep=True))
    pdo.SetZCoordinates(nps.numpy_to_vtk(num_array=coz,deep=True))

    return pdo

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
            out[os.path.basename(f)] = ubcModel3D(f)
        return out

    fileLines = np.genfromtxt(FileName, dtype=str, delimiter='\n', comments='!')
    data = np.genfromtxt((line.encode('utf8') for line in fileLines), dtype=np.float)
    return data

def _ubcMeshData3D(FileName_Mesh, FileName_Model, pdo=None):
    """Helper method to read a 3D mesh"""
    # Construct/read the mesh
    mesh = ubcMesh3D(FileName_Mesh, pdo=pdo)
    # Read the model data
    model = ubcModel3D(FileName_Model)
    # Place the model data onto the mesh
    grd = placeModelOnMesh(mesh, model)
    return grd


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
            mesh = placeModelOnMesh(mesh, model[key], dataNm=key)
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


def ubcTensorMesh(FileName_Mesh, FileName_Model, pdo=None):
    """
    @desc:
    Wrapper to Read UBC GIF 2D and 3D meshes. UBC Mesh 2D/3D models are defined using a 2-file format. The "mesh" file describes how the data is descritized. The "model" file lists the physical property values for all cells in a mesh. A model file is meaningless without an associated mesh file. If the mesh file is 2D, then then model file must also be in the 2D format (same for 3D).

    @params:
    FileName_Mesh : str : The mesh filename as an absolute path for the input mesh file in UBC 2D/3D Mesh Format
    FileName_Model : str : The model filename as an absolute path for the input model file in UBC 2D/3D Model Format.
    pdo : vtk.vtkRectilinearGrid : opt : The output data object

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
        pdo = _ubcMeshData2D(FileName_Mesh, FileName_Model, pdo=pdo)
    # Check if the mesh is a UBC 3D mesh
    elif sizeM.shape[0] == 3:
        pdo = _ubcMeshData3D(FileName_Mesh, FileName_Model, pdo=pdo)
    else:
        raise Exception('File format not recognized')
    return pdo
