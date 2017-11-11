def exportVTKjs(FileName='', compress=False):
    import os
    import sys
    path = os.path.dirname(os.path.abspath(__file__))
    sys.argv = ['%s/%s' % (path, 'export-scene-macro.py'), FileName, compress]
    execfile('%s/%s' % (path, 'export-scene-macro.py'), globals())
    return
