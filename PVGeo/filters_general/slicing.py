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
from ..base import PVGeoAlgorithmBase
from .. import _helpers
# NOTE: internal import - from scipy.spatial import cKDTree



class _SliceBase(PVGeoAlgorithmBase):
    """@desc: a helper class for making slicing fileters

    @notes:
    - Make sure the input data source is slice-able.
    - The SciPy module is required for this macro.
    """
    def __init__(self, numSlices=5,
            nInputPorts=1, inputType='vtkDataSet',
            nOutputPorts=1, outputType='vtkUnstructuredGrid'):
        PVGeoAlgorithmBase.__init__(self,
            nInputPorts=nInputPorts, inputType=inputType,
            nOutputPorts=nOutputPorts, outputType=outputType)
        # Parameters
        self.__numSlices = numSlices


    def _GeneratePlane(self, origin, normal):
        # Get the slicing Plane:
        plane = vtk.vtkPlane() # Construct the plane object
        # Set the origin... needs to be inside of the grid
        plane.SetOrigin(origin[0], origin[1], origin[2])
        # set normal of that plane so we look at XZ section
        plane.SetNormal(normal)
        return plane

    def _Slice(self, pdi, pdo, plane):
        """@desc: Slica an input on a plane and produce the output"""
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
    """@desc: Takes a series of points and a data source to be sliced. The points are used to construct a path through the data source and a slice is added at intervals of that path along the vector of that path at that point. This constructs many slices through the input dataset as an appended output `vtkUnstructuredGrid`.

    @notes:
    - Make sure the input data source is slice-able.
    - The SciPy module is required for this macro.
    """
    def __init__(self, numSlices=5):
        _SliceBase.__init__(self, numSlices=numSlices,
            nInputPorts=2, inputType='vtkDataSet',
            nOutputPorts=1, outputType='vtkUnstructuredGrid')
        self.__useNearestNbr = True

    # CRITICAL for multiple input ports
    def FillInputPortInformation(self, port, info):
        """@desc: This simply makes sure the user selects the correct inputs"""
        typ = 'vtkDataSet'
        if port == 0:
            typ = 'vtkPolyData' # Make sure points are poly data
        info.Set(self.INPUT_REQUIRED_DATA_TYPE(), typ)
        return 1

    def _ManySlicesAlongPoints(self, pdipts, pdidata, pdo):
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
        # Get input/output of Proxy
        pdipts = self.GetInputData(inInfo, 0, 0) # Port 0: points
        pdidata = self.GetInputData(inInfo, 1, 0) # Port 1: sliceable data
        pdo = self.GetOutputData(outInfo, 0)
        # Perfrom task
        self._ManySlicesAlongPoints(pdipts, pdidata, pdo)
        return 1



    #### Getters / Setters ####

    def SetUseNearestNbr(self, flag):
        if self.__useNearestNbr != flag:
            self.__useNearestNbr = flag
            self.Modified()


###############################################################################



class ManySlicesAlongAxis(_SliceBase):
    """@desc: Slices a `vtkDataSet` along a given axis many times"""
    def __init__(self, numSlices=5, outputType='vtkUnstructuredGrid'):
        _SliceBase.__init__(self, numSlices=numSlices,
            nInputPorts=1, inputType='vtkDataSet',
            nOutputPorts=1, outputType=outputType)
        # Parameters
        self.__axis = 0
        self.__rng = None


    def _GetOrigin(self, pdi, idx):
        og = self.GetInputCenter(pdi)
        og[self.__axis] = self.__rng[idx]
        return og


    def GetInputBounds(self, pdi):
        bounds = pdi.GetBounds()
        return bounds[self.__axis*2], bounds[self.__axis*2+1]

    def GetInputCenter(self, pdi):
        bounds = pdi.GetBounds()
        x = bounds[1] - bounds[0]
        y = bounds[3] - bounds[2]
        z = bounds[5] - bounds[4]
        return [x, y, z]

    def GetNormal(self):
        norm = [0,0,0]
        norm[self.__axis] = 1
        return norm

    def _SetAxialRange(self, pdi):
        bounds = self.GetInputBounds(pdi)
        self.__rng = np.linspace(bounds[0]+0.001, bounds[1]-0.001, num=self.GetNumberOfSlices())

    def _UpdateNumOutputs(self, num):
        """for internal use only"""
        return 1



    def RequestData(self, request, inInfo, outInfo):
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
        """@desc: set the axis on which to slice
        @params:
        axis : int : the axial index (0, 1, 2) = (x, y, z)"""
        if axis not in (0,1,2):
            raise Exception('Axis choice must be 0, 1, or 2 (x, y, or z)')
        if self.__axis != axis:
            self.__axis = axis
            self.Modified()

    def GetRange(self):
        return self.__rng

    def GetAxis(self):
        return self.__axis



###############################################################################


class SliceThroughTime(ManySlicesAlongAxis):
    """@desc: Takes a sliceable `vtkDataSet` and progresses a slice of it along a given axis. The macro requires that the clip already exist in the pipeline. This is especially useful if you have many clips linked together as all will move through the seen as a result of this macro.
    """
    def __init__(self, numSlices=5):
        ManySlicesAlongAxis.__init__(self, numSlices=numSlices, outputType='vtkPolyData')
        # Parameters
        self.__dt = 1.0
        self.__timesteps = None


    def _UpdateTimeSteps(self):
        """@desc: For internal use only"""
        self.__timesteps = _helpers.UpdateTimeSteps(self, self.GetNumberOfSlices(), self.__dt)



    #### Algorithm Methods ####

    def RequestData(self, request, inInfo, outInfo):
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
        # register time:
        self._UpdateTimeSteps()
        return 1

    #### Public Getters / Setters ####

    def SetNumberOfSlices(self, num):
        """@desc: Set the number of slices/timesteps to generate"""
        ManySlicesAlongAxis.SetNumberOfSlices(self, num)
        self._UpdateTimeSteps()
        self.Modified()

    def SetTimeDelta(self, dt):
        """@desc: Set the time step interval in seconds"""
        if self.__dt != dt:
            self.__dt = dt
            self._UpdateTimeSteps()
            self.Modified()

    def GetTimestepValues(self):
        """@desc: Use this in ParaView decorator to register timesteps"""
        return self.__timesteps.tolist() if self.__timesteps is not None else None
