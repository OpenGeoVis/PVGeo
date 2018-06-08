import numpy as np
import vtk
from vtk.util import numpy_support as nps

all = [
    'oddModelExtent',
    'oddModel',

]


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


def oddModelExtent(xcells, ycells, zcells):
    # Read the cell sizes
    cx = _readCellLine(xcells)
    cy = _readCellLine(ycells)
    cz = _readCellLine(zcells)
    ne,nn,nz = len(cx), len(cy), len(cz)
    return (0,ne, 0,nn, 0,nz)



def oddModel(origin, xcells, ycells, zcells, data=None, dataNm='Data', pdo=None):

    if pdo is None:
        pdo = vtk.vtkRectilinearGrid()

    ox,oy,oz = origin[0],origin[1],origin[2]


    # Read the cell sizes
    cx = _readCellLine(xcells)
    cy = _readCellLine(ycells)
    cz = _readCellLine(zcells)

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
    ext = oddModelExtent(xcells, ycells, zcells)
    nx,ny,nz = ext[1]+1,ext[3]+1,ext[5]+1
    pdo.SetDimensions(nx,ny,nz)
    # Convert to VTK array for setting coordinates
    pdo.SetXCoordinates(nps.numpy_to_vtk(num_array=cox,deep=True))
    pdo.SetYCoordinates(nps.numpy_to_vtk(num_array=coy,deep=True))
    pdo.SetZCoordinates(nps.numpy_to_vtk(num_array=coz,deep=True))

    # ADD DATA to cells
    if data is None:
        data = np.random.rand(nx*ny*nz)
        data = nps.numpy_to_vtk(num_array=data,deep=True)
        data.SetName('Random Data')
    else:
        data = nps.numpy_to_vtk(num_array=data,deep=True)
        data.SetName(dataNm)
    pdo.GetCellData().AddArray(data)
