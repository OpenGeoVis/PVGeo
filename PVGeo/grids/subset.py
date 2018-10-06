__all__ = [
    'ExtractTopography',
]

import vtk
import numpy as np
from vtk.numpy_interface import dataset_adapter as dsa
from datetime import datetime
# Import Helpers:
from ..base import FilterBase
from .. import _helpers
from .. import interface
# NOTE: internal import - from scipy.spatial import cKDTree



###############################################################################

class ExtractTopography(FilterBase):
    """This filter takes two inputs: a gridded data set and a set of points for a Topography source. This will add a boolean data array to the cell data of the input grid on whether that cell should be active (under topographic layer).

    """
    __displayname__ = 'Extract Topography'
    __category__ = 'filter'
    def __init__(self):
        FilterBase.__init__(self,
            nInputPorts=2, inputType='vtkDataSet',
            nOutputPorts=1)
        self.__tolerance = 0.001

    # CRITICAL for multiple input ports
    def FillInputPortInformation(self, port, info):
        """This simply makes sure the user selects the correct inputs
        """
        typ = 'vtkDataSet'
        if port == 1:
            typ = 'vtkPolyData' # Make sure topography are poly data
        info.Set(self.INPUT_REQUIRED_DATA_TYPE(), typ)
        return 1

    # THIS IS CRUCIAL to preserve data type through filter
    def RequestDataObject(self, request, inInfo, outInfo):
        """Constructs the output data object based on the input data object
        """
        self.OutputType = self.GetInputData(inInfo, 0, 0).GetClassName()
        self.FillOutputPortInformation(0, outInfo.GetInformationObject(0))
        return 1


    @staticmethod
    def __GetVoxelCenter(voxel):
        """Returns tuple for center of Voxel

        Note: The Z-coordinate is at the top of the cell
        """
        bounds = voxel.GetBounds()
        x = (bounds[0]+bounds[1])/2.0
        y = (bounds[2]+bounds[3])/2.0
        z = bounds[5]#(bounds[4]+bounds[5])/2.0
        return (x, y, z)

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output"""
        from scipy.spatial import cKDTree # NOTE: Must have SciPy in ParaView
        # Get input/output of Proxy
        igrid = self.GetInputData(inInfo, 0, 0) # Port 0: grid
        topo = self.GetInputData(inInfo, 1, 0) # Port 1: topography
        grid = self.GetOutputData(outInfo, 0)

        # Perfrom task
        grid.DeepCopy(igrid)
        ncells = grid.GetNumberOfCells()
        active = np.zeros((ncells), dtype=int)
        # Now iterate through the cells in the grid and test if they are beneath the topography
        wtopo = dsa.WrapDataObject(topo)
        topoPts = wtopo.Points

        filt = vtk.vtkCellCenters()
        filt.SetInputDataObject(igrid)
        filt.Update()
        datapts = dsa.WrapDataObject(filt.GetOutput(0)).Points

        tree = cKDTree(topoPts)
        i = tree.query(datapts)[1]
        comp = topoPts[i]
        active = np.array(datapts[:,2] < (comp[:,2] - self.__tolerance), dtype=int)

        # Now add cell data to output
        active = interface.convertArray(active, name='Active Topography')
        grid.GetCellData().AddArray(active)
        return 1

    def Apply(self, data, points):
        self.SetInputDataObject(0, data)
        self.SetInputDataObject(1, points)
        self.Update()
        return self.GetOutput()

    def SetTolerance(self, tol):
        if self.__tolerance != tol:
            self.__tolerance = tol
            self.Modified()

    def GetTolerance(self):
        return self.__tolerance
