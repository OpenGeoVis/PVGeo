import numpy as np
import os
import pickle
from paraview.simple import RenderAllViews, GetActiveCamera

class camLoc:
    def __init__(self,camera=GetActiveCamera()):
        """
        An object to store a single camera location/view
        Make a list/dict of these objects to save interestin views
        """
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

    # Variable access for internal use
    def _getOrientation(self):
        return self.orientation

    def _getPosition(self):
        return self.position

    def _getFocalPoint(self):
        return self.focus

    def _getViewUp(self):
        return self.viewup

    # Use new location
    def useLoc(self, camera=GetActiveCamera()):
        """
        Update the camera location
        """
        self.orientation = camera.GetOrientation()
        self.position = camera.GetPosition()
        self.focus = camera.GetFocalPoint()
        self.viewup = camera.GetViewUp()

    # Change the camera view
    def view(self, camera=GetActiveCamera()):
        """
        Use this method to update the camera to the saved location
        """
        orientation = self._getOrientation()
        position = self._getPosition()
        focus = self._getFocalPoint()
        viewup = self._getViewUp()

        # set the camera position and orientation
        camera.SetPosition(position)
        camera.SetViewUp(viewup)
        camera.SetFocalPoint(focus)
        RenderAllViews()
