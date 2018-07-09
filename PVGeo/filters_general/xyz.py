__all__ = [
    'PointsToPolyData',
    'latLonTableToCartesian',
    'RotateCoordinates',
    'ExtractPoints',
    'RotationTool',
]

import vtk
import numpy as np
from vtk.util import numpy_support as nps
from vtk.numpy_interface import dataset_adapter as dsa
# Import Helpers:
from ..base import PVGeoAlgorithmBase
from .. import _helpers



def PointsToPolyData(points):
    """@desc: Create `vtkPolyData` from a numpy array of XYZ points
    @returns:
    vtkPolyData : points with point-vertex cells"""
    if points.ndim != 2:
        points = points.reshape((-1, 3))

    npoints = points.shape[0]

    # Make VTK cells array
    cells = np.hstack((np.ones((npoints, 1)),
                       np.arange(npoints).reshape(-1, 1)))
    cells = np.ascontiguousarray(cells, dtype=np.int64)
    vtkcells = vtk.vtkCellArray()
    vtkcells.SetCells(npoints, nps.numpy_to_vtkIdTypeArray(cells, deep=True))

    # Convert points to vtk object
    pts = vtk.vtkPoints()
    for r in points:
        pts.InsertNextPoint(r[0],r[1],r[2])

    # Create polydata
    pdata = vtk.vtkPolyData()
    pdata.SetPoints(pts)
    pdata.SetVerts(vtkcells)
    return pdata


###############################################################################
#---- LatLon to Cartesian ----#
def latLonTableToCartesian(pdi, arrlat, arrlon, arralt, radius=6371.0, pdo=None):
    # TODO: This is very poorly done
    # TODO: filter works but assumes a spherical earth wich is VERY wrong
    # NOTE: Mismatches the vtkEarth Source however so we gonna keep it this way
    raise Exception('latLonTableToCartesian() not currently implemented.')
    if pdo is None:
        pdo = vtk.vtkPolyData()
    #pdo.DeepCopy(pdi)
    wpdo = dsa.WrapDataObject(pdo)
    import sys
    sys.path.append('/Users/bane/miniconda3/lib/python3.6/site-packages/')
    import utm

    # Get the input arrays
    (namelat, fieldlat) = arrlat[0], arrlat[1]
    (namelon, fieldlon) = arrlon[0], arrlon[1]
    (namealt, fieldalt) = arralt[0], arralt[1]
    wpdi = dsa.WrapDataObject(pdi)
    lat = _helpers.getArray(wpdi, fieldlat, namelat)
    lon = _helpers.getArray(wpdi, fieldlon, namelon)
    alt = _helpers.getArray(wpdi, fieldalt, namealt)
    if len(lat) != len(lon) or len(lat) != len(alt):
        raise Exception('Latitude, Longitude, and Altitude arrays must be same length.')

    coords = np.empty((len(lat),3))

    for i in range(len(lat)):
        (e, n, zN, zL) = utm.from_latlon(lat[i], lon[i])
        coords[i,0] = e
        coords[i,1] = n
    coords[:,2] = alt

    #insert = nps.numpy_to_vtk(num_array=coords, deep=True)
    #insert.SetName('Coordinates')
    # Add coords to ouptut table
    wpdo.Points = coords
    pts = vtk.vtkPoints()
    polys = vtk.vtkCellArray()
    k = 1
    # TODO: wee need point cells????
    for r in coords:
        pts.InsertNextPoint(r[0],r[1],r[2])
        polys.InsertNextCell(1)
        polys.InsertCellPoint(k)
        k = k + 1
    #polys.Allocate()
    pdo.SetPoints(pts)
    pdo.SetPolys(polys)
    # Add other arrays to output appropriately
    pdo = _helpers.copyArraysToPointData(pdi, pdo, fieldlat)

    return pdo

###############################################################################


