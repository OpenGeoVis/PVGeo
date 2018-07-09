from . import export
from . import vis

__author__ = 'Bane Sullivan'
__license__ = 'BSD-3-Clause'
__copyright__ = '2018, Bane Sullivan'
__version__ = '1.0.11'


def deleteDownstream(input=None):
    import paraview.simple as pvs
    if input is None:
        # The below snippet deletes all Filters on the pipeline
        #- i.e. deletes anything that has an input
        #- preserves readers and sources
        for f in pvs.GetSources().values():
            if f.GetProperty("Input") is not None:
                pvs.Delete(f)
    else:
        # Be able to specify upstream source
        src = pvs.FindSource(input)
        #print('src: ', src)
        # Delete ALL things downstream of input
        for f in pvs.GetSources().values():
            #print('f: ', f)
            #print('f.Input: ', f.GetProperty("Input"))
            if f.GetPropertyValue("Input") is src:
                #print('Deleting: ', f)
                pvs.Delete(f)
    # Done
    return None
