def exportVTKjs(FileName='', compress=False):
    """
    @desc:
    This function will execute a script to export the current scene from your rendering into the VTKjs shareable file format.

    @params:
    FileName : string : optional : Use to specify the basename of the output file. Extension will always be '.vtkjs'

    compress : boolean : optional : Declares a preference to compress the data arrays. Defaults to False.

    @returns:
    None: Prints the path to the saved '.vtkjs' file.

    @notes:
    - To view, open the file in the VTKjs standalone web viewer found [here](https://kitware.github.io/vtk-js/examples/StandaloneSceneLoader/StandaloneSceneLoader.html)
    - Use the `get_vtkjs_url.py` script in the PVGeo repository to get a shareable link for the exported file.

    """
    import os
    import sys
    path = os.path.dirname(os.path.abspath(__file__))
    # TODO: debug why compression sometimes fails
    sys.argv = ['%s/%s' % (path, '_export-scene-macro.py'), FileName, False]
    execfile('%s/%s' % (path, '_export-scene-macro.py'), globals())
    return
