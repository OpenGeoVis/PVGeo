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
    """This filter takes two inputs: any mesh dataset and a set of points for
    a topography source. This will add a boolean data array to the cell data of
    the input grid on whether that cell should be active (under topographic
    layer). A user can also choose to directly extract the data rather than
    appending a boolean scalar array via the ``remove`` argument.

    Args:
        op (str, int, or callable): The operation as a string key, int
            index, or callable method

        tolerance (float): buffer around the topography surface to include as
            part of the decision boundary

        offset (float): static value to shift the reference topography surface

        ivert (bool): optional to invert the extraction.

        remove (bool): Optional parameter to apply a thresholding filter and
            return a ``vtkUnstructuredGrid`` object with only the extracted
            cells. The ``remove`` option is only available in Python
            environments (not available in ParaView). The ``remove`` flag must
            be set at the time of instantiation of this algorithm.
            This does not actually update the algorithm's output data object
            but applies a ``pyvista`` threshold filter to pass a new data object
            after calling ``apply``.


    Note:
        This currenlty ignores time varying inputs. We can implement time
        variance but need to think about how we would like to do that. Should
        the topography surface be static and the volumetric data have time
        variance?

    """
    __displayname__ = 'Extract Topography'
    __category__ = 'filter'
    def __init__(self, op='underneath', tolerance=0.001, offset=0.0,
                 invert=False, remove=False):
        FilterBase.__init__(self,
            nInputPorts=2, inputType='vtkDataSet',
            nOutputPorts=1)
        self._tolerance = tolerance
        self._offset = offset
        self._invert = invert
        self._remove = remove
        self._operation = self._underneath
        self.set_operation(op)

    # CRITICAL for multiple input ports
    def FillInputPortInformation(self, port, info):
        """This simply makes sure the user selects the correct inputs
        """
        typ = 'vtkDataSet'
        if port == 1:
            typ = 'vtkPointSet' # Make sure topography is some sort of point set
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
    def _query(topo_points, data_points):
        """Querrys the data points for their closest point on the topography
        surface"""
        try:
            # sklearn's KDTree is faster: use it if available
            from sklearn.neighbors import KDTree as Tree
        except ImportError:
            from scipy.spatial import cKDTree  as Tree
        tree = Tree(topo_points)
        i = tree.query(data_points)[1].ravel()
        return topo_points[i]

    @staticmethod
    def _underneath(topo_points, data_points, tolerance):
        """Extract cells underneath the topography surface"""
        comp = ExtractTopography._query(topo_points, data_points)
        return np.array(data_points[:,2] < (comp[:,2] - tolerance), dtype=int)

    @staticmethod
    def _intersection(topo_points, data_points, tolerance):
        """Extract cells intersecting the topography surface"""
        comp = ExtractTopography._query(topo_points, data_points)
        return np.array(np.abs((data_points[:,2] - comp[:,2])) < tolerance, dtype=int)

    @staticmethod
    def get_operations():
        """Returns the extraction operation methods as callable objects in a
        dictionary
        """
        ops = dict(
            underneath=ExtractTopography._underneath,
            intersection=ExtractTopography._intersection,
        )
        return ops

    @staticmethod
    def get_operation_names():
        """Gets a list of the extraction operation keys

        Return:
            list(str): the keys for getting the operations
        """
        ops = ExtractTopography.get_operations()
        return list(ops.keys())

    @staticmethod
    def get_operation(idx):
        """Gets a extraction operation based on an index in the keys

        Return:
            callable: the operation method
        """
        if isinstance(idx, str):
            return ExtractTopography.get_operations()[idx]
        n = ExtractTopography.get_operation_names()[idx]
        return ExtractTopography.get_operations()[n]


    #### Pipeline Methods ####

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output"""
        # Get input/output of Proxy
        igrid = self.GetInputData(inInfo, 0, 0) # Port 0: grid
        topo = self.GetInputData(inInfo, 1, 0) # Port 1: topography
        grid = self.GetOutputData(outInfo, 0)
        grid.DeepCopy(igrid)

        # Perfrom task
        ncells = igrid.GetNumberOfCells()
        active = np.zeros((ncells), dtype=int)
        # Now iterate through the cells in the grid and test if they are beneath the topography
        wtopo = dsa.WrapDataObject(topo)
        topo_points = np.array(wtopo.Points) # mak sure we do not edit the input
        #  shift the topography points for the tree
        topo_points[:,2] = topo_points[:,2] + self._offset

        filt = vtk.vtkCellCenters()
        filt.SetInputDataObject(igrid)
        filt.Update()
        data_points = dsa.WrapDataObject(filt.GetOutput(0)).Points

        active = self._operation(topo_points, data_points, self._tolerance)

        if self._invert:
            # NOTE: assumes the given operation produces zeros and ones only
            active = 1 - active

        # Now add cell data to output
        active = interface.convert_array(active, name='Extracted')
        grid.GetCellData().AddArray(active)
        return 1

    def apply(self, data, points):
        """Run the algorithm on the input data using the topography points"""
        self.SetInputDataObject(0, data)
        self.SetInputDataObject(1, points)
        self.Update()
        output = interface.wrap_pyvista(self.GetOutput())
        if self._remove:
            # NOTE: Assumes the given operation produces zeros and ones only
            #       Also, this does not update the algorithm's output.
            #       This only sends a new thresholded dataset to the user.
            return output.threshold(0.5, scalars='Extracted')
        return output

    #### Setters/Getters ####

    def set_tolerance(self, tol):
        """Set the tolerance threshold for the querry"""
        if self._tolerance != tol:
            self._tolerance = tol
            self.Modified()

    def get_tolerance(self):
        """Get the tolerance threshold for the querry"""
        return self._tolerance

    def set_offset(self, offset):
        """Sets how far off (in Z dir) to slice the data"""
        if self._offset != offset:
            self._offset = offset
            self.Modified()

    def set_invert(self, flag):
        """Sets the boolean flag on whether to invert the extraction."""
        if self._invert != flag:
            self._invert = flag
            self.Modified()

    def set_operation(self, op):
        """Set the type of extraction to perform.

        Args:
            op (str, int, or callable): The operation as a string key, int
                index, or callable method

        Note:
            This can accept a callable method to set a custom operation as long
            as its signature is ``<callable>(self, topo_points, data_points)`` and it
            strictly produces an integer array of zeros and ones.
        """
        if isinstance(op, str):
            op = ExtractTopography.get_operations()[op]
        elif isinstance(op, int):
            op = ExtractTopography.get_operation(op)
        if self._operation != op:
            self._operation = op
            self.Modified()
