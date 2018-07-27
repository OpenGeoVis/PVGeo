__all__ = [
    'ManySlicesAlongPoints',
    'ManySlicesAlongAxis',
    'SliceThroughTime'
]

import vtk
from vtk.util import numpy_support as nps
import numpy as np
from vtk.numpy_interface import dataset_adapter as dsa
from datetime import datetime
# Import Helpers:
from ..base import FilterBase
from .. import _helpers
# NOTE: internal import - from scipy.spatial import cKDTree



class _SliceBase(FilterBase):
    """A helper class for making slicing fileters

    Note:
        * Make sure the input data source is slice-able.
        * The SciPy module is required for this filter.
    """
    __displayname__ = 'Base Slicing Filter'
    __type__ = 'filter'
    def __init__(self, numSlices=5,
            nInputPorts=1, inputType='vtkDataSet',
            nOutputPorts=1, outputType='vtkUnstructuredGrid'):
        FilterBase.__init__(self,
            nInputPorts=nInputPorts, inputType=inputType,
            nOutputPorts=nOutputPorts, outputType=outputType)
        # Parameters
        self.__numSlices = numSlices


    def _GeneratePlane(self, origin, normal):
        """Internal helper to build a ``vtkPlane`` for the cutter
        """
        # Get the slicing Plane:
        plane = vtk.vtkPlane() # Construct the plane object
        # Set the origin... needs to be inside of the grid
        plane.SetOrigin(origin[0], origin[1], origin[2])
        # set normal of that plane so we look at XZ section
        plane.SetNormal(normal)
        return plane

    def _Slice(self, pdi, pdo, plane):
        """Slice an input on a plane and produce the output
        """
        # create slice
        cutter = vtk.vtkCutter() # Construct the cutter object
        cutter.SetInputData(pdi) # Use the grid as the data we desire to cut
        cutter.SetCutFunction(plane) # the the cutter to use the plane we made
        cutter.Update() # Perfrom the Cut
        slc = cutter.GetOutput() # grab the output
        pdo.ShallowCopy(slc)

        return pdo

    def GetNumberOfSlices(self):
        return self.__numSlices

    def SetNumberOfSlices(self, num):
        if self.__numSlices != num:
            self.__numSlices = num
            self.Modified()


###############################################################################


