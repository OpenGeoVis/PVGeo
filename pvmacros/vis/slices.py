def manySlicesAlongAxis(dataNm, rng, axis=0, exportpath='', ext='.csv'):
    """
    Description
    -----------


    Parameters
    ----------
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
    if axis not in (0,1,2):
        raise Exception('Axis choice must be 0, 1, or 2 (x, y, or z)')

    # Specify data set to be sliced
    data = pvs.FindSource(dataNm)

    # get active view
    renderView = pvs.GetActiveViewOrCreate('RenderView')

    def getNorm():
        norm = [0,0,0]
        norm[axis] = 1
        return norm

    def updateOrigin(og, i):
        og[axis] = rng[i]
        return og

    norm = getNorm()

    num = 0
    inputs = []
    for i in range(len(rng)):
        # create slice
        slc = pvs.Slice(Input=data)
        slc.SliceType = 'Plane'

        # set origin at points
        og = slc.SliceType.Origin
        og = updateOrigin(og, i)
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
        inputs.append(slc)
        #pvs.Show(slc, renderView)

    # Now append all slices into once source for easy management
    app = pvs.AppendDatasets(Input=inputs)
    pvs.RenameSource('%s-Slices' % dataNm, app)
    pvs.Show(app, renderView)
    pvs.RenderAllViews()
    pvs.ResetCamera()
    return app
