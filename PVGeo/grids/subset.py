__all__ = [
    'ExtractTopography',
]

__displayname__ = 'Subsetting'

import numpy as np
import vtk
from vtk.numpy_interface import dataset_adapter as dsa

from .. import _helpers, interface
from ..base import FilterBase

# NOTE: internal import - from scipy.spatial import cKDTree



###############################################################################

class ExtractTopography(FilterBase):
    """This filter takes two inputs: a gridded data set and a set of points for
    a Topography source. This will add a boolean data array to the cell data of
    the input grid on whether that cell should be active (under topographic
    layer).

    Note:
        This currenlty ignores time varying inputs. We can implement time
        variance but need to think about how we would like to do that. Should
        the topography surface be static and the volumetric data have time
        variance?

    """
    __displayname__ = 'Extract Topography'
    __category__ = 'filter'
    def __init__(self, op='underneath', tolerance=0.001, offset=0.0):
        FilterBase.__init__(self,
            nInputPorts=2, inputType='vtkDataSet',
            nOutputPorts=1)
        self._tolerance = tolerance
        self._offset = offset
        self._operation = self._underneath
        self.SetOperation(op)

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


    #### Extraction Methods ####

    @staticmethod
    def _query(topoPts, dataPts):
        try:
            # sklearn's KDTree is faster: use it if available
            from sklearn.neighbors import KDTree as Tree
        except:
            from scipy.spatial import cKDTree  as Tree
        tree = Tree(topoPts)
        i = tree.query(dataPts)[1].ravel()
        return topoPts[i]

    @staticmethod
    def _underneath(topoPts, dataPts, tolerance):
        comp = ExtractTopography._query(topoPts, dataPts)
        return np.array(dataPts[:,2] < (comp[:,2] - tolerance), dtype=int)

    @staticmethod
    def _intersection(topoPts, dataPts, tolerance):
        comp = ExtractTopography._query(topoPts, dataPts)
        return np.array(np.abs((dataPts[:,2] - comp[:,2])) < tolerance, dtype=int)

    @staticmethod
    def GetOperations():
        """Returns the extraction operation methods as callable objects in a
        dictionary
        """
        ops = dict(
            underneath=ExtractTopography._underneath,
            intersection=ExtractTopography._intersection,
        )
        return ops

    @staticmethod
    def GetOperationNames():
        """Gets a list of the extraction operation keys

        Return:
            list(str): the keys for getting the operations
        """
        ops = ExtractTopography.GetOperations()
        return list(ops.keys())

    @staticmethod
    def GetOperation(idx):
        """Gets a extraction operation based on an index in the keys

        Return:
            callable: the operation method
        """
        if isinstance(idx, str):
            return ExtractTopography.GetOperations()[idx]
        n = ExtractTopography.GetOperationNames()[idx]
        return ExtractTopography.GetOperations()[n]


    #### Pipeline Methods ####

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output"""
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
        topoPts = np.array(wtopo.Points) # mak sure we do not edit the input
        #  shift the topography points for the tree
        topoPts[:,2] = topoPts[:,2] + self._offset

        filt = vtk.vtkCellCenters()
        filt.SetInputDataObject(igrid)
        filt.Update()
        dataPts = dsa.WrapDataObject(filt.GetOutput(0)).Points

        active = self._operation(topoPts, dataPts, self._tolerance)

        # Now add cell data to output
        active = interface.convertArray(active, name='Extracted')
        grid.GetCellData().AddArray(active)
        return 1

    def Apply(self, data, points):
        self.SetInputDataObject(0, data)
        self.SetInputDataObject(1, points)
        self.Update()
        return interface.wrapvtki(self.GetOutput())

    #### Setters/Getters ####

    def SetTolerance(self, tol):
        if self._tolerance != tol:
            self._tolerance = tol
            self.Modified()

    def GetTolerance(self):
        return self._tolerance

    def SetOffset(self, offset):
        """Sets how far off (in Z dir) to slice the data"""
        if self._offset != offset:
            self._offset = offset
            self.Modified()

    def SetOperation(self, op):
        """Set the type of extraction to perform

        Args:
            op (str, int, or callable): The operation as a string key, int
            index, or callable method

        Note:
            This can accept a callable method to set a custom operation as long
            as its signature is: ``<callable>(self, topoPts, dataPts)``
        """
        if isinstance(op, str):
            op = ExtractTopography.GetOperations()[op]
        elif isinstance(op, int):
            op = ExtractTopography.GetOperation(op)
        if self._operation != op:
            self._operation = op
            self.Modified()
