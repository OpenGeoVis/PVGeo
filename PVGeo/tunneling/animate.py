__all__ = [
    'AnimateTBM',
]

import vtk

from ..base import AlgorithmBase


class AnimateTBM(AlgorithmBase):
    """This filter analyzes a vtkTable containing position information about a Tunnel Boring Machine (TBM). This Filter iterates over each row of the table as a timestep and uses the XYZ coordinates of the three different parts of the TBM to generate a tube that represents the TBM."""

    def __init__(self):
        AlgorithmBase.__init__(
            self,
            nInputPorts=1,
            inputType='vtkTable',
            nOutputPorts=1,
            outputType='vtkPolyData',
        )
        # Parameters
        self.__diameter = (17.45,)
        self.__dt = 1.0

    def RequestData(self, request, inInfo, outInfo):
        from vtk.numpy_interface import dataset_adapter as dsa

        import PVGeo._helpers as inputhelp
        from PVGeo.filters import pointsToTube

        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        pdo = self.GetOutputData(outInfo, 0)
        # Grab input arrays to process from drop down menus
        # - Grab all fields for input arrays:
        fields = []
        for i in range(3):
            fields.append(inputhelp.get_selected_array_field(self, i))
        # - Simply grab the names
        names = []
        for i in range(9):
            names.append(inputhelp.get_selected_array_name(self, i))
        # Pass array names and associations on to process
        # Get the input arrays
        wpdi = dsa.WrapDataObject(pdi)
        arrs = []
        for i in range(9):
            arrs.append(inputhelp.get_array(wpdi, fields[i], names[i]))

        # grab coordinates for each part of boring machine at time idx as row
        executive = self.GetExecutive()
        outInfo = executive.GetOutputInformation(0)
        idx = int(outInfo.Get(executive.UPDATE_TIME_STEP()) / self.__dt)
        pts = []
        for i in range(3):
            x = arrs[i * 3][idx]
            y = arrs[i * 3 + 1][idx]
            z = arrs[i * 3 + 2][idx]
            pts.append((x, y, z))
        # now exectute a points to tube filter
        vtk_pts = vtk.vtkPoints()
        for i in range(len(pts)):
            vtk_pts.InsertNextPoint(pts[i][0], pts[i][1], pts[i][2])
        poly = vtk.vtkPolyData()
        poly.SetPoints(vtk_pts)
        pointsToTube(
            poly, radius=self.__diameter / 2, numSides=20, nrNbr=False, pdo=pdo
        )
        return 1

    def RequestInformation(self, request, inInfo, outInfo):
        import numpy as np

        executive = self.GetExecutive()
        outInfo = executive.GetOutputInformation(0)
        # Calculate list of timesteps here
        # - Get number of rows in table and use that for num time steps
        nrows = int(self.GetInput().GetColumn(0).GetNumberOfTuples())
        xtime = np.arange(0, nrows * self.__dt, self.__dt, dtype=float)
        outInfo.Remove(executive.TIME_STEPS())
        for i in range(len(xtime)):
            outInfo.Append(executive.TIME_STEPS(), xtime[i])
        # Remove and set time range info
        outInfo.Remove(executive.TIME_RANGE())
        outInfo.Append(executive.TIME_RANGE(), xtime[0])
        outInfo.Append(executive.TIME_RANGE(), xtime[-1])
        return 1
