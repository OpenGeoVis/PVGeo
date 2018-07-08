import unittest
import shutil
import tempfile
import os
import numpy as np

# VTK imports:
from vtk.util import numpy_support as nps
from vtk.numpy_interface import dataset_adapter as dsa

# Functionality to test:
from .delimited import *
from .binaries import *

RTOL = 0.000001

class TestDelimitedTextReader(unittest.TestCase):
    """
    Test the `DelimitedTextReader`: A widely used base class
    """
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.commafname = os.path.join(self.test_dir, 'comma.txt')
        self.tabfname = os.path.join(self.test_dir, 'tab.txt')
        # Make a temporary delimited text file to test:
        lines = ['This is a header line to skip',
                 'int,str,float ! Comment,this line has the data array names',
                 '5,foo,6.9',
                 '1,bar,8.5 ! another comment',
                 '3,oof,7.7'
                 ]
        # Append newlines
        lines = [ln+'\n' for ln in lines]
        # Now write contents to files
        f = open(self.commafname, 'w')
        f.writelines(lines)
        f.close()
        f = open(self.tabfname, 'w')
        f.writelines([ln.replace(',', '\t') for ln in lines])
        f.close()
        return

    def tearDown(self):
        # Remove the test data directory after the test
        shutil.rmtree(self.test_dir)

    ###########################################

    def _check_shape(self, table):
        # Check number of rows
        self.assertEqual(table.GetNumberOfRows(), 3)
        # Check number of columns:
        self.assertEqual(table.GetNumberOfColumns(), 3)
        return

    def _check_titles(self, table, titles=['int', 'str', 'float']):
        # Check data array names:
        self.assertEqual(table.GetColumnName(0), titles[0])
        self.assertEqual(table.GetColumnName(1), titles[1])
        self.assertEqual(table.GetColumnName(2), titles[2])
        return

    def _check_array_types(self, table, types=[int, float, float]):
        # Check data array types:
        typ = table.GetColumn(0).GetDataType()
        self.assertEqual(typ, nps.get_vtk_array_type(int))
        typ = table.GetColumn(1).GetDataType()
        self.assertEqual(typ, 13)
        typ = table.GetColumn(2).GetDataType()
        self.assertEqual(typ, nps.get_vtk_array_type(float))
        return

    def _check_array_values(self, table):
        # Check data array values:
        wt = dsa.WrapDataObject(table)
        arr = wt.RowData[0]
        self.assertEqual(arr[0], 5)
        self.assertEqual(arr[1], 1)
        self.assertEqual(arr[2], 3)
        arr = table.GetColumn(1)
        self.assertEqual(arr.GetValue(0), 'foo')
        self.assertEqual(arr.GetValue(1), 'bar')
        self.assertEqual(arr.GetValue(2), 'oof')
        arr = wt.RowData[2]
        self.assertEqual(arr[0], 6.9)
        self.assertEqual(arr[1], 8.5)
        self.assertEqual(arr[2], 7.7)
        return


    # TODO: check timesteps!


    def test_comma_read(self):
        """`DelimitedTextReader`: comma delimited file"""
        reader = DelimitedTextReader()
        reader.AddFileName(self.commafname)
        reader.SetDelimiter(',')
        reader.SetSkipRows(1)
        reader.SetComments('!')
        reader.Update()
        table = reader.GetOutput()
        self._check_shape(table)
        self._check_titles(table)
        self._check_array_types(table)
        self._check_array_values(table)
        return

    def test_tab_read(self):
        """`DelimitedTextReader`: tab delimited file"""
        reader = DelimitedTextReader()
        reader.AddFileName(self.tabfname)
        reader.SetUseTab(True)
        reader.SetSkipRows(1)
        reader.SetComments('!')
        reader.Update()
        table = reader.GetOutput()
        self._check_shape(table)
        self._check_titles(table)
        self._check_array_types(table)
        self._check_array_values(table)
        return

    def test_no_titles(self):
        """`DelimitedTextReader`: file without headers"""
        reader = DelimitedTextReader()
        reader.AddFileName(self.commafname)
        reader.SetDelimiter(',')
        reader.SetSkipRows(2)
        reader.SetHasTitles(False)
        reader.SetComments('!')
        reader.Update()
        table = reader.GetOutput()
        self._check_shape(table)
        self._check_titles(table, titles=['Field 0', 'Field 1', 'Field 2'])
        self._check_array_types(table)
        self._check_array_values(table)
        return





###############################################################################

class TestXYZTextReader(unittest.TestCase):
    """
    Test the `XYZTextReader`
    """
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.fname = os.path.join(self.test_dir, 'test.xyz')
        # Make a temporary file to test:
        self.nrows = 100
        self.ncols = 8 # LEAVE ALONE
        self.header = 'X, dx, Y, dy, Z, dz, approximate distance, cell index'
        self.data = np.random.random((self.nrows, self.ncols))
        np.savetxt(self.fname, self.data,
                   header=self.header,
                   comments='! ',
                   fmt='%.6e'
                   )
        reader = XYZTextReader()
        reader.AddFileName(self.fname)
        reader.Update()
        self.TABLE = reader.GetOutput()
        return

    def tearDown(self):
        # Remove the test data directory after the test
        shutil.rmtree(self.test_dir)

    ###########################################

    def test_data_aray_titles(self):
        """`XYZTextReader`: check data array names"""
        titles = self.header.split(', ')
        for i in range(self.ncols):
            self.assertEqual(self.TABLE.GetColumnName(i), titles[i])
        return

    def test_data_fidelity(self):
        """`XYZTextReader`: check data fidelity"""
        titles = self.header.split(', ')
        for i in range(self.ncols):
            arr = nps.vtk_to_numpy(self.TABLE.GetColumnByName(titles[i]))
            self.assertTrue(np.allclose(self.data[:,i], arr, rtol=RTOL))
        return

    def test_shape(self):
        """`XYZTextReader`: data table shape"""
        self.assertEqual(self.TABLE.GetNumberOfRows(), self.nrows)
        self.assertEqual(self.TABLE.GetNumberOfColumns(), self.ncols)
        return

