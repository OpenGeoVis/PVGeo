__all__ = [
    'LonLatToUTM',
    'RotatePoints',
    'ExtractPoints',
    'RotationTool',
    'ExtractCellCenters',
    'AppendCellCenters',
    'IterateOverPoints',
    'ConvertUnits',
]

import vtk
import numpy as np
import pandas as pd
import pyproj
from vtk.numpy_interface import dataset_adapter as dsa
# Import Helpers:
from ..base import FilterBase, FilterPreserveTypeBase
from .. import _helpers
from .. import interface



###############################################################################
#---- LonLat to Cartesian ----#

class LonLatToUTM(FilterBase):
    """Converts Points from Lon Lat to UTM
    """
    __displayname__ = 'Lat Lon To UTM'
    __category__ = 'filter'
    def __init__(self, **kwargs):
        FilterBase.__init__(self, inputType='vtkPolyData', outputType='vtkPolyData', **kwargs)
        self.__zone = kwargs.get('zone', 11) # User defined
        self.__ellps = kwargs.get('ellps', 'WGS84') # User defined

    @staticmethod
    def GetAvailableEllps(idx=None):
        """Returns the available ellps
        """
        ellps = pyproj.pj_ellps.keys()
        # Now migrate WGSXX to front so that 84 is always default
        wgs = ['WGS60','WGS66','WGS72', 'WGS84']
        for i, name in enumerate(wgs):
            oldindex = ellps.index(name)
            ellps.insert(0, ellps.pop(oldindex))
        if idx is not None: return ellps[idx]
        return ellps

    def __Convert2D(self, lon, lat, elev):
        """Converts 2D Lon Lat coords to 2D XY UTM points"""
        p = pyproj.Proj(proj='utm', zone=self.__zone, ellps=self.__ellps)
        utm_x, utm_y = p(lon, lat)
        return np.c_[utm_x, utm_y, elev]

    def RequestData(self, request, inInfo, outInfo):
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        pdo = self.GetOutputData(outInfo, 0)
        #### Perfrom task ####
        # Get the Points over the NumPy interface
        wpdi = dsa.WrapDataObject(pdi) # NumPy wrapped input
        if not hasattr(wpdi, 'Points'):
            raise _helpers.PVGeoError('Input data object does not have points to convert.')
        coords = np.array(wpdi.Points) # New NumPy array of poins so we dont destroy input
        # Now Conver the points
        points = self.__Convert2D(coords[:, 0], coords[:, 1], coords[:, 2])
        pdo.DeepCopy(interface.pointsToPolyData(points))
        _helpers.copyArraysToPointData(pdi, pdo, 0) # 0 is point data
        return 1

    def SetZone(self, zone):
        if zone < 1 or zone > 60:
            raise _helpers.PVGeoError('Zone (%d) is invalid.' % zone)
        if self.__zone != zone:
            self.__zone = int(zone)
            self.Modified()

    def SetEllps(self, ellps):
        if isinstance(ellps, int):
            ellps = self.GetAvailableEllps(idx=ellps)
        if not isinstance(ellps, str):
            raise _helpers.PVGeoError('Ellps must be a string.')
        if self.__ellps != ellps:
            self.__ellps = ellps
            self.Modified()


###############################################################################


