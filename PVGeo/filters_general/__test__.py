import unittest
import numpy as np

# VTK imports:
import vtk
from vtk.util import numpy_support as nps
from vtk.numpy_interface import dataset_adapter as dsa

# Functionality to test:
from .poly import *
from .slicing import *
from .tables import *
from .voxelize import *
from .xyz import *

RTOL = 0.000001

def _numToVTK(arr, name):
    c = nps.numpy_to_vtk(num_array=arr, deep=True)
    c.SetName(name)
    return c

###############################################################################
###############################################################################

class TestCombineTables(unittest.TestCase):
    """
    Test the `CombineTables` filter
    """
    def setUp(self):
        # Create some input tables
        self.t0 = vtk.vtkTable()
        self.t1 = vtk.vtkTable()
        # Populate the tables
        self.n = 100
        self.titles = ('Array 0', 'Array 1', 'Array 2')
        self.arrs = [None, None, None]
        self.arrs[0] = np.random.random(self.n) # Table 0
        self.arrs[1] = np.random.random(self.n) # Table 0
        self.arrs[2] = np.random.random(self.n) # Table 1
        self.t0.AddColumn(_numToVTK(self.arrs[0], self.titles[0]))
        self.t0.AddColumn(_numToVTK(self.arrs[1], self.titles[1]))
        self.t1.AddColumn(_numToVTK(self.arrs[2], self.titles[2]))
        # Now use the `CombineTables` filter:
        f = CombineTables()
        f.SetInputDataObject(0, self.t0)
        f.SetInputDataObject(1, self.t1)
        f.Update()
        self.TABLE = f.GetOutputDataObject(0)


    #########################


    def test_shape(self):
        """Test `CombineTables`: table shape"""
        self.assertEqual(self.TABLE.GetNumberOfColumns(), len(self.titles))
        self.assertEqual(self.TABLE.GetNumberOfRows(), self.n)

    def test_data_array_names(self):
        """Test `CombineTables`: data array names"""
        for i in range(len(self.titles)):
            self.assertEqual(self.TABLE.GetColumnName(i), self.titles[i])

    def test_data_fidelity(self):
        wpdi = dsa.WrapDataObject(self.TABLE)
        for i in range(len(self.titles)):
            arr = wpdi.RowData[self.titles[i]]
            self.assertTrue(np.allclose(arr, self.arrs[i], rtol=RTOL))

###############################################################################


class TestReshapeTable(unittest.TestCase):
    """
    Test the `ReshapeTable` filter
    """
    def setUp(self):
        # Create some input tables
        self.t0 = vtk.vtkTable()
        # Populate the tables
        self.arrs = [None, None, None]
        self.n = 4
        self.ncols = 2
        self.nrows = int(self.n * len(self.arrs) / self.ncols)
        self.titles = ('Array 0', 'Array 1', 'Array 2')
        self.arrs[0] = np.random.random(self.n) # Table 0
        self.arrs[1] = np.random.random(self.n) # Table 0
        self.arrs[2] = np.random.random(self.n) # Table 1
        self.t0.AddColumn(_numToVTK(self.arrs[0], self.titles[0]))
        self.t0.AddColumn(_numToVTK(self.arrs[1], self.titles[1]))
        self.t0.AddColumn(_numToVTK(self.arrs[2], self.titles[2]))
        return


    def _check_shape(self, table):
        self.assertEqual(table.GetNumberOfRows(), self.nrows)
        self.assertEqual(table.GetNumberOfColumns(), self.ncols)
        return

    def _check_data_fidelity(self, table, order):
        wpdi = dsa.WrapDataObject(table)
        tarr = np.zeros((self.nrows, self.ncols))
        for i in range(self.ncols):
            tarr[:,i] = wpdi.RowData[i]
        arrs = np.array(self.arrs).T
        arrs = arrs.flatten()
        arrs = np.reshape(arrs, (self.nrows, self.ncols), order=order)
        self.assertEqual(tarr.shape, arrs.shape)
        self.assertTrue(np.allclose(tarr, arrs, rtol=RTOL))
        return

    def _check_data_array_titles(self, table, titles):
        for i in range(len(titles)):
            self.assertEqual(table.GetColumnName(i), titles[i])
        return

    def _generate_output(self, order, titles=None):
        f = ReshapeTable()
        f.SetInputDataObject(0, self.t0)
        f.SetNumberOfColumns(self.ncols)
        f.SetNumberOfRows(self.nrows)
        f.SetOrder(order)
        if titles is not None:
            f.SetNames(titles)
        f.Update()
        return f.GetOutputDataObject(0)

    ###############

    def test_reshape_f(self):
        """Test `ReshapeTable`: F-order, no input names"""
        order = 'F'
        table = self._generate_output(order, titles=None)
        # Check output:
        self._check_shape(table)
        self._check_data_fidelity(table, order)
        self._check_data_array_titles(table, ['Field %d' % i for i in range(self.ncols)])
        return

    def test_reshape_f_names(self):
        """Test `ReshapeTable`: F-order, input names given"""
        order = 'F'
        titles = ['Title %d' % i for i in range(self.ncols)]
        table = self._generate_output(order, titles=titles)
        # Check output:
        self._check_shape(table)
        self._check_data_fidelity(table, order)
        self._check_data_array_titles(table, titles)
        return


    def test_reshape_c(self):
        """Test `ReshapeTable`: C-order, no input names"""
        order = 'C'
        table = self._generate_output(order, titles=None)
        # Check output:
        self._check_shape(table)
        self._check_data_fidelity(table, order)
        self._check_data_array_titles(table, ['Field %d' % i for i in range(self.ncols)])
        return

    def test_reshape_c_names(self):
        """Test `ReshapeTable`: C-order, input names given"""
        order = 'C'
        titles = ['Title %d' % i for i in range(self.ncols)]
        table = self._generate_output(order, titles=titles)
        # Check output:
        self._check_shape(table)
        self._check_data_fidelity(table, order)
        self._check_data_array_titles(table, titles)
        return




###############################################################################
###############################################################################
