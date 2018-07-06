import unittest
import numpy as np

# VTK imports:
import vtk
from vtk.util import numpy_support as nps
from vtk.numpy_interface import dataset_adapter as dsa

# Functionality to test:
from .reverse_axii import *
from .table2grid import *
from .trans_origin import *

RTOL = 0.000001

#
# ###############################################################################
#
# class TestTableToGrid(unittest.TestCase):
#     """
#     Test the `TableToGrid` filter
#     """
#
#     def test_(self):
#         self.assertTrue(False)
#
#
###############################################################################

class TestReverseImageDataAxii(unittest.TestCase):
    """
    Test the `ReverseImageDataAxii` filter
    """

    def test(self):
        """`ReverseImageDataAxii`: check that it works on point and cell data"""
        # Create input vtkImageData:
        nx, ny, nz = 10, 11, 12
        arr = np.random.random((nz, ny, nx))
        arrCells = np.random.random((nz-1, ny-1, nx-1))
        image = vtk.vtkImageData()
        image.SetDimensions(nx, ny, nz)
        image.SetSpacing(2, 2, 2)
        image.SetOrigin(0, 0, 0)
        data = nps.numpy_to_vtk(num_array=arr.flatten(), deep=True)
        data.SetName('Data')
        cellData = nps.numpy_to_vtk(num_array=arrCells.flatten(), deep=True)
        cellData.SetName('CellData')
        image.GetPointData().AddArray(data)
        image.GetCellData().AddArray(cellData)
        # Now perfrom the reverse for only X:
        f = ReverseImageDataAxii()
        f.SetInputDataObject(image)
        f.SetFlipX(True)
        f.SetFlipY(False)
        f.SetFlipZ(False)
        f.Update()
        ido = f.GetOutput()
        self.assertIsNotNone(ido)
        self.assertEqual(ido.GetNumberOfPoints(), len(arr.flatten()))
        # Check that x-axis was reversed
        wido = dsa.WrapDataObject(ido)
        test = wido.PointData['Data']
        testCells = wido.CellData['CellData']
        self.assertTrue(np.allclose(test, np.flip(arr, axis=2).flatten(), rtol=RTOL))
        self.assertTrue(np.allclose(testCells, np.flip(arrCells, axis=2).flatten(), rtol=RTOL))
        # Now perfrom the reverse for all axii:
        f.SetFlipX(True)
        f.SetFlipY(True)
        f.SetFlipZ(True)
        f.Update()
        ido = f.GetOutput()
        self.assertIsNotNone(ido)
        self.assertEqual(ido.GetNumberOfPoints(), len(arr.flatten()))
        # Check that x-axis was reversed
        wido = dsa.WrapDataObject(ido)
        test = wido.PointData['Data']
        testCells = wido.CellData['CellData']
        tarr = np.flip(arr, axis=0)
        tarr = np.flip(tarr, axis=1)
        tarr = np.flip(tarr, axis=2)
        tarrCells = np.flip(arrCells, axis=0)
        tarrCells = np.flip(tarrCells, axis=1)
        tarrCells = np.flip(tarrCells, axis=2)
        self.assertTrue(np.allclose(test, tarr.flatten(), rtol=RTOL))
        self.assertTrue(np.allclose(testCells, tarrCells.flatten(), rtol=RTOL))


# ###############################################################################
#
# class TestTranslateGridOrigin(unittest.TestCase):
#     """
#     Test the `TranslateGridOrigin` filter
#     """
#
#     def test_(self):
#         self.assertTrue(False)
#
#
# ###############################################################################
