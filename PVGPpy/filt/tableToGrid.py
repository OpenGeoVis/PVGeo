import vtk
from vtk.util import numpy_support as nps
import numpy as np

def unpack(arr, extent, order='C'):
    """
    This is a helper method that handles the initial unpacking of a data array.
    ParaView and VTK use Fortran packing so this is convert data saved in
    C packing to Fortran packing.
    """
    n1,n2,n3 = extent[0],extent[1],extent[2]
    if order == 'C':
        arr = np.reshape(arr, (n1,n2,n3))
        arr = np.swapaxes(arr,0,2)
    elif order == 'F':
        # effectively doing nothing
        #arr = np.reshape(arr, (n3,n2,n1))
        return arr.flatten(), extent
    return arr.flatten(), extent


def rearangeSEPlib(arr, extent):
    """
    This is a helper method to swap axes when using SEPlib axial conventions.
    """
    n1,n2,n3 = extent[0],extent[1],extent[2]
    arr = np.reshape(arr, (n3,n2,n1))
    arr = np.swapaxes(arr,0,2)
    return arr.flatten(), (n1,n2,n3)


def refold(arr, extent, SEPlib=True, order='F'):
    """
    This is a helper method to handle grabbing a data array and make sure it is
    ready for VTK/Fortran ordering in vtkImageData.
    """
    # Fold into 3D using extents. Packing dimensions should be in order extent
    if order == 'F' and not SEPlib:
        arr, extent = unpack(arr, extent, order='F')
    elif order == 'C' and not SEPlib:
        arr, extent = unpack(arr, extent, order='C')
    elif order == 'C' and SEPlib:
        arr, extent = unpack(arr, extent, order='C')
        arr, extent = rearangeSEPlib(arr, extent)
    elif order == 'F' and SEPlib:
        arr, extent = unpack(arr, extent, order='F')
        arr, extent = rearangeSEPlib(arr, extent)
    else:
        raise Exception('Refold case not implemented.')
    return arr, extent

def refoldidx(SEPlib=True):
    if SEPlib:
        idx = (2,1,0)
    else:
        idx = (0,1,2)
    return idx

def tableToGrid(pdi, extent, spacing=(1,1,1), origin=(0,0,0), SEPlib=True, order='F'):
    """
    Converts a table of data arrays to vtkImageData given an extent to reshape that table.
    Each column in the table will be treated as seperate data arrays for the described data space
    """
    cols = pdi.GetNumberOfColumns()
    rows = pdi.GetColumn(0).GetNumberOfTuples()

    # Output Data Type:
    image = vtk.vtkImageData() # vtkImageData

    idx = refoldidx(SEPlib=SEPlib)
    nx,ny,nz = extent[idx[0]],extent[idx[1]],extent[idx[2]]
    sx,sy,sz = spacing[idx[0]],spacing[idx[1]],spacing[idx[2]]
    ox,oy,oz = origin[idx[0]],origin[idx[1]],origin[idx[2]]
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
        arr, ext = refold(arr, extent, SEPlib=SEPlib, order=order)
        c = nps.numpy_to_vtk(num_array=arr,deep=True)
        c.SetName(name)
        #image.GetCellData().AddArray(c) # Should we add here? flipper won't flip these...
        image.GetPointData().AddArray(c)

    return image
