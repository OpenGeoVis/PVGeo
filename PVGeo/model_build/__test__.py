import unittest
import numpy as np

# VTK imports:
import vtk
from vtk.util import numpy_support as nps
from vtk.numpy_interface import dataset_adapter as dsa

# Functionality to test:
from .earth import *
from .evenModel import *
from .oddModel import *

###############################################################################

class TestEarthSource(unittest.TestCase):
    """
    Test the `EarthSource` source
    """

    def test_generation(self):
        """`EarthSource`: make sure works."""
        s = EarthSource()
        s.SetRadius(6000.0)
        s.Update()
        e = s.GetOutput()
        self.assertIsNotNone(e)
        self.assertTrue(isinstance(e, vtk.vtkPolyData))
        return


###############################################################################

class TestCreateUniformGrid(unittest.TestCase):
    """
    Test the `CreateUniformGrid` source
    """

    def test_generation(self):
        """`CreateUniformGrid`: make sure works."""
        g = CreateUniformGrid()
        g.SetExtent(20, 10, 35)
        g.SetOrigin(33.3, 45.5, 6.6)
        g.SetSpacing(5,1,7)
        g.Update()
        grid = g.GetOutput()
        self.assertIsNotNone(grid)
        self.assertEqual(grid.GetNumberOfCells(), (19*9*34))
        self.assertEqual(grid.GetNumberOfPoints(), (20*10*35))
        bounds = grid.GetBounds()
        tb = (33.3, 33.3+(19*5), 45.5, 45.5+(9*1), 6.6, 6.6+(34*7))
        self.assertEqual(bounds, tb)
        return


###############################################################################

class TestCreateEvenRectilinearGrid(unittest.TestCase):
    """
    Test the `CreateEvenRectilinearGrid` source
    """

    def test_generation(self):
        """`CreateEvenRectilinearGrid`: make sure works."""
        g = CreateEvenRectilinearGrid()
        g.SetExtent(20, 10, 35)
        g.SetXRange(0, 100)
        g.SetYRange(-100, 0)
        g.SetZRange(10, 50)
        g.Update()
        grid = g.GetOutput()
        self.assertIsNotNone(grid)
        self.assertEqual(grid.GetNumberOfCells(), (20*10*35))
        self.assertEqual(grid.GetNumberOfPoints(), (21*11*36))
        bounds = grid.GetBounds()
        tb = (0, 100, -100, 0, 10, 50)
        self.assertEqual(bounds, tb)


###############################################################################

class TestCreateTensorMesh(unittest.TestCase):
    """
    Test the `CreateTensorMesh` source
    """

    def test_generation(self):
        """`CreateTensorMesh`: make sure works."""
        g = CreateTensorMesh()
        g.SetXCellsStr('200 100 50 30*50.0 50 100 200')
        g.SetYCellsStr('200 100 50 25*50.0 50 100 200')
        g.SetZCellsStr('25*25.0 50 100 200')
        g.SetOrigin(-300.0, -450.0, 10.0)
        g.Update()
        grid = g.GetOutput()
        self.assertIsNotNone(grid)
        self.assertEqual(grid.GetNumberOfCells(), (36*31*28))
        bounds = grid.GetBounds()
        tb = (-300.0, 1900, -450, 1500, -965, 10)
        self.assertEqual(bounds, tb)


###############################################################################
