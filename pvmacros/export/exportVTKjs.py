def exportVTKjs(FileName='', compress=False):
    """This function will execute a script to export the current scene from your rendering into the VTKjs shareable file format.

    Args:
        FileName (str) : Use to specify the basename of the output file. Extension will always be '.vtkjs'
        compress (bool) : Declares a preference to compress the data arrays. Defaults to False.

    Return:
        None: Prints the path to the saved '.vtkjs' file.

    Note:
        - To view, open the file in the VTKjs standalone web viewer `found here`_
        - Use the ``get_vtkjs_url.py`` script in the ``PVGeo`` repository to get a shareable link for the exported file.

    .. _found here: http://viewer.pvgeo.org

    """
    import os
    import sys
    path = os.path.dirname(os.path.abspath(__file__))
    # TODO: debug why compression sometimes fails
    sys.argv = ['%s/%s' % (path, '_export-scene-macro.py'), FileName, False]
    execfile('%s/%s' % (path, '_export-scene-macro.py'), globals())
    return

exportVTKjs.__displayname__ = 'Export VTKjs'
exportVTKjs.__type__ = 'macro'
