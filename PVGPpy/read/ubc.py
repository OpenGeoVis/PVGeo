import numpy as np
import struct
import csv
import os
from vtk.util import numpy_support as nps
import vtk

#-----------------------    UBC MESH    -------------------------#
def ubcMeshExtnet(FileName_Mesh, deli=' ', useTab=False):
    """
    Description
    -----------
    Reads the mesh file for the UBCMesh format to get output extents. Computationally inexpensive method to discover whole output extent.

    Parameters
    ----------
    `FileName_Mesh` : str

    - The mesh filename as an absolute path for the input mesh file in UBCMesh Format.

    `deli` : str, optional

    - The delimiter field used in the input file. Default is a space character.

    `useTab` : boolean, optional

    - An optional flag to use a tab delimiter in the input file.

    Returns
    -------
    This returns a tuple of the whole extent for the rectilinear grid to be made of the input mesh file (0,n1-1, 0,n2-1, 0,n3-1). This output should be directly passed to util.SetOutputWholeExtent() when used in programmable filters or source generation on the pipeline.

    """
    if (useTab):
        deli = '\t'

    # Read in the mesh and set up structure of output grid from mesh file input
    with open(FileName_Mesh) as f:
        reader = csv.reader(f, delimiter=deli)
        h = reader.next()
        # TODO: ignore header lines if start with '!'
        # Ignore header lines if start with '!'
        while h[0][0] == '!':
            h = reader.next()
        # Number of CELLS in each axial direction. Points would be +1
        n1,n2,n3 = int(h[0]), int(h[1]), int(h[2])
        f.close()

    return (0,n1, 0,n2, 0,n3)


def ubcMesh(FileName_Mesh, deli=' ', useTab=False, pdo=None):
    """
    Description
    -----------
    This method reads a UBC Mesh file and builds an empty vrtkRectilinearGrid for data to be inserted into. Default file delimiter is a space character.

    Parameters
    ----------
    `FileName_Mesh` : str

    - The mesh filename as an absolute path for the input mesh file in UBCMesh Format.

    `deli` : str, optional

    - The delimiter field used in the input file. Default is a space character.

    `useTab` : boolean, optional

    - An optional flag to use a tab delimiter in the input file.

    Returns
    -------
    Returns a vtkRectilinearGrid generated from the UBCMesh grid. Mesh is defined by the input mesh file. No data attributes here, simply an empty mesh. Use the placeModelOnMesh() method to associate with model data.

    """
    if pdo is None:
        pdo = vtk.vtkRectilinearGrid() # vtkRectilinearGrid

    # Set the tab delimiter if needed
    if (useTab):
        deli = '\t'

    #--- Read in the mesh ---#
    with open(FileName_Mesh) as f:
        reader = csv.reader(f, delimiter=deli)
        h = reader.next()
        # Ignore header lines if start with '!'
        while h[0][0] == '!':
            h = reader.next()

        # Number of CELLS in each axial direction
        n1,n2,n3 = int(h[0]), int(h[1]), int(h[2])
        numCells = n1*n2*n3
        # Change to number of POINTS in each axial direction
        #- We do ths because we have to specify the points along each axial dir
        nn = [n1,n2,n3] = [n1+1,n2+1,n3+1]

        # The origin corner (South-west-top)
        #- Remember UBC Mesh Specifies down as the positive Z
        h = reader.next()
        oo = [o1,o2,o3] = [float(h[0]), float(h[1]), float(h[2])]

        vv = [None, None, None]
        for i in range(3):
            # Get spacings for this dimension:
            h = reader.next()
            # Construct coordinates on this axis
            s = np.zeros(nn[i])
            s[0] = o1
            for j in range(1, nn[i]):
                if (i == 2):
                    # Z dimension (down is positive Z!)
                    #  TODO: what is the correct way to do this?
                    s[j] = s[j-1] + float(h[j-1])
                else:
                    # X and Y dimensions
                    s[j] = s[j-1] + float(h[j-1])
            # Convert to VTK array for setting coordinates
            vv[i] = nps.numpy_to_vtk(num_array=s,deep=True)

        # Set the dims and coordinates for the output
        pdo.SetDimensions(n1,n2,n3)
        pdo.SetXCoordinates(vv[0])
        pdo.SetYCoordinates(vv[1])
        pdo.SetZCoordinates(vv[2])

        f.close()

    return pdo





