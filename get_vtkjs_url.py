"""
Use this script on the command line in a manner such as:

    python get_vtkjs_url.py <web file host> <file link>

For Example:

    python get_vtkjs_url.py dropbox https://www.dropbox.com/s/6m5ttdbv5bf4ngj/ripple.vtkjs\?dl\=0

    python get_vtkjs_url.py github https://github.com/OpenGeoVis/PVGeophysics/raw/docs/ripple.vtkjs

    Current file hosts supported:
        - Dropbox
        - GitHub
"""

import os
import sys

class stf:
    """
    String Formatting
    """
    G = '\033[92m'  # Green
    R = '\033[91m'  # Red
    B = '\033[1m'   # Bold
    U = '\033[4m'   # Underline
    END = '\033[0m' # Normal

def convertDropboxURL(url):
    return url.replace("https://www.dropbox.com", "https://dl.dropbox.com")

def convertGitHubURL(url):
    url = url.replace("https://github.com", "https://rawgit.com")
    url = url.replace("raw/", "")
    return url

def generateViewerURL(dataURL):
    viewerURL = "http://gpvis.org/"
    return viewerURL + '%s%s' % ("?fileURL=", dataURL)

def main():
    if len(sys.argv) != 3:
        print("%s--> Incorrect arguments for the script!" % stf.R)
        print('--> Usage: %s <web file host> <file link>%s' % (sys.argv[0], stf.END))
        sys.exit(1)

    host = sys.argv[1]
    inURL = sys.argv[2]


    if host.lower() == "dropbox":
        convertURL = convertDropboxURL(inURL)
    elif host.lower() == "github":
        convertURL = convertGitHubURL(inURL)
    else:
        print("%s%s--> Warning: Web host not specified or supported. URL is simply appended to standalone scene loader link.%s" % (stf.R, stf.B, stf.END))
        convertURL = inURL
    print("--> Your link: %s%s%s%s" % (stf.U, stf.G, generateViewerURL(convertURL), stf.END))
    exit(0)

if __name__ == '__main__':
    main()
