__all__ = [
    'deleteDownstream',
]

__displayname__ = 'Pipeline'

def deleteDownstream(input=None):
    """Delete downstream filters for a given input. If no input provided, all
    filters on the pipeline will be deleted.

    Args:
        input (str): The name of the object on the pipeline to preserve. 

    """
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

deleteDownstream.__displayname__ = 'Delete Downstream Filters'
deleteDownstream.__type__ = 'macro'
