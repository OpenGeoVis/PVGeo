from __future__ import print_function
from .manySlicesAlongPoints import *
from .clipThrough import *
from .camera import *
from .axes import *
from .slices import *

def deleteFilters(input=None):
    import paraview.simple as pvs
    """if input is not None:
        src = pvs.FindSource(dataNm)"""
    #TODO: be able to specify upstream source
    for f in pvs.GetSources().values():
        if f.GetProperty("Input") is not None:
            pvs.Delete(f)
    return None

def hideAll():
    """This hides all sources/filters on the pipeline from the current view"""
    import paraview.simple as pvs
    for f in pvs.GetSources().values():
        pvs.Hide(f)
    return None
