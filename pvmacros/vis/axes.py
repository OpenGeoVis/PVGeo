__all__ = [
    'customAxisTicks',
    'resetAxisTicks',
]

def customAxisTicks(rng, axis=0, uniform=False):
    """Use to set custom axis ticks in the render view

    Args:
        rng (list(float)): A list or tuple of floats for the axis ticks
        axis (int): The axis to set (X=0, Y=1, or Z=2)
        uniform (bool): An optional flag to use the given range on all axii
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

def resetAxisTicks(axis):
    """Use to reset the axis ticks in the render view for any given axii

    Args:
        axis (int or list(int)): The axis to set (X=0, Y=1, or Z=2)
    """
    from paraview.simple import GetActiveViewOrCreate, RenderAllViews
    rv = GetActiveViewOrCreate('RenderView')
    if not isinstance(axis, (list, tuple)):
        axis = [axis]
    for ax in axis:
        if ax is 0:
            rv.AxesGrid.XAxisLabels = []
            rv.AxesGrid.XAxisUseCustomLabels = 0
        if ax is 1:
            rv.AxesGrid.YAxisLabels = []
            rv.AxesGrid.YAxisUseCustomLabels = 0
        if ax is 2:
            rv.AxesGrid.ZAxisLabels = []
            rv.AxesGrid.ZAxisUseCustomLabels = 0
        RenderAllViews()
    return None

customAxisTicks.__displayname__ = 'Custom Axis Ticks'
customAxisTicks.__category__ = 'macro'
