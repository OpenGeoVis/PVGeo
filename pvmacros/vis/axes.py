__all__ = ['customAxisTicks']

def customAxisTicks(rng, axis=0, uniform=False):
    """Use to set custm axis ticks in the render view
    """
    from paraview.simple import GetActiveViewOrCreate, RenderAllViews
    # note that third parameter is the step size
    # get the active view
    rv = GetActiveViewOrCreate('RenderView')
    if axis is 0 or uniform:
        rv.AxesGrid.XAxisUseCustomLabels = 1
        rv.AxesGrid.XAxisLabels = rng
    if axis is 1 or uniform:
        rv.AxesGrid.YAxisUseCustomLabels = 1
        rv.AxesGrid.YAxisLabels = rng
    if axis is 2 or uniform:
        rv.AxesGrid.ZAxisUseCustomLabels = 1
        rv.AxesGrid.ZAxisLabels = rng
    RenderAllViews()
    return None

customAxisTicks.__displayname__ = 'Custom Axis Ticks'
customAxisTicks.__type__ = 'macro'
