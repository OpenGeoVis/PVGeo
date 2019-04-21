__all__ = [
    'deleteDownstream',
]

__displayname__ = 'Pipeline'

def deleteDownstream(input_source=None):
    """Delete downstream filters for a given input source. If no input source
    provided, all filters on the pipeline will be deleted.

    Args:
        input_source (str): The name of the object on the pipeline to preserve.

    """
    import paraview.simple as pvs
    if input_source is None:
        # The below snippet deletes all Filters on the pipeline
        #- i.e. deletes anything that has an input
        #- preserves readers and sources
        for f in pvs.GetSources().values():
            if f.GetProperty("Input") is not None:
                pvs.Delete(f)
    else:
        # Be able to specify upstream source
        src = pvs.FindSource(input_source)
        #print('src: ', src)
        # Delete ALL things downstream of input_source
        for f in pvs.GetSources().values():
            #print('f: ', f)
            #print('f.Input: ', f.GetProperty("Input"))
            if f.GetPropertyValue("Input") is src:
                #print('Deleting: ', f)
                pvs.Delete(f)
    # Done
    return None

deleteDownstream.__displayname__ = 'Delete Downstream Filters'
deleteDownstream.__category__ = 'macro'