###############################################################################


class TestPackedBinariesReader(unittest.TestCase):
    """
    Test the `PackedBinariesReader`
    """
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.n = 100
        return

    def tearDown(self):
        # Remove the test data directory after the test
        shutil.rmtree(self.test_dir)

    ###########################################

    def _check_data(self, table, data):
        arr = nps.vtk_to_numpy(table.GetColumn(0))
        self.assertTrue(np.allclose(data, arr, rtol=RTOL))
        return arr

    ###########################################

    def test_floats(self):
        """`PackedBinariesReader`: floats"""
        # Make data and write out
        dtype = np.dtype('f')
        arr = np.array(np.random.random(self.n), dtype=dtype)
        fname = os.path.join(self.test_dir, 'test.bin')
        arr.tofile(fname)
        # Set up reader
        reader = PackedBinariesReader()
        reader.AddFileName(fname)
        reader.SetDataType('f')
        reader.SetDataName('Test Data')
        # Perfrom Read
        reader.Update()
        table = reader.GetOutput()
        # Check output
        self.assertEqual(table.GetColumnName(0), 'Test Data')
        self._check_data(table, arr)
        return

    def test_doubles(self):
        """`PackedBinariesReader`: doubles"""
        # Make data and write out
        dtype = np.dtype('d')
        arr = np.array(np.random.random(self.n), dtype=dtype)
        fname = os.path.join(self.test_dir, 'test.bin')
        arr.tofile(fname)
        # Set up reader
        reader = PackedBinariesReader()
        reader.AddFileName(fname)
        reader.SetDataType('d')
        # Perfrom Read
        reader.Update()
        table = reader.GetOutput()
        # Check output
        self._check_data(table, arr)
        return

    def test_ints(self):
        """`PackedBinariesReader`: ints"""
        # Make data and write out
        dtype = np.dtype('i')
        arr = np.array(np.random.random(self.n), dtype=dtype)
        fname = os.path.join(self.test_dir, 'test.bin')
        arr.tofile(fname)
        # Set up reader
        reader = PackedBinariesReader()
        reader.AddFileName(fname)
        reader.SetDataType(2) # 'i' test that sending an int choice works
        # Perfrom Read
        reader.Update()
        table = reader.GetOutput()
        # Check output
        self._check_data(table, arr)
        return

    def test_endian_big(self):
        """`PackedBinariesReader`: floats with big-endianness"""
        # Make data and write out
        dtype = np.dtype('>f')
        arr = np.asarray(np.random.random(self.n), dtype=dtype)
        fname = os.path.join(self.test_dir, 'test.bin')
        arr.tofile(fname)
        # Set up reader
        reader = PackedBinariesReader()
        reader.AddFileName(fname)
        reader.SetDataType('f')
        reader.SetEndian('>')
        # Perfrom Read
        reader.Update()
        table = reader.GetOutput()
        # Check output
        self._check_data(table, arr)
        return

    def test_endian_little(self):
        """`PackedBinariesReader`: floats with little-endianness"""
        # Make data and write out
        dtype = np.dtype('<f')
        arr = np.array(np.random.random(self.n), dtype=dtype)
        fname = os.path.join(self.test_dir, 'test.bin')
        arr.tofile(fname)
        # Set up reader
        reader = PackedBinariesReader()
        reader.AddFileName(fname)
        reader.SetDataType('f')
        reader.SetEndian(1) # '<' test that sending an int choice works
        # Perfrom Read
        reader.Update()
        table = reader.GetOutput()
        # Check output
        self._check_data(table, arr)
        return

###############################################################################

class TestMadagascarReader(unittest.TestCase):
    """
    Test the `MadagascarReader`
    Does not test inherrited functionality
    """

    def tearDown(self):
        # Remove the test data directory after the test
        shutil.rmtree(self.test_dir)

    ###########################################

    def test_data_fidelity(self):
        """`MadagascarReader`: Check data fidelity"""
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.n = 100
        # Make data and write out
        dtype = np.dtype('f')
        self.data = np.array(np.random.random(self.n), dtype=dtype)
        fname = os.path.join(self.test_dir, 'test.rsf')
        # Write ascii header
        lines = ['hello\n']*10
        with open(fname, 'w') as f:
            f.writelines(lines)
        # Write data
        with open(fname, 'ab') as f:
            f.write(b'\014\014\004') # The control sequence
            self.data.tofile(f)
        # Set up reader
        reader = MadagascarReader()
        reader.AddFileName(fname)
        reader.SetDataType('f')
        reader.SetDataName('Test Data')
        self.assertEqual(reader.GetDataName(), 'Test Data')
        # Perfrom Read
        reader.Update()
        table = reader.GetOutput()
        arr = nps.vtk_to_numpy(table.GetColumn(0))
        self.assertTrue(np.allclose(self.data, arr))#, rtol=0.0001))
        self.assertEqual(table.GetColumnName(0), 'Test Data')
        return


###############################################################################


if __name__ == '__main__':
    unittest.main()
