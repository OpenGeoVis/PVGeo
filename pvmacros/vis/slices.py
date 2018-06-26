__all__ = ['manySlicesAlongPoints', 'manySlicesAlongAxis', 'clipThrough']

# import the simple module from the paraview and other needed libraries
import paraview.simple as pvs
import numpy as np
#from scipy.spatial import cKDTree
from vtk.util import numpy_support as nps
from vtk.numpy_interface import dataset_adapter as dsa
import time


def manySlicesAlongPoints(pointsNm, dataNm, numSlices=10, exportpath='', ext='.csv'):
    """
    @desc:
    This macro takes a series of points and a data source to be sliced. The points are used to construct a path through the data source and a slice is added at intervals of that path along the vector of that path at that point. This constructs `numSlices` slices through the dataset `dataNm`.

    @params:
    pointsNm : string : The string name of the points source to construct the path.
    dataNm : string : The string name of the data source to slice. Make sure this data source is slice-able.
    numSlices : int : optional : The number of slices along the path.
    exportpath : string : optional : The absolute file path of where to save each slice
    ext : string : optional : The file extension for saving out the slices. Default to '.csv'

    @notes:
    - Make sure the input data source is slice-able.
    - The SciPy module is required for this macro.

    """
    from scipy.spatial import cKDTree
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


def manySlicesAlongAxis(dataNm, rng, axis=0, exportpath='', ext='.csv'):
    """
    @desc:


    @params:
    dataNm : string : The string name of the data source to slice. Make sure this data source is slice-able.
    rng : list, tuple, or 1D np.array : A range of values along `axis` specified for the slice locations. Each element in `rng` will be a slice location along the `axis` chosen.
    exportpath : string : optional : The absolute file path of where to save each slice
    ext : string : optional : The file extension for saving out the slices. Default to '.csv'

    @notes:
    - Make sure the input data source is slice-able.
    - The SciPy module is required for this macro.

    """

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


def clipThrough(clip, ax, bounds, num=10, delay=1.0):
    """
    @desc:
    This macro takes a clip source and progresses its location through a set of bounds in the data scene. The macro requires that the clip already exist in the pipeline. This is especially useful if you have many clips linked together as all will move through the seen as a result of this macro.

    @params:
    clip : string : The string name of the clip source to be translated.
    ax : int : This is the axis on which to translate (0 for x, 1 for y, 2 for z). Think of this as the normal vector for the clip.
    bounds : list or tuple : These are the bounds to constrain the clip translation. 6 elements.
    num : int : optional : The number of discritizations in the clip translation.
    delay : float : optional : Time delay in seconds before conducting each clip translation.

    """

    if ax is not 0 and ax is not 1 and ax is not 2:
        raise Exception('Axis %d undefined.' % ax)

    if type(bounds) is not list and type(bounds) is not tuple:
        # TODO:
        raise Exception('getting bounds from data... not implemented')

    c = [(bounds[1]+bounds[0])/2, (bounds[3]+bounds[2])/2, (bounds[5]+bounds[4])/2]

    # disable automatic camera reset on 'Show'
    pvs._DisableFirstRenderCameraReset()
    # find source
    clp = pvs.FindSource(clip)
    # get active view
    renderView = pvs.GetActiveViewOrCreate('RenderView')

    for k in np.linspace(bounds[ax*2],bounds[ax*2+1],num=num):
        if ax == 0:
            o = [k, c[1], c[2]]
            n = [1, 0, 0]
        elif ax == 1:
            o = [c[0], k, c[2]]
            n = [0, 1, 0]
        elif ax == 2:
            o = [c[0], c[1], k]
            n = [0, 0, 1]
        clp.ClipType.Origin = o
        clp.ClipType.Normal = n
        renderView.Update()
        pvs.RenderAllViews()
        time.sleep(delay)
