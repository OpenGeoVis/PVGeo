import unittest
import warnings
import shutil
import tempfile
import os
import numpy as np

# VTK imports:
from vtk.util import numpy_support as nps
from vtk.numpy_interface import dataset_adapter as dsa

from .. import _helpers
# Functionality to test:
from .gslib import *
from .sgems import *
from .write import *


RTOL = 0.000001

###############################################################################

class TestGSLibReader(unittest.TestCase):
    """
    Test the `GSLibReader` and `WriteTableToGSLib`
    """
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.n = 100
        self.titles = ['Array 1', 'Array 2', 'Array 3']
        self.header = 'A header line'
        ##### Now generate output for testing ####
        fname = os.path.join(self.test_dir, 'test.dat')
        self.data = np.random.random((self.n, len(self.titles)))
        header = [self.header, '%d' % len(self.titles)]
        for ln in self.titles:
            header.append(ln + '\n')
        header = '\n'.join(header)
        np.savetxt(fname, self.data, delimiter=' ', header=header, comments='')
        # Set up the reader
        reader = GSLibReader()
        reader.AddFileName(fname)
        # Perform the read
        reader.Update()
        self.HEADER = reader.GetFileHeader()
        self.TABLE = reader.GetOutput()

    def tearDown(self):
        # Remove the test data directory after the test
        shutil.rmtree(self.test_dir)

    ###########################################

    def test_data_array_titles(self):
        """`GSLibReader`: data array names"""
        for i in range(len(self.titles)):
            self.assertEqual(self.TABLE.GetColumnName(i), self.titles[i])
        return

    def test_data_fidelity(self):
        """`GSLibReader`: data fidelity"""
        for i in range(len(self.titles)):
            arr = nps.vtk_to_numpy(self.TABLE.GetColumn(i))
            self.assertTrue(np.allclose(self.data[:,i], arr, rtol=RTOL))
        return

    def test_header_catch(self):
        """`GSLibReader`: check header caught by reader"""
        self.assertEqual(self.HEADER, self.header)
        return

    def test_bad_file(self):
        """`GSLibReader`: check handling of bad input file"""
        fname = os.path.join(self.test_dir, 'test_bad.dat')
        header = ['A header line', 'Bad number of titles']
        for ln in self.titles:
            header.append(ln + '\n')
        header = '\n'.join(header)
        np.savetxt(fname, self.data, delimiter=' ', header=header, comments='')
        # Set up the reader
        reader = GSLibReader()
        reader.AddFileName(fname)
        # Perform the read
        reader.Update()
        self.assertTrue(reader.ErrorOccurred())

    def test_writer(self):
        """`WriteTableToGSLib`: check data integrity across I/O"""
        writer = WriteTableToGSLib()
        fname = os.path.join(self.test_dir, 'test-writer.dat')
        writer.SetFileName(fname)
        writer.Write(self.TABLE)
        # Now read that data and compare
        reader = GSLibReader()
        read = reader.Apply(fname)
        # Compare data
        truedata = self.TABLE.GetRowData()
        testdata = read.GetRowData()
        self.assertEqual(truedata.GetNumberOfArrays(), testdata.GetNumberOfArrays())
        #self.assertEqual(truedata.GetNumberOfRows(), testdata.GetNumberOfRows())
        #self.assertEqual(truedata.GetNumberOfColumns(), testdata.GetNumberOfColumns())
        wtbl = dsa.WrapDataObject(self.TABLE)
        wrd = dsa.WrapDataObject(read)
        for i in range(truedata.GetNumberOfArrays()):
            self.assertIsNotNone(wtbl.RowData[i])
            self.assertIsNotNone(wrd.RowData[i])
            self.assertTrue(np.allclose(wtbl.RowData[i], wrd.RowData[i]))




###############################################################################


class TestSGeMSGridReader(unittest.TestCase):
    """
    Test the `SGeMSGridReader` and `WriteImageDataToSGeMS`
    """
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.n = 100
        self.shape = (150, 200, 20)
        self.extent = (0, self.shape[0]-1, 0, self.shape[1]-1, 0, self.shape[2]-1)
        self.titles = ['Array 1', 'Array 2', 'Array 3']
        ##### Now generate output for testing ####
        fname = os.path.join(self.test_dir, 'test.dat')
        self.data = np.random.random((self.n, len(self.titles)))
        header = ['%d %d %d' % self.shape, '%d' % len(self.titles)]
        for ln in self.titles:
            header.append(ln + '\n')
        header = '\n'.join(header)
        np.savetxt(fname, self.data, delimiter=' ', header=header, comments='')
        # Set up the reader
        self.GRID = SGeMSGridReader().Apply(fname)

    def tearDown(self):
        # Remove the test data directory after the test
        shutil.rmtree(self.test_dir)

    ###########################################

    def test_data_array_titles(self):
        """`SGeMSGridReader`: data array titles"""
        for i in range(len(self.titles)):
            self.assertEqual(self.GRID.GetPointData().GetArrayName(i), self.titles[i])
        return

    def test_shape(self):
        """`SGeMSGridReader`: check output grid shape"""
        self.assertEqual(self.GRID.GetExtent(), self.extent)
        self.assertEqual(self.GRID.GetNumberOfCells(), self.extent[1]*self.extent[3]*self.extent[5])
        return

    def test_data(self,):
        """`SGeMSGridReader`: data fidelity"""
        for i in range(len(self.titles)):
            arr = nps.vtk_to_numpy(self.GRID.GetPointData().GetArray(i))
            self.assertTrue(np.allclose(self.data[:,i], arr, rtol=RTOL))
        return

    def test_bad_file(self):
        """`SGeMSGridReader`: check handling of bad input file"""
        fname = os.path.join(self.test_dir, 'test_bad.dat')
        header = ['Bad header', '%d' % len(self.titles)]
        for ln in self.titles:
            header.append(ln + '\n')
        header = '\n'.join(header)
        np.savetxt(fname, self.data, delimiter=' ', header=header, comments='')
        # Set up the reader
        reader = SGeMSGridReader()
        reader.AddFileName(fname)
        # Perform the read
        reader.Update()
        self.assertTrue(reader.ErrorOccurred())


    def test_writer(self):
        """`WriteImageDataToSGeMS`: check data integrity across I/O"""
        writer = WriteImageDataToSGeMS()
        fname = os.path.join(self.test_dir, 'test-writer.dat')
        writer.SetFileName(fname)
        writer.Write(self.GRID)
        # Now read that data and compare
        reader = SGeMSGridReader()
        read = reader.Apply(fname)
        # Compare data
        truedata = self.GRID.GetPointData()
        testdata = read.GetPointData()
        self.assertEqual(truedata.GetNumberOfArrays(), testdata.GetNumberOfArrays())
        wtbl = dsa.WrapDataObject(self.GRID)
        wrd = dsa.WrapDataObject(read)
        for i in range(truedata.GetNumberOfArrays()):
            self.assertIsNotNone(wtbl.PointData[i])
            self.assertIsNotNone(wrd.PointData[i])
            self.assertTrue(np.allclose(wtbl.PointData[i], wrd.PointData[i]))
        for i in range(self.GRID.GetCellData().GetNumberOfArrays()):
            self.assertIsNotNone(wtbl.CellData[i])
            self.assertIsNotNone(wrd.CellData[i])
            self.assertTrue(np.allclose(wtbl.CellData[i], wrd.CellData[i]))