def ubcModel(FileName_Model, deli=' ', useTab=False):
    """
    Description
    -----------
    Reads the model file and returns a 1D NumPy float array. Use the placeModelOnMesh() method to associate with a grid.

    Parameters
    ----------
    `FileName_Model` : str

    - The model filename as an absolute path for the input model file in UBCMesh Format.

    `deli` : str, optional

    - The delimiter field used in the input file. Default is a space character.

    `useTab` : boolean, optional

    - An optional flag to use a tab delimiter in the input file.

    Returns
    -------
    Returns a NumPy float array that holds the model data read from the file. Use the placeModelOnMesh() method to associate with a grid.
    """
    #--- Read in the model ---#
    # Count number of lines in file
    with open(FileName_Model) as f:
        for i, l in enumerate(f):
            pass
        numLines = i + 1
        f.close()
    # Read in data from file with new iterator
    with open(FileName_Model) as f:
        h = f.next()
        skipped = 0
        # Ignore header lines if start with '!'
        while h[0][0] == '!':
            h = f.next()
            skipped += 1
        # Iterate over everyline of the file and pull data
        # TODO: can we just iterate over each line for 1D then reshape to 3D?
        data = np.zeros((numLines-skipped), dtype=float)
        idx = 0
        try:
            for i, l in enumerate(f):
                if idx >= numLines-skipped:
                    break
                data[idx] = float(str.strip(l))
                idx += 1
        except StopIteration:
            print('StopIteration encountered while reading the model file.')
            pass
        f.close()

    return data

def placeModelOnMesh(mesh, model, dataNm='Data'):
    """
    Description
    -----------
    Places model data onto a mesh. This is for the UBC Grid data reaers to associate model data with the mesh grid.

    Parameters
    ----------
    `mesh` : vtkRectilinearGrid

    - The vtkRectilinearGrid that is the mesh to place the model data upon.

    `model` : NumPy float array

    - A NumPy float array that holds all of the data to place inside of the mesh's cells.

    `dataNm` : str, optional

    - The name of the model data array once placed on the vtkRectilinearGrid.

    Returns
    -------
    Returns the input vtkRectilinearGrid with model data appended.

    """
    # model.GetNumberOfValues() if model is vtkDataArray
    # Make sure this model file fits the dimensions of the mesh
    ext = mesh.GetExtent()
    n1,n2,n3 = ext[1],ext[3],ext[5]
    if (n1*n2*n3 < len(model)):
        raise Exception('This model file has more data than the given mesh has cells to hold.')
    elif (n1*n2*n3 > len(model)):
        raise Exception('This model file does not have enough data to fill the given mesh\'s cells.')

    # Swap axes because VTK structures the coordinates a bit differently
    #-  This is absolutely crucial!
    #-  Do not play with unless you know what you are doing!
    model = np.reshape(model, (n1,n2,n3))
    model = np.swapaxes(model,0,1)
    model = np.swapaxes(model,0,2)
    model = model.flatten()

    # Convert data to VTK data structure and append to output
    c = nps.numpy_to_vtk(num_array=model,deep=True)
    c.SetName(dataNm)
    # THIS IS CELL DATA! Add the model data to CELL data:
    mesh.GetCellData().AddArray(c)
    return mesh

def ubcGridData(FileName_Mesh, FileName_Model, deli=' ', useTab=False, dataNm='', pdo=None):
    """
    Description
    -----------
    UBC Mesh 3D models are defined using a 2-file format. The "mesh" file describes how the data is descritized. The "model" file lists the physical property values for all cells in a mesh. A model file is meaningless without an associated mesh file. Default file delimiter is a space character.

    Parameters
    ----------
    `FileName_Mesh` : str

    - The mesh filename as an absolute path for the input mesh file in UBCMesh Format

    `FileName_Model` : str

    - The model filename as an absolute path for the input model file in UBCMesh Format.

    `deli` : str, optional

    - The delimiter field used in the input file. Default is a space character.

    `useTab` : boolean, optional

    - An optional flag to use a tab delimiter in the input file.

    `dataNm` : str, optional

    - The name of the model data array once placed on the vtkRectilinearGrid.

    Returns
    -------
    Returns a vtkRectilinearGrid generated from the UBCMesh grid. Mesh is defined by the input mesh file. Cell data is defined by the input model file.

    """
    # If no name given for data by user, use the basename of the file
    if dataNm == '':
        dataNm = os.path.basename(FileName_Model)
    # Construct/read the mesh
    mesh = ubcMesh(FileName_Mesh, deli, useTab, pdo=pdo)
    # Read the model data
    model = ubcModel(FileName_Model, deli, useTab)
    # Place the model data onto the mesh
    grd = placeModelOnMesh(mesh, model, dataNm)
    return grd
