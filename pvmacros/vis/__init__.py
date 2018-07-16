from __future__ import print_function
from .objs import *
from .axes import *

__displayname__ = 'Visualization'

def hideAll():
    """This hides all sources/filters on the pipeline from the current view
    """
    import paraview.simple as pvs
    for f in pvs.GetSources().values():
        pvs.Hide(f)
    return None

hideAll.__displayname__ = 'Hide All'
hideAll.__type__ = 'macro'
