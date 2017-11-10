def exportVTKjs(FileName=''):
    import os
    import sys
    path = os.path.dirname(os.path.abspath(__file__))
    if FileName != '':
        #sys.argv.append(FileName)
        sys.argv = ['%s/%s' % (path, 'export-scene-macro.py'), FileName]
        execfile('%s/%s' % (path, 'export-scene-macro.py'), globals())
    else:
        execfile('%s/%s' % (path, 'export-scene-macro.py'), globals())
    return
