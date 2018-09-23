__all__ = [
    'CombineTables',
    'ReshapeTable',
    'ExtractArray',
    'SplitTableOnArray',
]

import numpy as np
import pandas as pd
import vtk
from vtk.util import numpy_support as nps
from vtk.numpy_interface import dataset_adapter as dsa
# Import Helpers:
from ..base import FilterBase
from .. import _helpers
from .. import interface


###############################################################################

###############################################################################


class CombineTables(FilterBase):
    """Takes two tables and combines them if they have the same number of rows.
    """
    __displayname__ = 'Combine Tables'
    __category__ = 'filter'
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
    __category__ = 'filter'
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
            data[:,i] = interface.convertArray(c)

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
            # VTK arrays need a name. Set arbitrarily
            insert = interface.convertArray(col, name=self.__names[i]) # array_type=vtk.VTK_FLOAT
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



class ExtractArray(FilterBase):
    """Extract an array from a ``vtkDataSet`` and make a ``vtkTable`` of it.
    """
    __displayname__ = 'Extract Array'
    __category__ = 'filter'
    def __init__(self):
        FilterBase.__init__(self,
            nInputPorts=1, inputType='vtkDataSet',
            nOutputPorts=1, outputType='vtkTable')
        self.__inputArray = [None, None]


    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output
        """
        # Inputs from different ports:
        pdi = self.GetInputData(inInfo, 0, 0)
        table = self.GetOutputData(outInfo, 0)


        # Note user has to select a single array to save out
        field, name = self.__inputArray[0], self.__inputArray[1]
        vtkarr = _helpers.getVTKArray(pdi, field, name)

        table.GetRowData().AddArray(vtkarr)

        return 1

    def SetInputArrayToProcess(self, idx, port, connection, field, name):
        """Used to set the input array(s)

        Args:
            idx (int): the index of the array to process
            port (int): input port (use 0 if unsure)
            connection (int): the connection on the port (use 0 if unsure)
            field (int): the array field (0 for points, 1 for cells, 2 for field, and 6 for row)
            name (int): the name of the array
        """
        if self.__inputArray[0] != field:
            self.__inputArray[0] = field
            self.Modified()
        if self.__inputArray[1] != name:
            self.__inputArray[1] = name
            self.Modified()
        return 1

    def Apply(self, inputDataObject, arrayName):
        self.SetInputDataObject(inputDataObject)
        arr, field = _helpers.searchForArray(inputDataObject, arrayName)
        self.SetInputArrayToProcess(0, 0, 0, field, arrayName)
        self.Update()
        return self.GetOutput()



###############################################################################



class SplitTableOnArray(FilterBase):
    """A filter to seperate table data based on the unique values of a given data
    array into a ``vtkMultiBlockDataSet``.
    """
    __displayname__ = 'Split Table On Array'
    __category__ = 'filter'
    def __init__(self):
        FilterBase.__init__(self, nInputPorts=1, inputType='vtkTable',
                            nOutputPorts=1, outputType='vtkMultiBlockDataSet')
        self.__inputArray = [None, None]


    def RequestData(self, request, inInfo, outInfo):
        # Get input/output of Proxy
        table = self.GetInputData(inInfo, 0, 0)
        # Get number of points
        output = vtk.vtkMultiBlockDataSet.GetData(outInfo, 0)
        #### Perfrom task ####
        # Get input array
        field, name = self.__inputArray[0], self.__inputArray[1]
        wtbl = dsa.WrapDataObject(table)
        spliton = _helpers.getNumPyArray(wtbl, field, name)
        uniq = np.unique(spliton)
        # Split the input data based on indices
        df = interface.tableToDataFrame(table)
        blk = 0
        output.SetNumberOfBlocks(len(uniq))
        for val in uniq:
            temp = interface.dataFrameToTable(df[df[name] == val])
            output.SetBlock(blk, temp)
            output.GetMetaData(blk).Set(vtk.vtkCompositeDataSet.NAME(), '{}{}'.format(name, val))
            blk += 1

        return 1


    def SetInputArrayToProcess(self, idx, port, connection, field, name):
        """Used to set the input array(s)

        Args:
            idx (int): the index of the array to process
            port (int): input port (use 0 if unsure)
            connection (int): the connection on the port (use 0 if unsure)
            field (int): the array field (0 for points, 1 for cells, 2 for field, and 6 for row)
            name (int): the name of the array
        """
        if self.__inputArray[0] != field:
            self.__inputArray[0] = field
            self.Modified()
        if self.__inputArray[1] != name:
            self.__inputArray[1] = name
            self.Modified()
        return 1


    def Apply(self, inputDataObject, arrayName):
        self.SetInputDataObject(inputDataObject)
        arr, field = _helpers.searchForArray(inputDataObject, arrayName)
        self.SetInputArrayToProcess(0, 0, 0, field, arrayName)
        self.Update()
        return self.GetOutput()

###############################################################################