class RotationTool(object):
    """A class that holds a set of methods/tools for performing and estimating coordinate rotations.
    """
    __displayname__ = 'Rotation Tool'
    __category__ = 'filter'
    def __init__(self, decimals=6):
        # Parameters
        self.RESOLUTION = np.pi / 3200.0
        self.DECIMALS = decimals

    @staticmethod
    def _GetRotationMatrix(theta):
        xx = np.cos(theta)
        xy = -np.sin(theta)
        yx = np.sin(theta)
        yy = np.cos(theta)
        if not isinstance(theta, np.ndarray):
            return np.array([[xx, xy],
                             [yx, yy]])
        # Otherwise populate arrat manually
        mat = np.zeros((len(theta), 2, 2))
        mat[:, 0, 0] = xx
        mat[:, 0, 1] = xy
        mat[:, 1, 0] = yx
        mat[:, 1, 1] = yy
        return mat

    @staticmethod
    def RotateAround(pts, theta, origin):
        """Rotate points around an origins given an anlge on the XY plane
        """
        xarr, yarr = pts[:,0], pts[:,1]
        ox, oy = origin[0], origin[1]
        qx = ox + np.cos(theta) * (xarr - ox) - np.sin(theta) * (yarr - oy)
        qy = oy + np.sin(theta) * (xarr - ox) + np.cos(theta) * (yarr - oy)
        return np.vstack((qx, qy)).T

    @staticmethod
    def Rotate(pts, theta):
        """Rotate points around (0,0,0) given an anlge on the XY plane
        """
        rot = RotationTool._GetRotationMatrix(theta)
        rotated = pts.dot(rot)
        if not isinstance(theta, np.ndarray):
            return rotated
        return np.swapaxes(rotated, 0, 1)

    @staticmethod
    def DistanceBetween(pts):
        """Gets the distance between two points
        """
        if pts.ndim < 3:
            return np.sqrt((pts[0,0] - pts[1,0])**2 + (pts[0,1] - pts[1,1])**2)
        return np.sqrt((pts[:, 0,0] - pts[:, 1,0])**2 + (pts[:, 0,1] - pts[:, 1,1])**2)

    @staticmethod
    def CosBetween(pts):
        """Gets the cosine between two points
        """
        if pts.ndim < 3:
            xdiff = abs(pts[0,0] - pts[1,0])
            dist = RotationTool.DistanceBetween(pts)
            return np.arccos(xdiff/dist)
        # Otherwise we have a set of points
        xdiff = abs(pts[:, 0,0] - pts[:, 1,0])
        dist = RotationTool.DistanceBetween(pts)
        return np.arccos(xdiff/dist)

    @staticmethod
    def SinBetween(pts):
        ydiff = abs(pts[0,1] - pts[1,1])
        dist = RotationTool.DistanceBetween(pts)
        return np.arcsin(ydiff/dist)

    @staticmethod
    def RotationMatrix(vector_orig, vector_fin):
        """Calculate the rotation matrix required to rotate from one vector to another.
        For the rotation of one vector to another, there are an infinit series of rotation matrices
        possible.  Due to axially symmetry, the rotation axis can be any vector lying in the symmetry
        plane between the two vectors.  Hence the axis-angle convention will be used to construct the
        matrix with the rotation axis defined as the cross product of the two vectors.  The rotation
        angle is the arccosine of the dot product of the two unit vectors.
        Given a unit vector parallel to the rotation axis, w = [x, y, z] and the rotation angle a,
        the rotation matrix R is::
                  |  1 + (1-cos(a))*(x*x-1)   -z*sin(a)+(1-cos(a))*x*y   y*sin(a)+(1-cos(a))*x*z |
            R  =  |  z*sin(a)+(1-cos(a))*x*y   1 + (1-cos(a))*(y*y-1)   -x*sin(a)+(1-cos(a))*y*z |
                  | -y*sin(a)+(1-cos(a))*x*z   x*sin(a)+(1-cos(a))*y*z   1 + (1-cos(a))*(z*z-1)  |

        Args:
            vector_orig (umpy array, len 3): The unrotated vector defined in the reference frame.
            vector_fin (numpy array, len 3): The rotated vector defined in the reference frame.

        Note:
            This code was adopted from `printipi`_ under the MIT license.

        .. _printipi: https://github.com/Wallacoloo/printipi/blob/master/util/rotation_matrix.py
        """
        from math import acos, atan2, cos, pi, sin
        from numpy import array, cross, dot, float64, hypot, zeros
        from numpy.linalg import norm

        R = np.zeros((3,3))

        # Convert the vectors to unit vectors.
        vector_orig = vector_orig / norm(vector_orig)
        vector_fin = vector_fin / norm(vector_fin)

        # The rotation axis (normalised).
        axis = cross(vector_orig, vector_fin)
        axis_len = norm(axis)
        if axis_len != 0.0:
            axis = axis / axis_len

        # Alias the axis coordinates.
        x = axis[0]
        y = axis[1]
        z = axis[2]

        # The rotation angle.
        angle = acos(dot(vector_orig, vector_fin))

        # Trig functions (only need to do this maths once!).
        ca = cos(angle)
        sa = sin(angle)

        # Calculate the rotation matrix elements.
        R[0,0] = 1.0 + (1.0 - ca)*(x**2 - 1.0)
        R[0,1] = -z*sa + (1.0 - ca)*x*y
        R[0,2] = y*sa + (1.0 - ca)*x*z
        R[1,0] = z*sa+(1.0 - ca)*x*y
        R[1,1] = 1.0 + (1.0 - ca)*(y**2 - 1.0)
        R[1,2] = -x*sa+(1.0 - ca)*y*z
        R[2,0] = -y*sa+(1.0 - ca)*x*z
        R[2,1] = x*sa+(1.0 - ca)*y*z
        R[2,2] = 1.0 + (1.0 - ca)*(z**2 - 1.0)
        return R


    # def _ConvergeAngle2(self, pt1, pt2):
    #     """internal use only: pts should only be a two neighboring points"""
    #     # Make the theta range up to 90 degrees to rotate points through
    #     #- angles = [0.0, 90.0)
    #     angles = np.arange(0.0, np.pi/2, self.RESOLUTION)
    #     pts = self.Rotate(np.vstack((pt1, pt2)), angles)
    #     # Get the angles between the points
    #     c = self.CosBetween(pts)
    #     dist = self.DistanceBetween(pts)
    #
    #     # Find angles that satisfy grid conditions
    #     xidx = np.argwhere(abs(c - np.pi/2.0) < (1 * 10**-self.DECIMALS))
    #     yidx = np.argwhere(abs(c - 0.0) < (1 * 10**-self.DECIMALS))
    #     if len(xidx) == 1 and len(yidx) == 0:
    #         return 0, np.pi/2-angles[xidx], dist[xidx]
    #         #return angles[xidx[0][0]]
    #     elif len(yidx) == 1 and len(xidx) == 0:
    #         return 1, np.pi/2-angles[yidx], dist[yidx]
    #     else:
    #         raise _helpers.PVGeoError('No angle found')


    def _ConvergeAngle(self, pt1, pt2):
        """Internal use only: pts should only be a two neighboring points.
        """
        # Make the theta range up to 90 degrees to rotate points through
        #- angles = [0.0, 90.0)
        angles = np.arange(0.0, np.pi/2, self.RESOLUTION)
        nang = len(angles) # Number of rotations

        # if pt1.ndim == pt2.ndim == 3:
        #     # uh-oh
        #     raise RuntimeError()
        pts = np.vstack((pt1, pt2))

        rotated = self.Rotate(pts, angles) # Points rotated for all angles
        cosbtw = self.CosBetween(rotated)
        distbtw = self.DistanceBetween(rotated)
        # Now find minimum

        # X axis
        xmin = np.argwhere(np.abs(cosbtw - np.pi/2.0) < (1 * 10**-self.DECIMALS)).flatten()
        ymin = np.argwhere(np.abs(cosbtw - 0.0) < (1 * 10**-self.DECIMALS)).flatten()

        # Protection to make sure we can converge
        if len(xmin) == 0 and len(ymin) == 0:
            # Uh-oh... lets decrease the precision
            #- lets try again with lower precision
            self.DECIMALS -= 1
            if self.DECIMALS < 0:
                self.DECIMALS = 0
                raise _helpers.PVGeoError('No angle found.')
            return self._ConvergeAngle(pt1, pt2)

        # Figure out of the two points share the x axis or y axis and return
        if len(xmin) > 0 and len(ymin) > 0:
            raise RuntimeError('Invalid solution')
        elif len(xmin) > 0:
            xidx = np.mean(xmin, dtype=int)
            return 0, angles[xidx], distbtw[xidx]
        elif len(ymin) > 0:
            yidx = np.mean(ymin, dtype=int)
            return 1, angles[yidx], distbtw[yidx]
        # No solution found.
        raise _helpers.PVGeoError('No angle found. Precision too low/high.')


    def _EstimateAngleAndSpacing(self, pts, sample=.5):
        """internal use only
        """
        from scipy.spatial import cKDTree # NOTE: Must have SciPy in ParaView
        # Creat the indexing range for searching the points:
        num = len(pts)
        rng = np.linspace(0, num-1, num=num, dtype=int)
        N = int(num*sample) + 1
        rng = np.random.choice(rng, N)
        angles = np.zeros(len(rng))
        tree = cKDTree(pts)
        distances = [[],[]]

        #######################################################################
        #######################################################################
        # Find nearest point
        distall, ptsiall = tree.query(pts, k=2)
        pt1all, pt2all = pts[ptsiall[:, 0]], pts[ptsiall[:, 1]]
        #######################################################################
        idx = 0
        for i in rng:
            # OPTIMIZE
            ax, angles[idx], dist = self._ConvergeAngle(pt1all[i], pt2all[i])
            distances[ax].append(dist)
            idx += 1
        #######################################################################
        #TODO??? angles, distances = self._ConvergeAngle(pt1all, pt2all)
        #######################################################################
        #######################################################################
        dx, dy = distances[0], distances[1]
        if len(dx) == 0:
            dx = dy
        elif len(dy) == 0:
            dy = dx
        TOLERANCE = np.min(np.append(dx, dy)) / 2.0
        angle = np.average(np.unique(angles))
        dx = np.unique(np.around(dx / TOLERANCE)) * TOLERANCE
        dy = np.unique(np.around(dy / TOLERANCE)) * TOLERANCE

        # Now round to decimals
        dx = np.around(dx, self.DECIMALS)
        dy = np.around(dx, self.DECIMALS)

        # print('Recovered: ', dx, dy)
        return angle, dx[0], dy[0]


    def EstimateAndRotate(self, x, y, z):
        """A method to estimate the rotation of a set of points and correct that rotation on the XY plane
        """
        assert(len(x) == len(y) == len(z))
        idxs = np.argwhere(z == z[0])
        pts = np.hstack((x[idxs], y[idxs]))
        angle, dx, dy = self._EstimateAngleAndSpacing(pts)
        inv = self.Rotate(np.vstack((x, y)).T, angle)
        return inv[:,0], inv[:,1], z, dx, dy, angle



