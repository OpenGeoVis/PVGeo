import vtk
from vtk.util import numpy_support as nps
import numpy as np



def CtoF(arr, extent):
    """
    Transforms for C- to F-Contiguosness
    """
    n1,n2,n3 = extent[0],extent[1],extent[2]
    arr = np.reshape(arr, (n1,n2,n3))
    arr = np.swapaxes(arr,0,2)
    arr = np.reshape(arr, (n1*n2*n3))
    return arr

def rearangeSEPlib(arr, extent):
    # SWAP D1 AND D3 THEN SWAP D2 AND D1
    n3,n1,n2 = extent[0],extent[1],extent[2]
    arr = np.reshape(arr, (n3,n1,n2))
    arr = np.swapaxes(arr,0,2)
    arr = np.swapaxes(arr,0,1)
    arr = np.reshape(arr, (n1*n2*n3))
    return arr, (n3,n1,n2)


def tableToGrid(pdi, extent, spacing, origin, SEPlib=False, C_ordering=True):
    cols = pdi.GetNumberOfColumns()
    rows = pdi.GetColumn(0).GetNumberOfTuples()

    # Output Data Type:
    image = vtk.vtkImageData() # vtkImageData

    # Setup the ImageData
    if SEPlib:
        # SEPlib: d1=z, d2=x, d3=y
        nz,nx,ny = extent[0],extent[1],extent[2]
        sz,sx,sy = spacing[0],spacing[1],spacing[2]
        oz,ox,oy = origin[0],origin[1],origin[2]
    else:
        # Cartesian: d1=x, d2=y, d3=z
        nx,ny,nz = extent[0],extent[1],extent[2]
        sx,sy,sz = spacing[0],spacing[1],spacing[2]
        ox,oy,oz = origin[0],origin[1],origin[2]

    # make sure dimensions work
    if (nx*ny*nz != rows):
        raise Exception('Total number of elements must remain %d. Check reshape dimensions (n1 by n2 by n3).' % (rows))

    image.SetDimensions(nx, ny, nz)
    image.SetOrigin(ox, oy, oz)
    image.SetSpacing(sx, sy, sz)
    image.SetExtent(0,nx-1, 0,ny-1, 0,nz-1)


    # Add all columns of the table as arrays to the PointData
    for i in range(cols):
        c = pdi.GetColumn(i)
        name = c.GetName()
        arr = nps.vtk_to_numpy(c)
        if C_ordering:
            arr = CtoF(arr, (nx,ny,nz))
        if SEPlib:
            arr, ext = rearangeSEPlib(arr, (nx,ny,nz))
            """if C_ordering:
                arr = CtoF(arr, (nx,ny,nz))"""
        c = nps.numpy_to_vtk(num_array=arr,deep=True)
        c.SetName(name)
        #image.GetCellData().AddArray(c) # Should we add here? flipper won't flip these...
        image.GetPointData().AddArray(c)

    return image
