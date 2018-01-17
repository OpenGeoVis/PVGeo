import vtk
import numpy as np
from vtk.util import numpy_support as nps

#---- Reshape Table ----#

def reshapeTable(pdi, nrows, ncols, pdo=None):
    """
    Todo Description
    """
    if pdo is None:
        pdo = vtk.vtkTable()
    # Get number of columns
    cols = pdi.GetNumberOfColumns()
    # Get number of rows
    rows = pdi.GetColumn(0).GetNumberOfTuples() # TODO is the necessary?

    # Make a 2D numpy array and fille with data from input table
    data = np.empty((cols,rows))
    for i in range(cols):
        c = pdi.GetColumn(i)
        data[i] = nps.vtk_to_numpy(c)

    order = 'C'
    '''
    # Cannot use Fortran because nps needs contigous arrays
    if Fortran_Ordering:
        order = 'F'
    '''

    if ((ncols*nrows) != (cols*rows)):
        raise Exception('Total number of elements must remain %d. Check reshape dimensions.' % (cols*rows))

    # Use numpy.reshape() to reshape data NOTE: only 2D because its a table
    # NOTE: column access of this reshape is not contigous
    data = np.reshape(data, (nrows,ncols), order=order)
    pdo.SetNumberOfRows(nrows)

    # Add new array to output table and assign incremental names (e.g. Field0)
    for i in range(ncols):
        # Make a contigous array from the column we want
        col = np.array(data[:,i])
        # allow type to be determined by input
        insert = nps.numpy_to_vtk(num_array=col, deep=True) # array_type=vtk.VTK_FLOAT
        # VTK arrays need a name. Set arbitrarily
        insert.SetName('Field%d' % i)
        #pdo.AddColumn(insert) # these are not getting added to the output table
        # ... work around:
        pdo.GetRowData().AddArray(insert) # NOTE: this is in the FieldData

    return pdo


#---- LatLon to Cartesian ----#
def latLonTableToCartesian(pdi, lat_i, lon_i, radius=6371.0, pdo=None):
    # TODO: This is very poorly done
    # TODO: filter works but assumes a spherical earth wich is very wrong
    # NOTE: Msatches the vtkEarth SOurce however so we gonna keep it this way
    if pdo is None:
        pdo = vtk.vtkTable()
    pdo.DeepCopy(pdi)

    # Get number of columns
    ncols = pdi.GetNumberOfColumns()
    nrows = pdi.GetColumn(0).GetNumberOfTuples()

    # Make a 2D numpy array and fille with data from input table
    data = np.empty((nrows,ncols))
    for i in range(ncols):
        c = pdi.GetColumn(i)
        data[:,i] = nps.vtk_to_numpy(c)

    rad = 2 * np.pi / 360.0
    coords = np.empty((nrows,3))
    row_i = 0
    '''
    for r in data:
        x = radius * cos(r[lat_i] * rad) * cos(r[lon_i] * rad)
        y = radius * cos(r[lat_i] * rad) * sin(r[lon_i] * rad)
        z = radius * sin(r[lat_i] * rad)
        coords[row_i] = [x,y,z]
        row_i = row_i + 1
    '''
    x = radius * cos(data[:,lat_i] * rad) * cos(data[:,lon_i] * rad)
    y = radius * cos(data[:,lat_i] * rad) * sin(data[:,lon_i] * rad)
    z = radius * sin(data[:,lat_i] * rad)
    coords[:,0] = x
    coords[:,1] = y
    coords[:,2] = z
    # Add coords to ouptut table
    for i in range(3):
        col = np.array(coords[:,i])
        insert = nps.numpy_to_vtk(num_array=col, deep=True) # array_type=vtk.VTK_FLOAT
        # VTK arrays need a name.
        if i == 0:
            insert.SetName('X')
        elif i == 1:
            insert.SetName('Y')
        elif i == 2:
            insert.SetName('Z')
        #pdo.AddColumn(insert) # these are not getting added to the output table
        # ... work around:
        pdo.GetRowData().AddArray(insert) # NOTE: this is in the FieldData
    return pdo
