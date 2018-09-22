__all__ = [
    'EarthSource',
]

import vtk
# Import Helpers:
from ..base import AlgorithmBase
from .. import _helpers


class EarthSource(AlgorithmBase):
    """A simple data source to produce a ``vtkEarthSource``
    """
    __displayname__ = 'Earth Source'
    __category__ = 'source'
    def __init__(self, radius=6371.0):
        AlgorithmBase.__init__(self,
            nInputPorts=0,
            nOutputPorts=1, outputType='vtkPolyData')
        self.__radius = radius

    def RequestData(self, request, inInfo, outInfo):
        pdo = self.GetOutputData(outInfo, 0)
        earth = vtk.vtkEarthSource()
        earth.SetRadius(self.__radius)
        earth.OutlineOn()
        earth.Update()
        pdo.ShallowCopy(earth.GetOutput())
        return 1

    def SetRadius(self, radius):
        if self.__radius != radius:
            self.__radius = radius
            self.Modified()
