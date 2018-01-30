import numpy as np
import os
import pickle
from paraview.simple import RenderAllViews, GetActiveCamera, WriteImage

class camera:
    def __init__(self,cam=None):
        """
        An object to store a single camera location/view
        Make a list/dict of these objects to save interestin views
        """
        if cam is None:
            # This allows use to dynamicly select cameras
            cam = GetActiveCamera()
        self.orientation = cam.GetOrientation()
        self.position = cam.GetPosition()
        self.focus = cam.GetFocalPoint()
        self.viewup = cam.GetViewUp()

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
    def update(self, cam=None):
        """
        Update the camera location
        """
        if cam is None:
            # This allows use to dynamicly select cameras
            cam = GetActiveCamera()
        self.orientation = cam.GetOrientation()
        self.position = cam.GetPosition()
        self.focus = cam.GetFocalPoint()
        self.viewup = cam.GetViewUp()

    # Change the camera view
    def view(self, cam=None):
        """
        Use this method to update the camera to the saved location
        """
        if cam is None:
            # This allows use to dynamicly select cameras
            cam = GetActiveCamera()
        orientation = self._getOrientation()
        position = self._getPosition()
        focus = self._getFocalPoint()
        viewup = self._getViewUp()

        # set the camera position and orientation
        cam.SetPosition(position)
        cam.SetViewUp(viewup)
        cam.SetFocalPoint(focus)
        RenderAllViews()

    # Save Screenshot of single view
    def screenShot(self, cam=None, path=os.path.expanduser('~'), basenm='view'):
        """
        Save a screenshot of a single camera view
        """
        if cam is None:
            # This allows use to dynamicly select cameras
            cam = GetActiveCamera()
        os.chdir(path)
        self.view(cam=cam)
        WriteImage("%s.png" % (basenm))


    # Static Methods for structures containt cameras

    @staticmethod
    def saveViews(lib, filename='views', path=os.path.expanduser('~')):
        """
        Save a serialized dictionaty/list/whatever of views out to a file
        Dafault saves to home directory
        """
        ext = '.camera'
        os.chdir(path)
        f = open(filename + ext, 'wb')
        pickle.dump(lib, f, pickle.HIGHEST_PROTOCOL)
        f.close()

    @staticmethod
    def loadViews(filename, path=os.path.expanduser('~')):
        """
        Load a file containg a serialized camera objects
        Dafault loads from home directory if relative path
        """
        os.chdir(path)
        with open(filename, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def screenShotViews(views, cam=None, path=os.path.expanduser('~'), basenm='view'):
        """
        Save screenShot of many views
        """
        if cam is None:
            # This allows use to dynamicly select cameras
            cam = GetActiveCamera()

        def _iter(obj):
            return obj if isinstance(obj, dict) else xrange(len(obj))

        os.chdir(path)
        for v in _iter(views):
            views[v].view(cam=cam)
            WriteImage("%s_%s.png" % (basenm, v))
