__all__ = [
    'ExtractTopography',
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



###############################################################################

class ExtractTopography(FilterBase):
    """This filter takes two inputs: a gridded data set and a set of points for a Topography source. This will add a boolean data array to the cell data of the input grid on whether that cell should be active (under topographic layer).

    """
    __displayname__ = 'Extract Topography'
    __type__ = 'filter'
    def __init__(self):
        FilterBase.__init__(self,
            nInputPorts=2, inputType='vtkDataObject',
            nOutputPorts=1)

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
        wtopo = dsa.WrapDataObject(topo) # NumPy wrapped points
        topoPts = np.array(wtopo.Points) # New NumPy array of points so we dont destroy input
        tree = cKDTree(topoPts[:, 0:2]) # NOTE: only on the XY plane

        # OPTIMIZE: accelerate this to harness structured coords
        for i in range(ncells):
            voxel = grid.GetCell(i)
            x,y,z = self.__GetVoxelCenter(voxel)
            # Search for same XY point in topoPts
            ptsi = tree.query([[x, y]], k=1)[1]
            if z > topoPts[ptsi[0]][2]:
                active[i] = 0
            else:
                active[i] = 1


        # Now add cell data to output
        data = nps.numpy_to_vtk(num_array=active, deep=True)
        data.SetName('Active Topography')
        grid.GetCellData().AddArray(data)
        return 1

    def Apply(self, data, points):
        self.SetInputDataObject(0, data)
        self.SetInputDataObject(1, points)
        self.Update()
        return self.GetOutput()
