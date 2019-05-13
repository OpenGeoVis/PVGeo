__all__ = [
    'AddCellConnToPoints',
    'PointsToTube',
    'LonLatToUTM',
    'RotatePoints',
    'ExtractPoints',
    'RotationTool',
    'ExtractCellCenters',
    'AppendCellCenters',
    'IterateOverPoints',
    'ConvertUnits',
    'BuildSurfaceFromPoints',
]

__displayname__ = 'Point/Line Sets'

from datetime import datetime

import numpy as np
import pandas as pd
import vtk
from vtk.numpy_interface import dataset_adapter as dsa
import pyvista

# NOTE: internal import of pyproj in LonLatToUTM

from .. import _helpers, interface
from ..base import FilterBase, FilterPreserveTypeBase
# improt CreateTensorMesh for its cell string parsing
from ..model_build import CreateTensorMesh

###############################################################################
#---- Cell Connectivity ----#

class AddCellConnToPoints(FilterBase):
    """This filter will add linear cell connectivity between scattered points.
    You have the option to add ``VTK_Line`` or ``VTK_PolyLine`` connectivity.
    ``VTK_Line`` connectivity makes a straight line between the points in order
    (either in the order by index or using a nearest neighbor calculation).
    The ``VTK_PolyLine`` adds a poly line connectivity between all points as
    one spline (either in the order by index or using a nearest neighbor
    calculation). Type map is specified in `vtkCellType.h`.

    **Cell Connectivity Types:**

    - 4: Poly Line
    - 3: Line
    """
    __displayname__ = 'Add Cell Connectivity to Points'
    __category__ = 'filter'
    def __init__(self, **kwargs):
        FilterBase.__init__(self,
            nInputPorts=1, inputType='vtkPolyData',
            nOutputPorts=1, outputType='vtkPolyData')
        # Parameters
        self.__cell_type = kwargs.get('cell_type', vtk.VTK_POLY_LINE)
        self.__usenbr = kwargs.get('nearest_nbr', False)
        self.__close_loop = kwargs.get('close_loop', False)
        self.__keep_vertices = kwargs.get('keep_vertices', False)
        self.__unique = True


    def _connect_cells(self, pdi, pdo, log_time=False):
        """Internal helper to perfrom the connection
        """
        # NOTE: Type map is specified in vtkCellType.h
        cell_type = self.__cell_type

        if log_time:
            startTime = datetime.now()

        # Get the Points over the NumPy interface
        pdi = pyvista.wrap(pdi)
        points = np.copy(pdi.points) # New NumPy array of poins so we dont destroy input
        if self.__unique:
            # Remove repeated points
            indexes = np.unique(points, return_index=True, axis=0)[1]
            points = np.array(points[sorted(indexes)])

        def _find_min_path(points):
            try:
                # sklearn's KDTree is faster: use it if available
                from sklearn.neighbors import KDTree as Tree
            except ImportError:
                from scipy.spatial import cKDTree  as Tree
            _compute_dist = lambda pt0, pt1: np.linalg.norm(pt0-pt1)
            ind, min_dist = None, np.inf
            tree = Tree(points)
            for pt in points:
                cur_ind = tree.query([pt], k=len(points))[1].ravel()
                dist = 0.
                for i in range(len(cur_ind)-1):
                    dist += _compute_dist(points[cur_ind[i]], points[cur_ind[i+1]])
                if dist < min_dist:
                    ind = cur_ind
                    min_dist = dist
            return ind.ravel()

        if self.__usenbr:
            ind = _find_min_path(points)
        else:
            ind = np.arange(len(points), dtype=int)
        if self.__keep_vertices:
            poly = pyvista.PolyData(np.copy(points))
        else:
            poly = pyvista.PolyData()
            poly.points = np.copy(points)
        if cell_type == vtk.VTK_LINE:
            lines = np.c_[np.full(len(ind)-1, 2), ind[0:-1], ind[1:]]
            if self.__close_loop:
                app = np.append(lines, [[2, ind[-1], ind[0]],], axis=0)
                lines = app
            poly.lines = lines
        elif cell_type == vtk.VTK_POLY_LINE:
            cells = vtk.vtkCellArray()
            cell = vtk.vtkPolyLine()
            if self.__close_loop:
                cell.GetPointIds().SetNumberOfIds(len(ind) + 1)
            else:
                cell.GetPointIds().SetNumberOfIds(len(ind))
            for i in ind:
                cell.GetPointIds().SetId(i, ind[i])
            if self.__close_loop:
                cell.GetPointIds().SetId(i+1, ind[0])
            cells.InsertNextCell(cell)
            poly.SetLines(cells)
        else:
            raise _helpers.PVGeoError('Cell type ({}) not supported'.format(cell_type))
        for key, val in pdi.point_arrays.items():
            poly.point_arrays[key] = val
        pdo.DeepCopy(poly)
        return pdo

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output data object
        """
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        pdo = self.GetOutputData(outInfo, 0)
        # Perfrom task
        self._connect_cells(pdi, pdo)
        return 1


    #### Seters and Geters ####


    def set_cell_type(self, cell_type):
        """Set the cell typ by the integer id as specified in `vtkCellType.h`
        """
        if cell_type != self.__cell_type:
            self.__cell_type = cell_type
            self.Modified()

    def set_use_nearest_nbr(self, flag):
        """Set a flag on whether to a KDTree nearest neighbor
        algorithm to sort the points to before adding linear connectivity.
        """
        if flag != self.__usenbr:
            self.__usenbr = flag
            self.Modified()

    def set_use_unique_points(self, flag):
        """Set a flag on whether to only use unique points"""
        if flag != self.__unique:
            self.__unique = flag
            self.Modified()


###############################################################################


class PointsToTube(AddCellConnToPoints):
    """Takes points from a vtkPolyData object and constructs a line of those
    points then builds a polygonal tube around that line with some specified
    radius and number of sides.
    """
    __displayname__ = 'Points to Tube'
    __category__ = 'filter'
    def __init__(self, num_sides=20, radius=10.0, capping=False, **kwargs):
        AddCellConnToPoints.__init__(self, **kwargs)
        # Additional Parameters
        # NOTE: CellType should remain vtk.VTK_POLY_LINE (4) connection
        self.__numSides = num_sides
        self.__radius = radius
        self.__capping = capping


    def _connect_cells(self, pdi, pdo, log_time=False):
        """This uses the parent's ``_connect_cells()`` to build a tub around
        """
        AddCellConnToPoints._connect_cells(self, pdi, pdo, log_time=log_time)
        tube = vtk.vtkTubeFilter()
        tube.SetInputData(pdo)
        # User Defined Parameters
        tube.SetCapping(self.__capping)
        tube.SetRadius(self.__radius)
        tube.SetNumberOfSides(self.__numSides)
        # apply the filter
        tube.Update()
        pdo.ShallowCopy(tube.GetOutput())
        return pdo


    #### Seters and Geters ####

    def set_radius(self, radius):
        """Set the radius of the tube
        """
        if self.__radius != radius:
            self.__radius = radius
            self.Modified()

    def set_number_of_sides(self, num):
        """Set the number of sides (resolution) for the tube
        """
        if self.__numSides != num:
            self.__numSides = num
            self.Modified()

    def set_capping(self, flag):
        """Set a boolean flag on whether or not to cap the ends of the tube
        """
        if self.__capping != flag:
            self.__capping = flag
            self.Modified()




###############################################################################
#---- LonLat to Cartesian ----#

class LonLatToUTM(FilterPreserveTypeBase):
    """Converts Points from Lon Lat to UTM
    """
    __displayname__ = 'Lat Lon To UTM'
    __category__ = 'filter'
    def __init__(self, **kwargs):
        FilterPreserveTypeBase.__init__(self, inputType='vtkDataSet', **kwargs)
        self.__zone = 11,
        self.__ellps = 'WGS84'
        self.set_zone(kwargs.get('zone', 11)) # User defined
        self.set_ellps(kwargs.get('ellps', 'WGS84')) # User defined

    @staticmethod
    def get_available_ellps(idx=None):
        """Returns the available ellps
        """
        import pyproj
        ellps = pyproj.pj_ellps.keys()
        # Now migrate WGSXX to front so that 84 is always default
        wgs = ['WGS60','WGS66','WGS72', 'WGS84']
        for i, name in enumerate(wgs):
            oldindex = ellps.index(name)
            ellps.insert(0, ellps.pop(oldindex))
        if idx is not None: return ellps[idx]
        return ellps

    def __convert_2d(self, lon, lat, elev):
        """Converts 2D Lon Lat coords to 2D XY UTM points"""
        import pyproj
        p = pyproj.Proj(proj='utm', zone=self.__zone, ellps=self.__ellps)
        utm_x, utm_y = p(lon, lat)
        return np.c_[utm_x, utm_y, elev]

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output"""
        # Get input/output of Proxy
        pdi = pyvista.wrap(self.GetInputData(inInfo, 0, 0))
        pdo = self.GetOutputData(outInfo, 0)
        #### Perfrom task ####
        if not hasattr(pdi, 'points'):
            raise _helpers.PVGeoError('Input data object does not have points to convert.')
        coords = pdi.points.copy() # New NumPy array of poins so we dont destroy input
        # Now Conver the points
        points = self.__convert_2d(coords[:, 0], coords[:, 1], coords[:, 2])
        output = pdi.copy()
        output.points = points
        pdo.DeepCopy(output)
        return 1

    def set_zone(self, zone):
        """Set the UTM zone number"""
        if zone < 1 or zone > 60:
            raise _helpers.PVGeoError('Zone (%d) is invalid.' % zone)
        if self.__zone != zone:
            self.__zone = int(zone)
            self.Modified()

    def set_ellps(self, ellps):
        """Set the ellipsoid type"""
        if isinstance(ellps, int):
            ellps = self.get_available_ellps(idx=ellps)
        if not isinstance(ellps, str):
            raise _helpers.PVGeoError('Ellps must be a string.')
        if self.__ellps != ellps:
            self.__ellps = ellps
            self.Modified()


