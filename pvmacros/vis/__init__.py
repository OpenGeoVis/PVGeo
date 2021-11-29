from __future__ import print_function

from .axes import *
from .objs import *

__displayname__ = 'Visualization'


def hideAll():
    """This hides all sources/filters on the pipeline from the current view"""
    import paraview.simple as pvs

    for f in pvs.GetSources().values():
        pvs.Hide(f)
    return None


hideAll.__displayname__ = 'Hide All'
hideAll.__category__ = 'macro'
