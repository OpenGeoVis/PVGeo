from .tensor_mesh import *
from .octree import *


#------------------------------------------------------------------#
# General Methods for UBC Formats
#------------------------------------------------------------------#

def ubcExtent(FileName):
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
        xpts, xdisc, zpts, zdisc = _ubcMesh2D_part(FileName)
        nx = np.sum(np.array(xdisc,dtype=int))+1
        nz = np.sum(np.array(zdisc,dtype=int))+1
        return (0,nx, 0,1,  0,nz)
    # Check if the mesh is a UBC 3D mesh or OcTree
    elif sizeM.shape[0] >= 3:
        # Get mesh dimensions
        dim = sizeM[0:3]
        ne,nn,nz = dim[0], dim[1], dim[2]
        return (0,ne, 0,nn, 0,nz)
    else:
        raise Exception('File format not recognized')
