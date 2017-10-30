"""
Use this script on the command line in a manner such as:

    python get_vtkjs_url.py <web file host> <file link>

For Example:

    python get_vtkjs_url.py github https://github.com/banesullivan/ParaViewGeophysics/raw/docs/ripple.vtkjs

    python get_vtkjs_url.py dropbox https://www.dropbox.com/s/6m5ttdbv5bf4ngj/ripple.vtkjs\?dl\=0

    Current file hosts supported:
        - Dropbox
        - GitHub
"""

import os
import sys

def convertDropboxURL(url):
    return url.replace("https://www.dropbox.com", "https://dl.dropbox.com")

def convertGitHubURL(url):
    url = url.replace("https://github.com", "https://rawgit.com")
    url = url.replace("raw/", "")
    return url

def generateViewerURL(dataURL):
    viewerURL = "https://rawgit.com/banesullivan/PVGPvtk.js/master/StandaloneSceneLoader.html"
    return viewerURL + '%s%s' % ("?fileURL=", dataURL)

def main():
    if len(sys.argv) != 3:
        print('Usage: %s <web file host> <file link>' % sys.argv[0])
        sys.exit(1)

    host = sys.argv[1]
    inURL = sys.argv[2]


    if host.lower() == "dropbox":
        convertURL = convertDropboxURL(inURL)
    elif host.lower() == "github":
        convertURL = convertGitHubURL(inURL)
    else:
        convertURL = inURL
    print("Your link: %s" % generateViewerURL(convertURL))
    exit(0)

if __name__ == '__main__':
    main()