#---- Coordinate Rotations ----#

class RotatePoints(FilterBase):
    """Rotates XYZ coordinates in `vtkPolyData` around an origin at a given angle on the XY plane.
    """
    __displayname__ = 'Rotate Points'
    __category__ = 'filter'
    def __init__(self, angle=45.0, origin=[0.0, 0.0], useCorner=True):
        FilterBase.__init__(self,
            nInputPorts=1, inputType='vtkPolyData',
            nOutputPorts=1, outputType='vtkPolyData')
        # Parameters
        self.__angle = angle
        self.__origin = origin
        self.__useCorner = useCorner

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output.
        """
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        pdo = self.GetOutputData(outInfo, 0)
        #### Perfrom task ####
        # Get the Points over the NumPy interface
        wpdi = dsa.WrapDataObject(pdi) # NumPy wrapped input
        points = np.array(wpdi.Points) # New NumPy array of poins so we dont destroy input
        origin = self.__origin
        if self.__useCorner:
            idx = np.argmin(points[:,0])
            origin = [points[idx,0], points[idx,1]]
        points[:,0:2] = RotationTool.RotateAround(points[:,0:2], self.__angle, origin)
        pdo.DeepCopy(pdi)
        pts = pdo.GetPoints()
        for i in range(len(points)):
            pts.SetPoint(i, points[i])
        return 1

    def SetRotationDegrees(self, theta):
        """Sets the rotational angle in degrees.
        """
        theta = np.deg2rad(theta)
        if self.__angle != theta:
            self.__angle = theta
            self.Modified()

    def SetOrigin(self, xo, yo):
        """Sets the origin to perform the rotate around.
        """
        if self.__origin != [xo, yo]:
            self.__origin = [xo, yo]
            self.Modified()

    def SetUseCorner(self, flag):
        """A flag to use a corner of the input data set as the rotational origin.
        """
        if self.__useCorner != flag:
            self.__useCorner = flag
            self.Modified()



###############################################################################

class ExtractPoints(FilterBase):
    """Extracts XYZ coordinates and point/cell data from an input ``vtkDataSet``
    """
    __displayname__ = 'Extract Points'
    __category__ = 'filter'
    def __init__(self):
        FilterBase.__init__(self,
            nInputPorts=1, inputType='vtkDataSet',
            nOutputPorts=1, outputType='vtkPolyData')

    def RequestData(self, request, inInfo, outInfo):
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        pdo = self.GetOutputData(outInfo, 0)
        #### Perfrom task ####
        # Get the Points over the NumPy interface
        wpdi = dsa.WrapDataObject(pdi) # NumPy wrapped input
        if not hasattr(wpdi, 'Points'):
            raise _helpers.PVGeoError('Input data object does not have XYZ points.')
        points = np.array(wpdi.Points) # New NumPy array of poins so we dont destroy input
        # Now transfer data
        f = vtk.vtkCellDataToPointData()
        f.SetInputData(pdi)
        f.Update()
        d = f.GetOutput()
        pdo.ShallowCopy(interface.pointsToPolyData(points))
        _helpers.copyArraysToPointData(d, pdo, 0) # 0 is point data
        return 1



class ExtractCellCenters(FilterBase):
    __displayname__ = 'Extract Cell Centers'
    __category__ = 'filter'
    def __init__(self, **kwargs):
        FilterBase.__init__(self, nInputPorts=1, inputType='vtkDataSet',
                    nOutputPorts=1, outputType='vtkPolyData', **kwargs)

    def RequestData(self, request, inInfoVec, outInfoVec):
        pdi = self.GetInputData(inInfoVec, 0, 0)
        pdo = self.GetOutputData(outInfoVec, 0)
        # Find cell centers
        filt = vtk.vtkCellCenters()
        filt.SetInputDataObject(pdi)
        filt.Update()

        centers = dsa.WrapDataObject(filt.GetOutput()).Points
        # Get CellData
        wpdi = dsa.WrapDataObject(pdi)
        celldata = wpdi.CellData
        keys = celldata.keys()

        # Make poly data of Cell centers:
        pdo.DeepCopy(interface.pointsToPolyData(centers))
        for i, name in enumerate(keys):
            pdo.GetPointData().AddArray(pdi.GetCellData().GetArray(name))
        return 1


class AppendCellCenters(FilterPreserveTypeBase):
    __displayname__ = 'Append Cell Centers'
    __category__ = 'filter'
    def __init__(self, **kwargs):
        FilterPreserveTypeBase.__init__(self, **kwargs)

    def RequestData(self, request, inInfoVec, outInfoVec):
        pdi = self.GetInputData(inInfoVec, 0, 0)
        pdo = self.GetOutputData(outInfoVec, 0)
        # Find cell centers
        filt = vtk.vtkCellCenters()
        filt.SetInputDataObject(pdi)
        filt.Update()

        # I use the dataset adapter/numpy interface because its easy
        centers = dsa.WrapDataObject(filt.GetOutput()).Points
        centers = interface.convertArray(centers)
        centers.SetName('Cell Centers')

        # Copy input data and add cell centers as tuple array
        pdo.DeepCopy(pdi)
        pdo.GetCellData().AddArray(centers)

        return 1




class IterateOverPoints(FilterBase):
    """Iterate over points in a time varying manner.
    """
    __displayname__ = 'Iterate Over Points'
    __category__ = 'filter'
    def __init__(self, dt=1.0):
        FilterBase.__init__(self, nInputPorts=1, inputType='vtkPolyData', nOutputPorts=1, outputType='vtkPolyData')
        # Parameters
        self.__dt = dt
        self.__timesteps = None
        self.__original = 2
        self.__tindex = None
        self.__n = 2
        self.__decimate = 100


    def _UpdateTimeSteps(self):
        """For internal use only
        """
        self.__timesteps = _helpers.updateTimeSteps(self, self.__n, self.__dt)


    def RequestData(self, request, inInfo, outInfo):
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        # Get number of points
        pdo = self.GetOutputData(outInfo, 0)
        #### Perfrom task ####
        # Get the Points over the NumPy interface
        wpdi = dsa.WrapDataObject(pdi) # NumPy wrapped input
        # Get requested time index
        i = _helpers.getRequestedTime(self, outInfo)
        # Now grab point at this timestep
        pt = pdi.GetPoints().GetPoint(self.__tindex[i])
        poly = interface.pointsToPolyData(np.array(pt))
        pdo.ShallowCopy(poly)
        return 1


    def RequestInformation(self, request, inInfo, outInfo):
        """Used by pipeline to set the time information
        """
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        # Get number of points
        self.__original = pdi.GetNumberOfPoints()
        self.SetDecimate(self.__decimate)
        # register time:
        self._UpdateTimeSteps()
        return 1

    #### Public Getters / Setters ####

    def SetDecimate(self, percent):
        """Set the percent (1 to 100) to decimate
        """
        if percent > 100 or percent < 1:
            return
        self.__decimate = percent
        self.__n = int(self.__original * (percent/100.0))
        self.__tindex = np.linspace(0, self.__original-1, self.__n, dtype=int)
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




class ConvertUnits(FilterPreserveTypeBase):
    """Convert points in an input data object to from meters to feet or vice versa.
    This simply uses a ``vtkTransformFilter`` and scales input data object with
    common conversions.
    """
    __displayname__ = 'Convert XYZ Units'
    __category__ = 'filter'
    def __init__(self, **kwargs):
        FilterPreserveTypeBase.__init__(self, **kwargs)
        self.__conversion = 'meter_to_feet'

    @staticmethod
    def LookupConversions(getkeys=False):
        """All Available conversions

        Return:
            dict: dictionary of conversion units
        """
        convs = dict(
            meter_to_feet=3.2808399,
            feet_to_meter=1/3.2808399,
        )
        if getkeys:
            return convs.keys()
        return convs

    def RequestData(self, request, inInfo, outInfo):
        """Execute on pipeline"""
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        # Get number of points
        pdo = self.GetOutputData(outInfo, 0)
        #### Perfrom task ####
        filt = vtk.vtkTransformFilter()
        trans = vtk.vtkTransform()
        trans.Scale(self.GetConversion(), self.GetConversion(), self.GetConversion())
        filt.SetTransform(trans)
        filt.SetInputDataObject(pdi)
        filt.Update()
        scaled = filt.GetOutputDataObject(0)
        pdo.DeepCopy(scaled)
        return 1



    def SetConversion(self, key):
        """Set the conversion via a lookup table"""
        convs = self.LookupConversions()
        if isinstance(key, str):
            if key.lower() not in convs.keys():
                raise _helpers.PVGeoError('Converion `%s` not available.' % key)
        elif isinstance(key, int):
            key = convs.keys()[key]
        if self.__conversion != key:
            self.__conversion = key
            self.Modified()
        return 1

    def GetConversion(self):
        """Get the conversion value"""
        convs = self.LookupConversions()
        return convs[self.__conversion]
