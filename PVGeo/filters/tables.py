__all__ = [
    'CombineTables',
    'ReshapeTable',
]

import numpy as np
from vtk.util import numpy_support as nps
from vtk.numpy_interface import dataset_adapter as dsa
# Import Helpers:
from ..base import FilterBase
from .. import _helpers


###############################################################################

###############################################################################


class CombineTables(FilterBase):
    """Takes two tables and combines them if they have the same number of rows.
    """
    __displayname__ = 'Combine Tables'
    __type__ = 'filter'
    def __init__(self):
        FilterBase.__init__(self,
            nInputPorts=2, inputType='vtkTable',
            nOutputPorts=1, outputType='vtkTable')
        # Parameters... none

    # CRITICAL for multiple input ports
    def FillInputPortInformation(self, port, info):
        """Used by pipeline. Necessary when dealing with multiple input ports
        """
        # all are tables so no need to check port
        info.Set(self.INPUT_REQUIRED_DATA_TYPE(), "vtkTable")
        return 1


    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output
        """
        # Inputs from different ports:
        pdi0 = self.GetInputData(inInfo, 0, 0)
        pdi1 = self.GetInputData(inInfo, 1, 0)
        pdo = self.GetOutputData(outInfo, 0)

        pdo.DeepCopy(pdi0)

        # Get number of rows
        nrows = pdi0.GetNumberOfRows()
        nrows1 = pdi1.GetNumberOfRows()
        assert(nrows == nrows1)

        for i in range(pdi1.GetRowData().GetNumberOfArrays()):
            arr = pdi1.GetRowData().GetArray(i)
            pdo.GetRowData().AddArray(arr)
        return 1

    def Apply(self, table0, table1):
        self.SetInputDataObject(0, table0)
        self.SetInputDataObject(1, table1)
        self.Update()
        return self.GetOutput()


###############################################################################
#---- Reshape Table ----#

class ReshapeTable(FilterBase):
    """This filter will take a ``vtkTable`` object and reshape it. This filter essentially treats ``vtkTable``s as 2D matrices and reshapes them using ``numpy.reshape`` in a C contiguous manner. Unfortunately, data fields will be renamed arbitrarily because VTK data arrays require a name.
    """
    __displayname__ = 'Reshape Table'
    __type__ = 'filter'
    def __init__(self, **kwargs):
        FilterBase.__init__(self,
            nInputPorts=1, inputType='vtkTable',
            nOutputPorts=1, outputType='vtkTable')
        # Parameters
        self.__nrows = kwargs.get('nrows', 1)
        self.__ncols = kwargs.get('ncols', 1)
        self.__names = kwargs.get('names', [])
        self.__order = kwargs.get('order', 'F')

    def _Reshape(self, pdi, pdo):
        """Internal helper to perfrom the reshape
        """
        # Get number of columns
        cols = pdi.GetNumberOfColumns()
        # Get number of rows
        rows = pdi.GetColumn(0).GetNumberOfTuples()

        if len(self.__names) is not 0:
            num = len(self.__names)
            if num < self.__ncols:
                for i in range(num, self.__ncols):
                    self.__names.append('Field %d' % i)
            elif num > self.__ncols:
                raise _helpers.PVGeoError('Too many array names. `ncols` specified as %d and %d names given.' % (self.__ncols, num))
        else:
            self.__names = ['Field %d' % i for i in range(self.__ncols)]

        # Make a 2D numpy array and fill with data from input table
        data = np.empty((rows,cols))
        for i in range(cols):
            c = pdi.GetColumn(i)
            data[:,i] = nps.vtk_to_numpy(c)

        if ((self.__ncols*self.__nrows) != (cols*rows)):
            raise _helpers.PVGeoError('Total number of elements must remain %d. Check reshape dimensions.' % (cols*rows))

        # Use numpy.reshape() to reshape data NOTE: only 2D because its a table
        # NOTE: column access of this reshape is not contigous
        data = np.array(np.reshape(data.flatten(), (self.__nrows,self.__ncols), order=self.__order))
        pdo.SetNumberOfRows(self.__nrows)

        # Add new array to output table and assign incremental names (e.g. Field0)
        for i in range(self.__ncols):
            # Make a contigous array from the column we want
            col = np.array(data[:,i])
            # allow type to be determined by input
            insert = nps.numpy_to_vtk(num_array=col, deep=True) # array_type=vtk.VTK_FLOAT
            # VTK arrays need a name. Set arbitrarily
            insert.SetName(self.__names[i])
            #pdo.AddColumn(insert) # these are not getting added to the output table
            # ... work around:
            pdo.GetRowData().AddArray(insert) # NOTE: this is in the FieldData

        return pdo

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline
        """
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        pdo = self.GetOutputData(outInfo, 0)
        # Perfrom task
        self._Reshape(pdi, pdo)
        return 1


    #### Seters and Geters ####

    def SetNames(self, names):
        """Set names using a semicolon (;) seperated string or a list of strings

        Args:
            names (string): a string of data array names for the reshaped table using a semicolon (;) to spearate
        """
        # parse the names (a semicolon seperated list of names)
        if isinstance(names, str):
            names = names.split(';')
        if self.__names != names:
            self.__names = names
            self.Modified()

    def AddName(self, name):
        """Use to append a name to the list of data array names for the output table
        """
        self.__names.append(name)
        self.Modified()

    def GetNames(self):
        return self.__names

    def SetNumberOfColumns(self, ncols):
        """Set the number of columns for the output ``vtkTable``
        """
        if isinstance(ncols, float):
            ncols = int(ncols)
        if self.__ncols != ncols:
            self.__ncols = ncols
            self.Modified()

    def SetNumberOfRows(self, nrows):
        """Set the number of rows for the output ``vtkTable``
        """
        if isinstance(nrows, float):
            nrows = int(nrows)
        if self.__nrows != nrows:
            self.__nrows = nrows
            self.Modified()

    def SetOrder(self, order):
        """Set the reshape order (``'C'`` of ``'F'``)
        """
        if self.__order != order:
            self.__order = order
            self.Modified()
