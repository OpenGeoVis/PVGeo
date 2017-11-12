def manySlicesAlongPoints(pointsNm, dataNm, numSlices=10, exportpath='', ext='.csv'):
    """
    Description
    -----------
    This macro takes a series of points and a data source to be sliced. The points are used to construct a path through the data source and a slice is added at intervals of that path along the vector of that path at that point. This constructs `numSlices` slices through the dataset `dataNm`.

    Parameters
    ----------
    `pointsNm` : string

    - The string name of the points source to construct the path.

    `dataNm` : string

    - The string name of the data source to slice.
    - Make sure this data source is slice-able.

    `numSlices` : int, optional

    - The number of slices along the path.

    `exportpath` : string, optional

    - The absolute file path of where to save each slice

    `ext` : string, optional

    - The file extension for saving out the slices.
    - Default to '.csv'


    Notes
    -----
    - Make sure the input data source is slice-able.
    - The SciPy module is required for this macro.

    """
    # import the simple module from the paraview and other needed libraries
    import paraview.simple as pvs
    import numpy as np
    from scipy.spatial import cKDTree
    from vtk.util import numpy_support as nps
    from vtk.numpy_interface import dataset_adapter as dsa

    # exportpath: Where to save data. Absolute path:

    # Specify Points for the Line Source:
    line = pvs.servermanager.Fetch(pvs.FindSource(pointsNm))

    # Specify data set to be sliced
    data = pvs.FindSource(dataNm)

    # get active view
    renderView = pvs.GetActiveViewOrCreate('RenderView')

    # Get the Points over the NumPy interface
    wpdi = dsa.WrapDataObject(line) # NumPy wrapped points
    points = np.array(wpdi.Points) # New NumPy array of points so we dont destroy input
    numPoints = line.GetNumberOfPoints()
    tree = cKDTree(points)
    dist, ptsi = tree.query(points[0], k=numPoints)

    # iterate of points in order (skips last point):
    num = 0
    for i in range(0, numPoints - 1, numPoints/numSlices):
        # get normal
        pts1 = points[ptsi[i]]
        pts2 = points[ptsi[i+1]]
        x1, y1, z1 = pts1[0], pts1[1], pts1[2]
        x2, y2, z2 = pts2[0], pts2[1], pts2[2]
        norm = [x2-x1,y2-y1,z2-z1]

        # create slice
        slc = pvs.Slice(Input=data)
        slc.SliceType = 'Plane'

        # set origin at points
        slc.SliceType.Origin = [x1,y1,z1]
        # set normal as vector from current point to next point
        slc.SliceType.Normal = norm

        if exportpath != '':
            # save out slice with good metadata: TODO: change name
            # This will use a value from the point data to add to the name
            #num = wpdi.PointData['Advance LL (S-558)'][ptsi[i]]
            filename = path + 'Slice_%d%s' % (num, ext)
            print(filename)
            pvs.SaveData(filename, proxy=slc)

        num += 1
        pvs.Show(slc, renderView)

    pvs.RenderAllViews()
    pvs.ResetCamera()
