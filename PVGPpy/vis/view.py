import numpy as np
import os
import pickle
from paraview.simple import RenderAllViews, GetActiveCamera, GetActiveView, WriteImage

class view:
    def __init__(self,camera=None):
        """
        An object to store a single camera location/view
        Make a list/dict of these objects to save interestin views
        """
        if camera is None:
            # This allows use to dynamicly select cameras
            camera = GetActiveCamera()
        self.orientation = camera.GetOrientation()
        self.position = camera.GetPosition()
        self.focus = camera.GetFocalPoint()
        self.viewup = camera.GetViewUp()

    @staticmethod
    def save(lib, filename='views', path=os.path.expanduser('~')):
        """
        Save a serialized dictionaty/list/whatever of views out to a file
        Dafault saves to home directory
        """
        ext = '.view'
        os.chdir(path)
        f = open(filename + ext, 'wb')
        pickle.dump(lib, f, pickle.HIGHEST_PROTOCOL)
        f.close()

    @staticmethod
    def load(filename, path=os.path.expanduser('~')):
        """
        Load a file containg a serialized view object(s)
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
    def useLoc(self, camera=None):
        """
        Update the camera location
        """
        if camera is None:
            # This allows use to dynamicly select cameras
            camera = GetActiveCamera()
        self.orientation = camera.GetOrientation()
        self.position = camera.GetPosition()
        self.focus = camera.GetFocalPoint()
        self.viewup = camera.GetViewUp()

    # Change the camera view
    def view(self, camera=None):
        """
        Use this method to update the camera to the saved location
        """
        if camera is None:
            # This allows use to dynamicly select cameras
            camera = GetActiveCamera()
        orientation = self._getOrientation()
        position = self._getPosition()
        focus = self._getFocalPoint()
        viewup = self._getViewUp()

        # set the camera position and orientation
        camera.SetPosition(position)
        camera.SetViewUp(viewup)
        camera.SetFocalPoint(focus)
        RenderAllViews()

    # Save Screenshot of single view
    def screenShot(self, camera=None, path=os.path.expanduser('~'), basenm='view'):
        """
        Save a screenshot of a single view
        """
        if camera is None:
            # This allows use to dynamicly select cameras
            camera = GetActiveCamera()
        os.chdir(path)
        view = GetActiveView()
        self.view(camera=camera)
        WriteImage("%s_%s.png" % (basenm, v))


    @staticmethod
    def screenShotViews(views, camera=None, path=os.path.expanduser('~'), basenm='view'):
        """
        Save screenShot of many views
        """
        if camera is None:
            # This allows use to dynamicly select cameras
            camera = GetActiveCamera()

        def _iter(obj):
            return obj if isinstance(obj, dict) else xrange(len(obj))

        os.chdir(path)
        view = GetActiveView()
        for v in _iter(views):
            views[v].view(camera=camera)
            WriteImage("%s_%s.png" % (basenm, v))