class RotationTool(PVGeoAlgorithmBase):
    """@desc: a class that holds a set of methods/tools for performing and estimating coordinate rotations"""
    def __init__(self, decimals=6):
        PVGeoAlgorithmBase.__init__(self,
            nInputPorts=1, inputType='vtkPolyData',
            nOutputPorts=1, outputType='vtkPolyData')
        # Parameters
        self.RESOLUTION = np.pi / 3200.0
        self.DECIMALS = decimals

    @staticmethod
    def _GetRotationMatrix(theta):
        return np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)]])

    @staticmethod
    def RotateAround(pts, theta, origin):
        """@desc: rotate points around an origins given an anlge on the XY plane"""
        xarr, yarr = pts[:,0], pts[:,1]
        ox, oy = origin[0], origin[1]
        qx = ox + np.cos(theta) * (xarr - ox) - np.sin(theta) * (yarr - oy)
        qy = oy + np.sin(theta) * (xarr - ox) + np.cos(theta) * (yarr - oy)
        return np.vstack((qx, qy)).T

    @staticmethod
    def Rotate(pts, theta):
        """@desc: rotate points around (0,0,0) given an anlge on the XY plane"""
        rot = RotationTool._GetRotationMatrix(theta)
        return pts.dot(rot)

    @staticmethod
    def DistanceBetween(pts):
        """@desc: Gets the distance between two points"""
        return np.sqrt((pts[0,0] - pts[1,0])**2 + (pts[0,1] - pts[1,1])**2)

    @staticmethod
    def CosBetween(pts):
        xdiff = abs(pts[0,0] - pts[1,0])
        dist = RotationTool.DistanceBetween(pts)
        return np.arccos(xdiff/dist)

    @staticmethod
    def SinBetween(pts):
        ydiff = abs(pts[0,1] - pts[1,1])
        dist = RotationTool.DistanceBetween(pts)
        return np.arcsin(ydiff/dist)


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
        """internal use only: pts should only be a two neighboring points"""
        # Make the theta range up to 90 degrees to rotate points through
        #- angles = [0.0, 90.0)
        angles = np.arange(0.0, np.pi/2, self.RESOLUTION)
        nang = len(angles) # Number of rotations

        pts = np.vstack((pt1, pt2))

        for i in range(nang):
            # TODO: eliminate this for loop
            temp = self.Rotate(pts, angles[i])
            # Check the angles between the points
            c = self.CosBetween(temp)
            dist = self.DistanceBetween(temp)
            if abs(c - np.pi/2.0) < (1 * 10**-self.DECIMALS):
                return 0, angles[i], dist
            if abs(c - 0.0) < (1 * 10**-self.DECIMALS):
                return 1, angles[i], dist
        # Uh-oh... we reached here...
        #- lets try again with lower precision
        self.DECIMALS -= 1
        if self.DECIMALS < 0:
            self.DECIMALS = 0
            raise _helpers.PVGeoError('No angle found. Precision too low/high.')
        return self._ConvergeAngle(pt1, pt2)


    def _EstimateAngleAndSpacing(self, pts, sample=0.10):
        """internal use only"""
        from scipy.spatial import cKDTree # NOTE: Must have SciPy in ParaView
        # Creat the indexing range for searching the points:
        num = len(pts)
        rng = np.linspace(0, num-1, num=num, dtype=int)
        N = int(num*(1.0-sample))
        rng = rng[0::N]
        angles = np.zeros(len(rng))
        tree = cKDTree(pts)
        distances = [[],[]]

        # Get angles
        idx = 0
        for i in rng:
            # Find nearest point
            dist, ptsi = tree.query(pts[i], k=2)
            pt1 = pts[ptsi[0]]
            pt2 = pts[ptsi[1]]
            ax, angles[idx], dist = self._ConvergeAngle(pt1, pt2)
            distances[ax].append(dist)
            idx += 1

        angle = np.average(np.unique(angles))
        dx = np.unique(distances[0])
        dy = np.unique(distances[1])
        if len(dx) == 0:
            dx = dy
        elif len(dy) == 0:
            dy = dx
        # Now make sure only one angle was found
        # if len(angles) > 1:
        #     # This algorithm assumes the input data has uniform spacing throughout.
        #     # If multiple angles were found then that assumption must be False making the input data invalid.
        #     raise _helpers.PVGeoError('More than one angle recovered: Input data is invalid. Seek help with <info@pvgeo.org>.')
        return angle, dx[0], dy[0]


    def EstimateAndRotate(self, x, y, z):
        """"@desc: a method to estimat the rotation of a set of points and correct that rotation on the XY plane"""
        assert(len(x) == len(y) == len(z))
        idxs = np.argwhere(z == z[0])
        pts = np.hstack((x[idxs], y[idxs]))
        angle, dx, dy = self._EstimateAngleAndSpacing(pts)
        inv = self.Rotate(np.vstack((x, y)).T, angle)
        return inv[:,0], inv[:,1], z, dx, dy, angle



#---- Coordinate Rotations ----#

class RotateCoordinates(PVGeoAlgorithmBase):
    """@desc: Rotates XYZ coordinates in `vtkPolyData` around an origin at a given angle on the XY plane"""
    def __init__(self, angle=45.0, origin=[0.0, 0.0]):
        PVGeoAlgorithmBase.__init__(self,
            nInputPorts=1, inputType='vtkPolyData',
            nOutputPorts=1, outputType='vtkPolyData')
        # Parameters
        self.__angle = angle
        self.__origin = origin
        self.__useCorner = True

    def RequestData(self, request, inInfo, outInfo):
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
        """@desc: Sets the rotational angle in degrees"""
        theta = np.deg2rad(theta)
        if self.__angle != theta:
            self.__angle = theta
            self.Modified()

    def SetOrigin(self, xo, yo):
        """@desc: Sets the origin to perform the rotate around"""
        if self.__origin != [xo, yo]:
            self.__origin = [xo, yo]
            self.Modified()

    def SetUseCorner(self, flag):
        """@desc: a flag to use a corner of the input data set as the rotational origin"""
        if self.__useCorner != flag:
            self.__useCorner = flag
            self.Modified()



###############################################################################

class ExtractPoints(PVGeoAlgorithmBase):
    """@desc: Extracts XYZ coordinates and point/cell data from an input `vtkDataSet`"""
    def __init__(self):
        PVGeoAlgorithmBase.__init__(self,
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
        pdo.ShallowCopy(PointsToPolyData(points))
        _helpers.copyArraysToPointData(d, pdo, 0) # 0 is point data
        return 1
