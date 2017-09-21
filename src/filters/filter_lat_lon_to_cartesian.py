Name = 'LatLonToCartesian'
Label = 'Lat Lon To Cartesian'
FilterCategory = 'CSM Geophysics Filters'
Help = 'Help for the Test Filter'

NumberOfInputs = 1
InputDataType = 'vtkTable'
OutputDataType = 'vtkTable'
ExtraXml = ''


Properties = dict(
    Radius=6371.0,
    lat_i=1,
    lon_i=0,
)

# TODO: filter works but assumes a spherical earth wich is very wrong

def RequestData():
    import numpy as np
    from vtk.util import numpy_support as nps
    pdi = self.GetInput()
    pdo = self.GetOutput()

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
    for r in data:
        x = Radius * cos(r[lat_i] * rad) * cos(r[lon_i] * rad)
        y = Radius * cos(r[lat_i] * rad) * sin(r[lon_i] * rad)
        z = Radius * sin(r[lat_i] * rad)
        coords[row_i] = [x,y,z]
        row_i = row_i + 1

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
