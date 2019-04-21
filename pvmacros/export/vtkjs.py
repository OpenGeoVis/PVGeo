"""The ``export`` module privides a few macros for exporting data scenes within
ParaView's rendering environment to the VTKjs format.

"""

__all__ = [
    'exportVTKjs',
    'getVTKjsURL',
]


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
exportVTKjs.__category__ = 'macro'

################################################################################


def convertDropboxURL(url):
    return url.replace("https://www.dropbox.com", "https://dl.dropbox.com")

def convertGitHubURL(url):
    url = url.replace("https://github.com", "https://rawgit.com")
    url = url.replace("raw/", "")
    return url

def generateViewerURL(dataURL):
    viewerURL = "http://viewer.pvgeo.org/"
    return viewerURL + '%s%s' % ("?fileURL=", dataURL)

def getVTKjsURL(*args):
    """After using ``exportVTKjs()`` to create a ``.vtkjs`` file from a ParaView
    data scene which is uploaded to an online file hosting service like Dropbix,
    use this method to get a shareable link to that scene on the
    `PVGeo VTKjs viewer`_.

    .. _PVGeo VTKjs viewer: http://viewer.pvgeo.org

    **Current file hosts supported:**
    - Dropbox
    - GitHub

    Args:
        host (str): the name of the file hosting service.
        inURL (str): the web URL to the ``.vtkjs`` file.

    Example:
        >>> import pvmacros as pvm
        >>> # A Dropbox hosted file:
        >>> pvm.export.getVTKjsURL('dropbox', 'https://www.dropbox.com/s/6m5ttdbv5bf4ngj/ripple.vtkjs\?dl\=0')

        >>> # A GitHib hosted file:
        >>> pvm.export.getVTKjsURL('github', 'https://github.com/OpenGeoVis/PVGeo/raw/docs/ripple.vtkjs')

    """
    if len(args) == 1:
        host = 'dropbox'
        inURL = args[0]
    elif len(args) == 2:
        host = args[0]
        inURL = args[1]
    else:
        raise RuntimeError('Arguments not understood.')
    if host.lower() == "dropbox":
        convertURL = convertDropboxURL(inURL)
    elif host.lower() == "github":
        convertURL = convertGitHubURL(inURL)
    else:
        print("--> Warning: Web host not specified or supported. URL is simply appended to standalone scene loader link.")
        convertURL = inURL
    #print("--> Your link: %s" % generateViewerURL(convertURL))
    return generateViewerURL(convertURL)

getVTKjsURL.__displayname__ = 'Get VTKjs URL'
getVTKjsURL.__category__ = 'macro'
