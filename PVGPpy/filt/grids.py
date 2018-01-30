import vtk
from vtk.util import numpy_support as nps
import numpy as np

#---- Table To Grid Stuff ----#


def _refold(arr, extent, order='F', swapXY=False):
    """
    This is a helper method that handles the initial unpacking of a data array.
    ParaView and VTK use Fortran packing so this is convert data saved in
    C packing to Fortran packing.
    the extent passed to this function is straight from the user...
        either C (nx,ny,nz) or F (nz,ny,nz)
    the extent returned is (nz,ny,nx)
    """
    idx = refoldidx(order=order)
    nx,ny,nz = extent[idx[0]],extent[idx[1]],extent[idx[2]]
    n1,n2,n3 = extent[0],extent[1],extent[2]

    if order == 'C':
        if swapXY:
            arr = np.reshape(arr, (ny,nx,nz))
            arr = np.swapaxes(arr,0,1)
        else:
            arr = np.reshape(arr, (nx,ny,nz))
        arr = np.swapaxes(arr,0,2) # Shape should be (nz,ny,nx)
    elif order == 'F':
        # Update extent to be fortran like
        if swapXY:
            arr = np.reshape(arr, (nz,ny,nx))
            arr = np.swapaxes(arr,1,2) # Shape should be (nz,ny,nx)

    return arr.flatten(), (nz,ny,nx)

def refoldidx(swapXY=False):
    """
    Theses are indexing corrections to set the spacings and origin witht the correct axes after refolding.
    """
    if order == 'F':
        idx = (2,1,0)
        if swapXY:
            idx = (2,0,1)
    else:
        idx = (0,1,2)
        if swapXY:
            idx = (1,0,2)
    return idx

def tableToGrid(pdi, extent, spacing=(1,1,1), origin=(0,0,0), order='F', swapXY=False, pdo=None):
    """
    Converts a table of data arrays to vtkImageData given an extent to reshape that table.
    Each column in the table will be treated as seperate data arrays for the described data space
    """
    cols = pdi.GetNumberOfColumns()
    rows = pdi.GetColumn(0).GetNumberOfTuples()

    # Output Data Type:
    if pdo is None:
        pdo = vtk.vtkImageData()

    idx = refoldidx(order=order)
    nx,ny,nz = extent[idx[0]],extent[idx[1]],extent[idx[2]]
    sx,sy,sz = spacing[idx[0]],spacing[idx[1]],spacing[idx[2]]
    ox,oy,oz = origin[idx[0]],origin[idx[1]],origin[idx[2]]
    # make sure dimensions work
    if (nx*ny*nz != rows):
        raise Exception('Total number of elements must remain %d. Check reshape dimensions (n1 by n2 by n3).' % (rows))

    pdo.SetDimensions(nx, ny, nz)
    pdo.SetOrigin(ox, oy, oz)
    pdo.SetSpacing(sx, sy, sz)
    pdo.SetExtent(0,nx-1, 0,ny-1, 0,nz-1)

    # Add all columns of the table as arrays to the PointData
    for i in range(cols):
        c = pdi.GetColumn(i)
        name = c.GetName()
        arr = nps.vtk_to_numpy(c)
        arr, ext = _refold(arr, extent, order=order, swapXY=swapXY)
        c = nps.numpy_to_vtk(num_array=arr,deep=True)
        c.SetName(name)
        #pdo.GetCellData().AddArray(c) # Should we add here? flipper won't flip these...
        pdo.GetPointData().AddArray(c)

    return pdo




#---- Reverse Grid Axii ----#




def reverseGridAxii(pdi, axes=(True,True,True), pdo=None):
    """
    Reverses data along different axial directions

    TODO: Description
    """
    if pdo is None:
        pdo = vtk.vtkImageData()

    # Copy over input to output to be flipped around
    # Deep copy keeps us from messing with the input data
    pdo.DeepCopy(pdi)

    # Iterate over all array in the PointData
    for j in range(pdo.GetPointData().GetNumberOfArrays()):
        # Swap Scalars with all Arrays in PointData so that all data gets filtered
        scal = pdo.GetPointData().GetScalars()
        arr = pdi.GetPointData().GetArray(j)
        pdo.GetPointData().SetScalars(arr)
        pdo.GetPointData().AddArray(scal)
        for i in range(3):
            # Rotate ImageData on each axis if needed
            # Go through each axis and rotate if needed
            # Note: ShallowCopy is necessary!!
            if axes[i]:
                flipper = vtk.vtkImageFlip()
                flipper.SetInputData(pdo)
                flipper.SetFilteredAxis(i)
                flipper.Update()
                flipper.UpdateWholeExtent()
                pdo.ShallowCopy(flipper.GetOutput())
    return pdo




#---- Translate Grid Origin ----#


def translateGridOrigin(pdi, corner=1, pdo=None):
    """
    TODO: Description


    <Entry value="1" text="South East Bottom"/>
    <Entry value="2" text="North West Bottom"/>
    <Entry value="3" text="North East Bottom"/>
    <Entry value="4" text="South West Top"/>
    <Entry value="5" text="South East Top"/>
    <Entry value="6" text="North West Top"/>
    <Entry value="7" text="North East Top"/>
    """
    if pdo is None:
        pdo = vtk.vtkImageData()

    [nx, ny, nz] = pdi.GetDimensions()
    [ox, oy, oz] = pdi.GetOrigin()
    # TODO: what about spacing???

    pdo.DeepCopy(pdi)

    xx,yy,zz = 0.0,0.0,0.0

    if Corner == 1:
        # South East Bottom
        xx = ox - nx
        yy = oy
        zz = oz
    elif Corner == 2:
        # North West Bottom
        xx = ox
        yy = oy - ny
        zz = oz
    elif Corner == 3:
        # North East Bottom
        xx = ox - nx
        yy = oy - ny
        zz = oz
    elif Corner == 4:
        # South West Top
        xx = ox
        yy = oy
        zz = oz - nz
    elif Corner == 5:
        # South East Top
        xx = ox - nx
        yy = oy
        zz = oz - nz
    elif Corner == 6:
        # North West Top
        xx = ox
        yy = oy - ny
        zz = oz - nz
    elif Corner == 7:
        # North East Top
        xx = ox - nx
        yy = oy - ny
        zz = oz - nz

    pdo.SetOrigin(xx, yy, zz)

    return pdo