###############################################################################


class RotationTool(object):
    """A class that holds a set of methods/tools for performing and estimating
    coordinate rotations.
    """
    __displayname__ = 'Rotation Tool'
    __category__ = 'filter'
    def __init__(self, decimals=6):
        # Parameters
        self.RESOLUTION = np.pi / 3200.0
        self.DECIMALS = decimals

    @staticmethod
    def _get_rotation_matrix(theta):
        """Internal helper to generate a rotation matrix given a rotation angle"""
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
    def rotate_around(pts, theta, origin):
        """Rotate points around an origins given an anlge on the XY plane
        """
        xarr, yarr = pts[:,0], pts[:,1]
        ox, oy = origin[0], origin[1]
        qx = ox + np.cos(theta) * (xarr - ox) - np.sin(theta) * (yarr - oy)
        qy = oy + np.sin(theta) * (xarr - ox) + np.cos(theta) * (yarr - oy)
        return np.vstack((qx, qy)).T

    @staticmethod
    def rotate(pts, theta):
        """Rotate points around (0,0,0) given an anlge on the XY plane
        """
        rot = RotationTool._get_rotation_matrix(theta)
        rotated = pts.dot(rot)
        if not isinstance(theta, np.ndarray):
            return rotated
        return np.swapaxes(rotated, 0, 1)

    @staticmethod
    def distance_between(pts):
        """Gets the distance between two points
        """
        if pts.ndim < 3:
            return np.sqrt((pts[0,0] - pts[1,0])**2 + (pts[0,1] - pts[1,1])**2)
        return np.sqrt((pts[:, 0,0] - pts[:, 1,0])**2 + (pts[:, 0,1] - pts[:, 1,1])**2)

    @staticmethod
    def cos_between(pts):
        """Gets the cosine between two points
        """
        if pts.ndim < 3:
            xdiff = abs(pts[0,0] - pts[1,0])
            dist = RotationTool.distance_between(pts)
            return np.arccos(xdiff/dist)
        # Otherwise we have a set of points
        xdiff = abs(pts[:, 0,0] - pts[:, 1,0])
        dist = RotationTool.distance_between(pts)
        return np.arccos(xdiff/dist)

    @staticmethod
    def sin_between(pts):
        """Calculate the sin angle between two points"""
        ydiff = abs(pts[0,1] - pts[1,1])
        dist = RotationTool.distance_between(pts)
        return np.arcsin(ydiff/dist)

    @staticmethod
    def rotation_matrix(vector_orig, vector_fin):
        """Calculate the rotation matrix required to rotate from one vector to another.
        For the rotation of one vector to another, there are an infinit series of rotation matrices
        possible.  Due to axially symmetry, the rotation axis can be any vector lying in the symmetry
        plane between the two vectors.  Hence the axis-angle convention will be used to construct the
        matrix with the rotation axis defined as the cross product of the two vectors.  The rotation
        angle is the arccosine of the dot product of the two unit vectors.
        Given a unit vector parallel to the rotation axis, w = [x, y, z] and the rotation angle a,
        the rotation matrix R is::
                |  1 + (1-cos(a))*(x*x-1)   -z*sin(a)+(1-cos(a))*x*y   y*sin(a)+(1-cos(a))*x*z |
            R = |  z*sin(a)+(1-cos(a))*x*y   1 + (1-cos(a))*(y*y-1)   -x*sin(a)+(1-cos(a))*y*z |
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


    # def _converge_angle2(self, pt1, pt2):
    #     """internal use only: pts should only be a two neighboring points"""
    #     # Make the theta range up to 90 degrees to rotate points through
    #     #- angles = [0.0, 90.0)
    #     angles = np.arange(0.0, np.pi/2, self.RESOLUTION)
    #     pts = self.rotate(np.vstack((pt1, pt2)), angles)
    #     # Get the angles between the points
    #     c = self.cos_between(pts)
    #     dist = self.distance_between(pts)
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


    def _converge_angle(self, pt1, pt2):
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

        rotated = self.rotate(pts, angles) # Points rotated for all angles
        cosbtw = self.cos_between(rotated)
        distbtw = self.distance_between(rotated)
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
            return self._converge_angle(pt1, pt2)

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


    def _estimate_angle_and_spacing(self, pts, sample=0.5):
        """internal use only
        """
        try:
            # sklearn's KDTree is faster: use it if available
            from sklearn.neighbors import KDTree as Tree
        except ImportError:
            from scipy.spatial import cKDTree  as Tree
        # Creat the indexing range for searching the points:
        num = len(pts)
        rng = np.linspace(0, num-1, num=num, dtype=int)
        N = int(num*sample) + 1
        rng = np.random.choice(rng, N)
        angles = np.zeros(len(rng))
        tree = Tree(pts)
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
            ax, angles[idx], dist = self._converge_angle(pt1all[i], pt2all[i])
            distances[ax].append(dist)
            idx += 1
        #######################################################################
        #TODO??? angles, distances = self._converge_angle(pt1all, pt2all)
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


    def estimate_and_rotate(self, x, y, z):
        """A method to estimate the rotation of a set of points and correct
        that rotation on the XY plane
        """
        if not (len(x) == len(y) == len(z)):
            raise AssertionError('Must have same number of coordinates for all components.')
        idxs = np.argwhere(z == z[0])
        pts = np.hstack((x[idxs], y[idxs]))
        angle, dx, dy = self._estimate_angle_and_spacing(pts)
        inv = self.rotate(np.vstack((x, y)).T, angle)
        return inv[:,0], inv[:,1], z, dx, dy, angle



#---- Coordinate Rotations ----#

class RotatePoints(FilterBase):
    """Rotates XYZ coordinates in `vtkPolyData` around an origin at a given
    angle on the XY plane.
    """
    __displayname__ = 'Rotate Points'
    __category__ = 'filter'
    def __init__(self, angle=45.0, origin=None, use_corner=True):
        FilterBase.__init__(self,
            nInputPorts=1, inputType='vtkPolyData',
            nOutputPorts=1, outputType='vtkPolyData')
        # Parameters
        self.__angle = angle
        if origin is None:
            origin = [0.0, 0.0]
        self.__origin = origin
        self.__use_corner = use_corner

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
        if self.__use_corner:
            idx = np.argmin(points[:,0])
            origin = [points[idx,0], points[idx,1]]
        points[:,0:2] = RotationTool.rotate_around(points[:,0:2], self.__angle, origin)
        pdo.DeepCopy(pdi)
        pts = pdo.GetPoints()
        for i, pt in enumerate(points):
            pts.SetPoint(i, pt)
        return 1

    def set_rotation_degrees(self, theta):
        """Sets the rotational angle in degrees.
        """
        theta = np.deg2rad(theta)
        if self.__angle != theta:
            self.__angle = theta
            self.Modified()

    def set_origin(self, xo, yo):
        """Sets the origin to perform the rotate around.
        """
        if self.__origin != [xo, yo]:
            self.__origin = [xo, yo]
            self.Modified()

    def set_use_corner(self, flag):
        """A flag to use a corner of the input data set as the rotational
        origin.
        """
        if self.__use_corner != flag:
            self.__use_corner = flag
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
        """Used by pipeline to generate output"""
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
        pdo.ShallowCopy(interface.points_to_poly_data(points))
        _helpers.copy_arrays_to_point_data(d, pdo, 0) # 0 is point data
        return 1



class ExtractCellCenters(FilterBase):
    __displayname__ = 'Extract Cell Centers'
    __category__ = 'filter'
    def __init__(self, **kwargs):
        FilterBase.__init__(self, nInputPorts=1, inputType='vtkDataSet',
                    nOutputPorts=1, outputType='vtkPolyData', **kwargs)

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output"""
        pdi = self.GetInputData(inInfo, 0, 0)
        pdo = self.GetOutputData(outInfo, 0)
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
        pdo.DeepCopy(interface.points_to_poly_data(centers))
        for i, name in enumerate(keys):
            pdo.GetPointData().AddArray(pdi.GetCellData().GetArray(name))
        return 1


