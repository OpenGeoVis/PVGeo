all = [
    'EarthSource',
]

import vtk
# Import Helpers:
from ..base import PVGeoAlgorithmBase
from .. import _helpers


class EarthSource(PVGeoAlgorithmBase):
    """@desc: a simple data source to produce a `vtkEarthSource`"""
    def __init__(self):
        PVGeoAlgorithmBase.__init__(self,
            nInputPorts=0,
            nOutputPorts=1, outputType='vtkPolyData')
        self.__radius = 6371.0

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
