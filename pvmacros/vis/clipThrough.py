def clipThrough(clip, ax, bounds, num=10, delay=1.0):
    """
    Description
    -----------
    This macro takes a clip source and progresses its location through a set of bounds in the data scene. The macro requires that the clip already exist in the pipeline. This is especially useful if you have many clips linked together as all will move through the seen as a result of this macro.

    Parameters
    ----------
    `clip` : string
    - The string name of the clip source to be translated.

    `ax` : int
    - This is the axis on which to translate (0 for x, 1 for y, 2 for z).
    - Think of this as the normal vector for the clip.

    `bounds` : 6-element list or tuple
    - These are the bounds to constrain the clip translation.

    `num` : int, optional
    - The number of discritizations in the clip translation.

    `delay` : float, optional
    - Time delay in seconds before conducting each clip translation.

    """
    import paraview.simple as pvs
    import numpy as np
    import time

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