class AppendCellCenters(FilterPreserveTypeBase):
    __displayname__ = 'Append Cell Centers'
    __category__ = 'filter'
    def __init__(self, **kwargs):
        FilterPreserveTypeBase.__init__(self, **kwargs)

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output"""
        pdi = self.GetInputData(inInfo, 0, 0)
        pdo = self.GetOutputData(outInfo, 0)
        # Find cell centers
        filt = vtk.vtkCellCenters()
        filt.SetInputDataObject(pdi)
        filt.Update()

        # I use the dataset adapter/numpy interface because its easy
        centers = dsa.WrapDataObject(filt.GetOutput()).Points
        centers = interface.convert_array(centers)
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
        FilterBase.__init__(self, nInputPorts=1, inputType='vtkPolyData',
                            nOutputPorts=1, outputType='vtkPolyData')
        # Parameters
        self.__dt = dt
        self.__timesteps = None
        self.__original = 2
        self.__tindex = None
        self.__n = 2
        self.__decimate = 100
        # The point/normal that gets updated on every iteration
        self.__point = (0.0, 0.0, 0.0)
        self.__normal = (1.0, 0.0, 0.0)


    def _update_time_steps(self):
        """For internal use only
        """
        self.__timesteps = _helpers.update_time_steps(self, self.__n, self.__dt)


    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output"""
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        # Get number of points
        pdo = self.GetOutputData(outInfo, 0)
        #### Perfrom task ####
        # Get the Points over the NumPy interface
        wpdi = dsa.WrapDataObject(pdi) # NumPy wrapped input
        # Get requested time index
        i = _helpers.get_requested_time(self, outInfo)
        # Now grab point at this timestep
        pt = pdi.GetPoints().GetPoint(self.__tindex[i])
        # Calculate normal
        pts1 = self.__point
        pts2 = pt
        x1, y1, z1 = pts1[0], pts1[1], pts1[2]
        x2, y2, z2 = pts2[0], pts2[1], pts2[2]
        normal = [x2-x1, y2-y1, z2-z1]
        self.__point = pt
        self.__normal = normal
        poly = interface.points_to_poly_data(np.array(pt))
        pdo.ShallowCopy(poly)
        return 1


    def RequestInformation(self, request, inInfo, outInfo):
        """Used by pipeline to set the time information
        """
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        # Get number of points
        self.__original = pdi.GetNumberOfPoints()
        self.set_decimate(self.__decimate)
        # register time:
        self._update_time_steps()
        return 1

    #### Public Getters / Setters ####

    def set_decimate(self, percent):
        """Set the percent (1 to 100) to decimate
        """
        if percent > 100 or percent < 1:
            return
        self.__decimate = percent
        self.__n = int(self.__original * (percent/100.0))
        self.__tindex = np.linspace(0, self.__original-1, self.__n, dtype=int)
        self._update_time_steps()
        self.Modified()

    def set_time_delta(self, dt):
        """
        Set the time step interval in seconds
        """
        if self.__dt != dt:
            self.__dt = dt
            self._update_time_steps()
            self.Modified()

    def get_time_step_values(self):
        """Use this in ParaView decorator to register timesteps
        """
        return self.__timesteps.tolist() if self.__timesteps is not None else None

    def get_point(self):
        """Get the current point"""
        return list(self.__point)

    def get_normal(self):
        """Get the current normal vector"""
        return list(self.__normal)




