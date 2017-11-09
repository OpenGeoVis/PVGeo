def exportVTKjs(compress=False):
    import os
    path = os.path.dirname(os.path.abspath(__file__))
    execfile('%s/%s' % (path, 'export-scene-macro.py'), globals())
    return
