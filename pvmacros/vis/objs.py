__all__ = ['camera']

import os
import pickle

from paraview.simple import GetActiveCamera, RenderAllViews, WriteImage


class camera:
    """An object to store a single camera location/view. You can make a list/dict of these objects to save interesting views for your project. This object saves just a few parameters about the camera so that it can easily be reconstructed.
    """
    __displayname__ = 'Camera'
    __category__ = 'macro'
    def __init__(self,cam=None):
        """
        @params:
        cam : vtkRenderingOpenGL2Python.vtkOpenGLCamera : optional : The camera you wish to update this object to. Totally optional
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
        """Updates the camera location to that which is in the currently activated view unless a vtkOpenGLCamera is specified.

        Args:
            cam (vtkRenderingOpenGL2Python.vtkOpenGLCamera) : The camera you wish to update this object to. Totally optional
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
        """Use this method to update the camera to the saved location

        Args:
            cam (vtkRenderingOpenGL2Python.vtkOpenGLCamera) : The camera you wish to view/update in the current render view
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
        """Save a screenshot of a single camera view

        Args:
            cam (vtkRenderingOpenGL2Python.vtkOpenGLCamera) : The camera you wish to view then save a screenshot
            path (str) : The directory you wish to save the screenshot. Defaults to user home directory
            basenm (str) : The file basename for the screenshot
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
        """Save a serialized dictionaty/list/whatever of views out to a file. Dafault saves to user's home directory

        Args:
            lib (dict or list) : some iterable object containg multiple `camera` objects
            filename (str) : The file basename for the serialized file
            path (str) : The directory you wish to save the views. Defaults to user home directory
        """
        ext = '.camera'
        os.chdir(path)
        f = open(filename + ext, 'wb')
        pickle.dump(lib, f, pickle.HIGHEST_PROTOCOL)
        f.close()

    @staticmethod
    def loadViews(filename='views.camera', path=os.path.expanduser('~')):
        """Load a file containg a serialized camera objects. Dafault loads from home directory if relative path

        Args:
            filename (str) : The file basename for the serialized file (defualt is default for output def)
            path (str): The directory from which you wish to load the views. Defaults to user home directory for relative paths.
        """
        os.chdir(path)
        with open(filename, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def screenShotViews(views, cam=None, path=os.path.expanduser('~'), basenm='view'):
        """Save screenshots of many views/cameras

        Args:
            view d(ict or list) : some iterable object containg multiple `camera` objects
            cam (vtkRenderingOpenGL2Python.vtkOpenGLCamera) : The camera you wish to view then save a screenshot
            path (str): The directory you wish to save the screenshot. Defaults to user home directory
            basenm (str): The file basename for the screenshot
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
