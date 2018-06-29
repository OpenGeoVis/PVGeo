__all__ = [
    'CombineTables',
    'ReshapeTable',
]

# Import Helpers:
from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase
from .. import _helpers


###############################################################################

###############################################################################


class CombineTables(VTKPythonAlgorithmBase):
    """Takes two tables and combines them if they have the same number of rows."""
    def __init__(self):
        VTKPythonAlgorithmBase.__init__(self,
            nInputPorts=2, inputType='vtkTable',
            nOutputPorts=1, outputType='vtkTable')
        # Parameters... none

    # CRITICAL for multiple input ports
    def FillInputPortInformation(self, port, info):
        # all are tables so no need to check port
        info.Set(self.INPUT_REQUIRED_DATA_TYPE(), "vtkTable")
        return 1


    def RequestData(self, request, inInfo, outInfo):
        # Inputs from different ports:
        pdi0 = self.GetInputData(inInfo, 0, 0)
        pdi1 = self.GetInputData(inInfo, 1, 0)
        pdo = self.GetOutputData(outInfo, 0)

        pdo.DeepCopy(pdi0)

        # Get number of columns
        ncols1 = pdi1.GetNumberOfColumns()
        # Get number of rows
        nrows = pdi0.GetNumberOfRows()
        nrows1 = pdi1.GetNumberOfRows()
        assert(nrows == nrows1)

        for i in range(pdi1.GetRowData().GetNumberOfArrays()):
            arr = pdi1.GetRowData().GetArray(i)
            pdo.GetRowData().AddArray(arr)
        return 1


###############################################################################
#---- Reshape Table ----#

class ReshapeTable(VTKPythonAlgorithmBase):
    """This filter will take a vtkTable object and reshape it. This filter essentially treats vtkTables as 2D matrices and reshapes them using numpy.reshape in a C contiguous manner. Unfortunately, data fields will be renamed arbitrarily because VTK data arrays require a name."""
    def __init__(self):
        VTKPythonAlgorithmBase.__init__(self,
            nInputPorts=1, inputType='vtkTable',
            nOutputPorts=1, outputType='vtkTable')
        # Parameters
        self.__nrows = 4
        self.__ncols = False
        self.__names = []
        self.__order = 'F'

    def _Reshape(self, pdi, pdo):
        """
        Todo Description
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
                raise Exception('Too many array names. `ncols` specified as %d and %d names given.' % (self.__ncols, num))
        else:
            self.__names = ['Field %d' % i for i in range(self.__ncols)]

        # Make a 2D numpy array and fill with data from input table
        data = np.empty((cols,rows))
        for i in range(cols):
            c = pdi.GetColumn(i)
            data[i] = nps.vtk_to_numpy(c)

        if ((self.__ncols*self.__nrows) != (cols*rows)):
            raise Exception('Total number of elements must remain %d. Check reshape dimensions.' % (cols*rows))

        # Use numpy.reshape() to reshape data NOTE: only 2D because its a table
        # NOTE: column access of this reshape is not contigous
        data = np.array(np.reshape(data, (self.__nrows,self.__ncols), order=self.__order))
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
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        pdo = self.GetOutputData(outInfo, 0)
        # Perfrom task
        self._Reshape(pdi, pdo)
        return 1


    #### Seters and Geters ####

    def SetNames(self, names):
        """Set names using a semicolon (;) seperated list"""
        # parse the names (a semicolon seperated list of names)
        names = names.split(';')
        if self.__names != names:
            self.__names = names
            self.Modified()

    def AddName(self, name):
        """Use to append a name to the names list"""
        self.__names.append(name)
        self.Modified()

    def GetNames(self):
        return self.__names

    def SetNumberOfColumns(self, ncols):
        if self.__ncols != ncols:
            self.__ncols = ncols
            self.Modified()

    def SetNumberOfRows(self, nrows):
        if self.__nrows != nrows:
            self.__nrows = nrows
            self.Modified()

    def SetOrder(self, order):
        if self.__order != order:
            self.__order = order
            self.Modified()
