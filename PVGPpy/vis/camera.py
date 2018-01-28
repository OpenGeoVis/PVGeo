import numpy as np
import os
import pickle
from paraview.simple import RenderAllViews, GetActiveCamera

class camLoc:
    def __init__(self,camera=GetActiveCamera()):
        self.orientation = camera.GetOrientation()
        self.position = camera.GetPosition()
        self.focus = camera.GetFocalPoint()
        self.viewup = camera.GetViewUp()

    # Variable saving
    def save(self, filename='view.camloc', path=os.path.expanduser('~')):
        """
        Save a serialized variable out to a file
        Dafault saves to home directory
        """
        os.chdir(path)
        f = open(filename, 'wb')
        pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        f.close()

    @staticmethod
    def saveDict(lib, filename='views.camloc', path=os.path.expanduser('~')):
        """
        Save a serialized dictionaty of views out to a file
        Dafault saves to home directory
        """
        os.chdir(path)
        f = open(filename, 'wb')
        pickle.dump(lib, f, pickle.HIGHEST_PROTOCOL)
        f.close()

    @staticmethod
    def load(filename, path=os.path.expanduser('~')):
        """
        Load a file containg a serialized camLoc object(s)
        Dafault loads from home directory if relative path
        """
        os.chdir(path)
        with open(filename, 'rb') as f:
            return pickle.load(f)

    # Variable access
    def getOrientation(self):
        return self.orientation

    def getPosition(self):
        return self.position

    def getFocalPoint(self):
        return self.focus

    def getViewUp(self):
        return self.viewup

    # Use new location
    def useLoc(self, camera=GetActiveCamera()):
        self.orientation = camera.GetOrientation()
        self.position = camera.GetPosition()
        self.focus = camera.GetFocalPoint()
        self.viewup = camera.GetViewUp()

    # change the camera view
    def view(self, camera=GetActiveCamera()):
        orientation = self.getOrientation()
        position = self.getPosition()
        focus = self.getFocalPoint()
        viewup = self.getViewUp()

        # set the camera position and orientation
        camera.SetPosition(position)
        camera.SetViewUp(viewup)
        camera.SetFocalPoint(focus)
        RenderAllViews()
