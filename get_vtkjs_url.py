import os
import sys

def convertDropboxURL(url):
    return url.replace("https://www.dropbox.com", "https://dl.dropbox.com")

def generateViewerURL(dataURL):
    viewerURL = "https://rawgit.com/banesullivan/PVGPvtk.js/master/StandaloneSceneLoader.html"
    return viewerURL + '%s%s' % ("?fileURL=", dataURL)

def main():
    if len(sys.argv) != 3:
        print('Usage: %s <web file host> <file link>' % sys.argv[0])
        sys.exit(1)

    host = sys.argv[1]
    inlink = sys.argv[2]

    if host.lower() == "dropbox":
        convertURL = convertDropboxURL(inlink)
    else:
        convertURL = inlink
    print("Your link: %s" % generateViewerURL(convertURL))
    exit(0)

if __name__ == '__main__':
    main()
