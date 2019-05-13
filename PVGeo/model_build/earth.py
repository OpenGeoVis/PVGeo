__all__ = [
    'OutlineContinents',
    'GlobeSource',
]

import numpy as np
import pandas as pd
import vtk
from scipy.spatial import Delaunay
from vtk.util import numpy_support as nps

from .. import interface
from ..base import AlgorithmBase


class OutlineContinents(AlgorithmBase):
    """A simple data source to produce a ``vtkEarthSource`` outlining the
    Earth's continents. This works well with our ``GlobeSource``.
    """
    __displayname__ = 'Outline Continents'
    __category__ = 'source'
    def __init__(self, radius=6371.0e6):
        AlgorithmBase.__init__(self,
            nInputPorts=0,
            nOutputPorts=1, outputType='vtkPolyData')
        self.__radius = radius

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate the output"""
        pdo = self.GetOutputData(outInfo, 0)
        earth = vtk.vtkEarthSource()
        earth.SetRadius(self.__radius)
        earth.OutlineOn()
        earth.Update()
        pdo.ShallowCopy(earth.GetOutput())
        return 1

    def set_radius(self, radius):
        """Set the radius of the globe. Defualt is 6.371.0e9 meters"""
        if self.__radius != radius:
            self.__radius = radius
            self.Modified()


###############################################################################


class GlobeSource(AlgorithmBase):
    """Creates a globe/sphere the size of the Earth with texture coordinates
    already mapped. The globe's center is assumed to be (0,0,0).

    Args:
        radius (float): the radius to use
        npar (int): the number of parallels (latitude)
        nmer (int): the number of meridians (longitude)
    """
    __displayname__ = 'Globe Source'
    __category__ = 'source'
    def __init__(self, radius=6371.0e6, npar=15, nmer=36, **kwargs):
        AlgorithmBase.__init__(self, nInputPorts=0, nOutputPorts=1, outputType='vtkPolyData')
        self.__radius = radius
        self.__npar = npar
        self.__nmer = nmer
        # TODO: use **kwargs

    def spherical_to_cartesian(self, meridian, parallel):
        """Converts longitude/latitude to catesian coordinates. Assumes the
        arguments are given in degrees.
        """
        lon_r = np.radians(meridian)
        lat_r = np.radians(parallel)
        x =  self.__radius * np.cos(lat_r) * np.cos(lon_r)
        y = self.__radius * np.cos(lat_r) * np.sin(lon_r)
        z = self.__radius * np.sin(lat_r)
        return np.vstack((x, y, z)).T

    def create_sphere(self):
        """Creates longitude/latitude as 2D points and returns the corresponding
        texture coordinates for those positions."""
        lon = np.linspace(-180.0, 180.0, self.__nmer)
        lat = np.linspace(-90.0, 90.0, self.__npar)
        lon_g, lat_g = np.meshgrid(lon, lat, indexing='ij')
        pos = np.vstack([lon_g.ravel(), lat_g.ravel()]).T
        # Now create the texture map
        tcgx, tcgy = np.meshgrid(
                        np.linspace(0.0, 1.0, len(lon)),
                        np.linspace(0.0, 1.0, len(lat)),
                        indexing='ij')
        tex = np.vstack([tcgx.ravel(), tcgy.ravel()]).T
        return pos, tex

    def build_globe(self):
        """Generates the globe as ``vtkPolyData``"""
        pos, tex = self.create_sphere()
        pts = self.spherical_to_cartesian(pos[:,0], pos[:,1])
        points = interface.points_to_poly_data(pts).GetPoints()
        texcoords = interface.convert_array(tex, name='Texture Coordinates')
        # Now generate triangles
        cell_connectivity = Delaunay(pos).simplices.astype(int)
        cells = vtk.vtkCellArray()
        cells.SetNumberOfCells(cell_connectivity.shape[0])
        cells.SetCells(cell_connectivity.shape[0], interface.convert_cell_conn(cell_connectivity))
        # Generate output
        output = vtk.vtkPolyData()
        output.SetPoints(points)
        output.GetPointData().SetTCoords(texcoords)
        output.SetPolys(cells)
        return output

    def RequestData(self, request, inInfo, outInfo):
        """The pipeline executes this to generate output"""
        pdo = self.GetOutputData(outInfo, 0)
        globe = self.build_globe()
        pdo.ShallowCopy(globe)
        return 1

    def set_radius(self, radius):
        """Set the radius of the globe. Defualt is 6.371.0e9 meters"""
        if self.__radius != radius:
            self.__radius = radius
            self.Modified()

    def set_n_meridians(self, n):
        """Set the number of meridians to use"""
        if self.__nmer != n:
            self.__nmer = n
            self.Modified()

    def set_n_parallels(self, n):
        """Set the number of parallels to use"""
        if self.__npar != n:
            self.__npar = n
            self.Modified()