class ManySlicesAlongPoints(_SliceBase):
    """Takes a series of points and a data source to be sliced. The points are used to construct a path through the data source and a slice is added at intervals of that path along the vector of that path at that point. This constructs many slices through the input dataset as an appended output ``vtkUnstructuredGrid``.

    Note:
        * Make sure the input data source is slice-able.
        * The SciPy module is required for this filter.
    """
    __displayname__ = 'Many Slices Along Points'
    __type__ = 'filter'
    def __init__(self, numSlices=5, nearestNbr=True):
        _SliceBase.__init__(self, numSlices=numSlices,
            nInputPorts=2, inputType='vtkDataSet',
            nOutputPorts=1, outputType='vtkUnstructuredGrid')
        self.__useNearestNbr = nearestNbr

    # CRITICAL for multiple input ports
    def FillInputPortInformation(self, port, info):
        """This simply makes sure the user selects the correct inputs
        """
        typ = 'vtkDataSet'
        if port == 0:
            typ = 'vtkPolyData' # Make sure points are poly data
        info.Set(self.INPUT_REQUIRED_DATA_TYPE(), typ)
        return 1

    def _ManySlicesAlongPoints(self, pdipts, pdidata, pdo):
        """Internal helper to perfrom the filter
        """
        # Get the Points over the NumPy interface
        wpdi = dsa.WrapDataObject(pdipts) # NumPy wrapped points
        points = np.array(wpdi.Points) # New NumPy array of points so we dont destroy input
        numPoints = pdipts.GetNumberOfPoints()
        if self.__useNearestNbr:
            from scipy.spatial import cKDTree # NOTE: Must have SciPy in ParaView
            tree = cKDTree(points)
            ptsi = tree.query(points[0], k=numPoints)[1]
        else:
            ptsi = [i for i in range(numPoints)]

        # iterate of points in order (skips last point):
        app = vtk.vtkAppendFilter()
        for i in range(0, numPoints - 1, numPoints/self.GetNumberOfSlices()):
            # get normal
            pts1 = points[ptsi[i]]
            pts2 = points[ptsi[i+1]]
            x1, y1, z1 = pts1[0], pts1[1], pts1[2]
            x2, y2, z2 = pts2[0], pts2[1], pts2[2]
            normal = [x2-x1,y2-y1,z2-z1]

            # create slice
            plane = self._GeneratePlane([x1,y1,z1], normal)
            temp = vtk.vtkPolyData()
            self._Slice(pdidata, temp, plane)
            app.AddInputData(temp)
        app.Update()
        pdo.ShallowCopy(app.GetOutput())
        return pdo



    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output"""
        # Get input/output of Proxy
        pdipts = self.GetInputData(inInfo, 0, 0) # Port 0: points
        pdidata = self.GetInputData(inInfo, 1, 0) # Port 1: sliceable data
        pdo = self.GetOutputData(outInfo, 0)
        # Perfrom task
        self._ManySlicesAlongPoints(pdipts, pdidata, pdo)
        return 1



    #### Getters / Setters ####

    def SetUseNearestNbr(self, flag):
        """Set a flag on whether to use SciPy's nearest neighbor approximation when generating the slicing path
        """
        if self.__useNearestNbr != flag:
            self.__useNearestNbr = flag
            self.Modified()

    def Apply(self, points, data):
        self.SetInputDataObject(0, points)
        self.SetInputDataObject(1, data)
        self.Update()
        return self.GetOutput()


###############################################################################



class ManySlicesAlongAxis(_SliceBase):
    """Slices a ``vtkDataSet`` along a given axis many times.
    This produces a specified number of slices at once each with a normal vector
    oriented along the axis of choice and spaced uniformly through the range of
    the dataset on the chosen axis.
    """
    __displayname__ = 'Many Slices Along Axis'
    __type__ = 'filter'
    def __init__(self, numSlices=5, axis=0, rng=None, outputType='vtkUnstructuredGrid'):
        _SliceBase.__init__(self, numSlices=numSlices,
            nInputPorts=1, inputType='vtkDataSet',
            nOutputPorts=1, outputType=outputType)
        # Parameters
        self.__axis = axis
        self.__rng = rng


    def _GetOrigin(self, pdi, idx):
        """Internal helper to get plane origin
        """
        og = list(self.GetInputCenter(pdi))
        og[self.__axis] = self.__rng[idx]
        return og


    def GetInputBounds(self, pdi):
        """Gets the bounds of the input data set on the set slicing axis.
        """
        bounds = pdi.GetBounds()
        return bounds[self.__axis*2], bounds[self.__axis*2+1]

    def GetInputCenter(self, pdi):
        """Gets the center of the input data set

        Return:
            tuple: the XYZ coordinates of the center of the data set.
        """
        bounds = pdi.GetBounds()
        x = bounds[1] - bounds[0]
        y = bounds[3] - bounds[2]
        z = bounds[5] - bounds[4]
        return (x, y, z)

    def GetNormal(self):
        """Get the normal of the slicing plane"""
        norm = [0,0,0]
        norm[self.__axis] = 1
        return norm

    def _SetAxialRange(self, pdi):
        """Internal helper to set the slicing range along the set axis
        """
        bounds = self.GetInputBounds(pdi)
        self.__rng = np.linspace(bounds[0]+0.001, bounds[1]-0.001, num=self.GetNumberOfSlices())

    def _UpdateNumOutputs(self, num):
        """for internal use only
        """
        return 1



    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output
        """
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        pdo = self.GetOutputData(outInfo, 0)
        self._SetAxialRange(pdi)
        normal = self.GetNormal()
        # Perfrom task
        app = vtk.vtkAppendFilter()
        for i in range(self.GetNumberOfSlices()):
            temp = vtk.vtkPolyData()
            origin = self._GetOrigin(pdi, i)
            plane = self._GeneratePlane(origin, normal)
            # Perfrom slice for that index
            self._Slice(pdi, temp, plane)
            app.AddInputData(temp)
        app.Update()
        pdo.ShallowCopy(app.GetOutput())

        return 1



    #### Getters / Setters ####


    def SetAxis(self, axis):
        """Set the axis on which to slice

        Args:
            axis (int): the axial index (0, 1, 2) = (x, y, z)
        """
        if axis not in (0,1,2):
            raise _helpers.PVGeoError('Axis choice must be 0, 1, or 2 (x, y, or z)')
        if self.__axis != axis:
            self.__axis = axis
            self.Modified()

    def GetRange(self):
        """Get the slicing range for the set axis
        """
        return self.__rng

    def GetAxis(self):
        """Get the set axis to slice upon as int index (0,1,2)
        """
        return self.__axis



###############################################################################


class SliceThroughTime(ManySlicesAlongAxis):
    """Takes a sliceable ``vtkDataSet`` and progresses a slice of it along a given axis. The macro requires that the clip already exist in the pipeline. This is especially useful if you have many clips linked together as all will move through the seen as a result of this macro.
    """
    __displayname__ = 'Slice Through Time'
    __type__ = 'filter'
    def __init__(self, numSlices=5, dt=1.0, axis=0, rng=None,):
        ManySlicesAlongAxis.__init__(self, numSlices=numSlices,
                axis=axis, rng=rng, outputType='vtkPolyData')
        # Parameters
        self.__dt = dt
        self.__timesteps = None


    def _UpdateTimeSteps(self):
        """For internal use only
        """
        self.__timesteps = _helpers.UpdateTimeSteps(self, self.GetNumberOfSlices(), self.__dt)



    #### Algorithm Methods ####

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output
        """
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        pdo = self.GetOutputData(outInfo, 0)
        self._SetAxialRange(pdi)
        i = _helpers.GetRequestedTime(self, outInfo)
        # Perfrom task
        normal = self.GetNormal()
        origin = self._GetOrigin(pdi, i)
        plane = self._GeneratePlane(origin, normal)
        self._Slice(pdi, pdo, plane)
        return 1

    def RequestInformation(self, request, inInfoVec, outInfoVec):
        """Used by pipeline to set the time information
        """
        # register time:
        self._UpdateTimeSteps()
        return 1

    #### Public Getters / Setters ####

    def SetNumberOfSlices(self, num):
        """Set the number of slices/timesteps to generate
        """
        ManySlicesAlongAxis.SetNumberOfSlices(self, num)
        self._UpdateTimeSteps()
        self.Modified()

    def SetTimeDelta(self, dt):
        """
        Set the time step interval in seconds
        """
        if self.__dt != dt:
            self.__dt = dt
            self._UpdateTimeSteps()
            self.Modified()

    def GetTimestepValues(self):
        """Use this in ParaView decorator to register timesteps
        """
        return self.__timesteps.tolist() if self.__timesteps is not None else None
