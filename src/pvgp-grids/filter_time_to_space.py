Name = 'ProjectShotRecordToSpace'
Label = 'Project Shot Record To Space'
Help = 'TODO: Should we keep this in the repo?'

NumberOfInputs = 2
InputDataType = 'vtkTable'
OutputDataType = 'vtkPolyData'
ExtraXml = ''

Properties = dict(
    ns=126,
    nt=1500,
    ds=1.0,
    dt=0.001,
)

def RequestData():
    from vtk.util import numpy_support as nps
    import numpy as np

    pdo = self.GetOutput()

    idata = 0
    icoord = 1

    if 'coord' in inputs[0].GetColumn(0).GetName():
        idata = 1
        icoord = 0

    # connect to input ports
    data_in = inputs[idata]
    coords_in = inputs[icoord]

    #print('Data: ', data_in.GetColumn(0).GetName())
    #print('Coords: ', coords_in.GetColumn(0).GetName())

    # Put arrays from inout to numpy arrays
    data = nps.vtk_to_numpy(data_in.GetColumn(0))
    coords = nps.vtk_to_numpy(coords_in.GetColumn(0))

    # Reshape arrays
    #data = np.reshape(data, (ns,nt,1)) # NOT NEEDED!!!!!!
    coords = np.reshape(coords, (ns,6))
    # Coordinate indices in the ns x 6 matrix:
    gx = 3
    gy = 2
    gz = 5
    sx = 1
    sy = 0
    sz = 4

    vtk_pts = vtk.vtkPoints()
    traces_as_points = np.empty((nt,4))
    # For each trace (essentially columns in both structures/arrays)
    for i in range(ns):
        # Grab source and receiver coords
        pts = coords[i]
        # source:
        s = [pts[sx], pts[sy], pts[sz]]
        # Receiver:
        g = [pts[gx], pts[gy], pts[gz]]
        # Direction Vector: Vector points from receiver to source
        vec = [s[0] - g[0], s[1] - g[1], s[2] - g[2]]
        # Total spatial distance:
        dist = math.sqrt(vec[0]**2 + vec[1]**2) # + vec[2]**2
        # Get unit vector for direction
        vec = [vec[0]/dist, vec[1]/dist, vec[2]] # /dist
        # Determine spacing factor from distance of 3D line and total data to fit on that 3D line
        #ds = math.floor(dist) / nt

        # Generate an array of coords for that whole line at that spacing and associate trace data
        line_coords = np.empty((nt,3))
        for j in range(nt):
            x = g[0] + (vec[0] * (nt-j) ) #* dt
            y = g[1] + (vec[1] * (nt-j) ) #* dt
            z = g[2]#s[2] + (vec[2] * j * ds)
            #line_coords = np.append(line_coords, [x,y,z])
            #line_coords[j] = [x,y,z]
            vtk_pts.InsertNextPoint(x,y,z)

    # Add each trace one after another (x,y,z,data) to 4D array
    #temp = np.append(line_coords, data[i], axis=1)
    #traces_as_points = np.append(traces_as_points, temp, axis=0)
    #pdo.SetPoints(vtk_pts)
    #insert = nps.numpy_to_vtk(num_array=data, deep=True, array_type=vtk.VTK_FLOAT)
    pdo.GetPointData().AddArray(data_in.GetColumn(0))
    #pdo.AddArray(data)

    # Add the points to the vtkPolyData object
    # Right now the points are not associated with a line -
    # it is just a set of unconnected points. We need to
    # create a 'cell' object that ties points together
    # to make a curve (in this case). This is done below.
    # A 'cell' is just an object that tells how points are
    # connected to make a 1D, 2D, or 3D object.
    pdo.SetPoints(vtk_pts)

    # Make a vtkPolyLine which holds the info necessary
    # to create a curve composed of line segments. This
    # really just hold constructor data that will be passed
    # to vtkPolyData to add a new line.
    aPolyLine = vtk.vtkPolyLine()

    #Indicate the number of points along the line
    numPts = ns*nt
    aPolyLine.GetPointIds().SetNumberOfIds(numPts)
    for i in range(0,numPts):
        # Add the points to the line. The first value indicates
        # the order of the point on the line. The second value
        # is a reference to a point in a vtkPoints object. Depends
        # on the order that Points were added to vtkPoints object.
        # Note that this will not be associated with actual points
        # until it is added to a vtkPolyData object which holds a
        # vtkPoints object.
        aPolyLine.GetPointIds().SetId(i, i)

    # Allocate the number of 'cells' that will be added. We are just
    # adding one vtkPolyLine 'cell' to the vtkPolyData object.
    pdo.Allocate(1, 1)

    # Add the poly line 'cell' to the vtkPolyData object.
    pdo.InsertNextCell(aPolyLine.GetCellType(), aPolyLine.GetPointIds())