class ConvertUnits(FilterPreserveTypeBase):
    """Convert points in an input data object to from meters to feet or vice versa.
    This simply uses a ``vtkTransformFilter`` and scales input data object with
    common conversions.
    """
    __displayname__ = 'Convert XYZ Units'
    __category__ = 'filter'
    def __init__(self, conversion='meter_to_feet', **kwargs):
        FilterPreserveTypeBase.__init__(self, **kwargs)
        self.__conversion = conversion

    @staticmethod
    def lookup_conversions(get_keys=False):
        """All Available conversions

        Return:
            dict: dictionary of conversion units
        """
        convs = dict(
            meter_to_feet=3.2808399,
            feet_to_meter=1/3.2808399,
        )
        if get_keys:
            return convs.keys()
        return convs

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output"""
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        # Get number of points
        pdo = self.GetOutputData(outInfo, 0)
        #### Perfrom task ####
        filt = vtk.vtkTransformFilter()
        trans = vtk.vtkTransform()
        trans.Scale(self.get_conversion(), self.get_conversion(), self.get_conversion())
        filt.SetTransform(trans)
        filt.SetInputDataObject(pdi)
        filt.Update()
        scaled = filt.GetOutputDataObject(0)
        pdo.DeepCopy(scaled)
        return 1



    def set_conversion(self, key):
        """Set the conversion via a lookup table"""
        convs = self.lookup_conversions()
        if isinstance(key, str):
            if key.lower() not in convs.keys():
                raise _helpers.PVGeoError('Converion `%s` not available.' % key)
        elif isinstance(key, int):
            key = convs.keys()[key]
        if self.__conversion != key:
            self.__conversion = key
            self.Modified()
        return 1

    def get_conversion(self):
        """Get the conversion value"""
        convs = self.lookup_conversions()
        return convs[self.__conversion]





class BuildSurfaceFromPoints(FilterBase):
    """From the sorted x, y, and z station locations in the input PolyData,
    create a surface to project down from the line of those points. Use the
    Z cells to control the size of the mesh surface
    """
    __displayname__ = 'Build Surface From Points'
    __category__ = 'filter'
    def __init__(self, **kwargs):
        FilterBase.__init__(self, inputType='vtkPolyData',
                            outputType='vtkUnstructuredGrid', **kwargs)
        self.__zcoords = CreateTensorMesh._read_cell_line('0. 50.')
        zcoords = kwargs.get('zcoords', self.__zcoords)
        if not isinstance(zcoords, (str, list, tuple, np.ndarray)):
            raise TypeError('zcoords of bad type.')
        if isinstance(zcoords, str):
            self.set_z_coords_str(zcoords)
        else:
            self.set_z_coords(zcoords)


    @staticmethod
    def create_surface(points, z_range):
        """From the sorted x, y, and z station locations, create a surface
        to display a seismic recording/migration on in space. The result is
        defined in the X,Y,Z-z_range 3D space.

        The z_range should be treated as relative coordinates to the values
        given on the third column of the points array. If you want the values
        in the z_range to be treated as the absolute coordinates, simply
        do not pass any Z values in the points array - if points is N by 2,
        then the values in z_range will be inferred as absolute.

        Args:
            points (np.ndarray): array-like of the station x and y locations
            (npts by 2-3) z_range (np.ndarray): The linear space of the z
            dimension. This will be filled out for every station location.

        Return:
            pyvista.UnstructuredGrid
        """
        if hasattr(points, 'values'):
            # This will extract data from pandas dataframes if those are given
            points = points.values
        points = np.array(points)
        z_range = np.array(z_range)
        xloc = points[:,0]
        yloc = points[:,1]
        if points.shape[1] > 2:
            zloc = points[:,2]
        else:
            val = np.nanmax(z_range)
            z_range = val - np.flip(z_range)
            zloc = np.full(xloc.shape, val)
        if not len(xloc) == len(yloc) == len(zloc):
            raise AssertionError('Coordinate shapes do not match.')
        nt = len(xloc)
        ns = len(z_range)

        # Extrapolate points to a 2D surface
        # repeat the XY locations across
        points = np.repeat(np.c_[xloc,yloc,zloc], ns, axis=0)
        # repeat the Z locations across
        tp = np.repeat(z_range.reshape((-1, len(z_range))), nt, axis=0)
        tp = zloc[:,None] - tp
        points[:,-1] = tp.ravel()

        # Create cell indices for that surface
        indexes = np.array(range(0, (nt*ns)))
        indexes = np.reshape(indexes, (nt, ns) )

        # Define the cell connectivity on the surface
        cellConn = np.zeros(( nt-1, ns-1 , 4), dtype=np.int)
        cellConn[:,:,0] = indexes[:-1, :-1]
        cellConn[:,:,1] = indexes[1:, :-1]
        cellConn[:,:,2] = indexes[1:, 1:]
        cellConn[:,:,3] = indexes[:-1, 1:]
        cellConn = cellConn.reshape((ns-1)*(nt-1) , 4)
        cells = vtk.vtkCellArray()
        cells.SetNumberOfCells(cellConn.shape[0])
        cells.SetCells(cellConn.shape[0], interface.convert_cell_conn(cellConn))

        # Produce the output
        output = pyvista.UnstructuredGrid()
        output.points = points
        output.SetCells(vtk.VTK_QUAD, cells)
        return output


    def RequestData(self, request, inInfo, outInfo):
        """Execute on pipeline"""
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        # Get number of points
        pdo = self.GetOutputData(outInfo, 0)
        #### Perfrom task ####
        data = pyvista.wrap(pdi)
        output = BuildSurfaceFromPoints.create_surface(data.points, np.array(self.__zcoords))
        pdo.DeepCopy(output)
        return 1

    def set_z_coords(self, zcoords):
        """Set the spacings for the cells in the Z direction

        Args:
            zcoords (list or np.array(floats)): the spacings along the Z-axis"""
        if len(zcoords) != len(self.__zcoords) or not np.allclose(self.__zcoords, zcoords):
            self.__zcoords = zcoords
            self.Modified()

    def set_z_coords_str(self, zcoordstr):
        """Set the spacings for the cells in the Z direction

        Args:
            zcoordstr (str)  : the spacings along the Z-axis in the UBC style"""
        zcoords = CreateTensorMesh._read_cell_line(zcoordstr)
        self.set_z_coords(zcoords)
