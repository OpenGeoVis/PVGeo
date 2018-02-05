import vtk
import numpy as np
from vtk.util import numpy_support as nps
from vtk.numpy_interface import dataset_adapter as dsa
from PVGPpy.helpers import *

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
def latLonTableToCartesian(pdi, (namelat, fieldlat), (namelon, fieldlon), radius=6371.0, pdo=None):
    # TODO: This is very poorly done
    # TODO: filter works but assumes a spherical earth wich is VERY wrong
    # NOTE: Mismatches the vtkEarth Source however so we gonna keep it this way
    raise Exception('latLonTableToCartesian() not currently implemented.')
    if pdo is None:
        pdo = vtk.vtkPolyData()
    #pdo.DeepCopy(pdi)
    wpdo = dsa.WrapDataObject(pdo)

    # Get the input arrays
    wpdi = dsa.WrapDataObject(pdi)
    lat = getArray(wpdi, fieldlat, namelat)
    lon = getArray(wpdi, fieldlon, namelon)
    if len(lat) != len(lon):
        raise Exception('Latitude and Longitude arrays must be same length.')

    rad = 2 * np.pi / 360.0
    coords = np.empty((len(lat),3))

    coords[:,0] = radius * np.cos(lat * rad) * np.cos(lon * rad)
    coords[:,1] = radius * np.cos(lat * rad) * np.sin(lon * rad)
    coords[:,2] = radius * np.sin(lat * rad)

    #insert = nps.numpy_to_vtk(num_array=coords, deep=True)
    #insert.SetName('Coordinates')
    # Add coords to ouptut table
    wpdo.Points = coords
    pts = vtk.vtkPoints()
    polys = vtk.vtkCellArray()
    k = 1
    # TODO: wee need point cells????
    for r in coords:
        pts.InsertNextPoint(r[0],r[1],r[2])
        polys.InsertNextCell(1)
        polys.InsertCellPoint(k)
        k = k + 1
    #polys.Allocate()
    pdo.SetPoints(pts)
    pdo.SetPolys(polys)
    # Add other arrays to output appropriately
    pdo = copyArraysToPointData(pdi, pdo, fieldlat)

    return pdo
