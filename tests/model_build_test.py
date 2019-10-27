import vtk

from base import TestBase
# Functionality to test:
from PVGeo.model_build import (CreateEvenRectilinearGrid, CreateTensorMesh,
                               CreateUniformGrid, GlobeSource,
                               OutlineContinents)

###############################################################################

class TestOutlineContinents(TestBase):
    """
    Test the `OutlineContinents` source
    """

    def test_generation(self):
        """`OutlineContinents`: make sure works."""
        s = OutlineContinents()
        s.set_radius(6000.0)
        s.Update()
        e = s.GetOutput()
        self.assertIsNotNone(e)
        self.assertTrue(isinstance(e, vtk.vtkPolyData))
        return


###############################################################################


class TestGlobeSource(TestBase):
    """
    Test the `GlobeSource` source
    """

    def test_generation(self):
        """`GlobeSource`: make sure works."""
        s = GlobeSource()
        s.set_radius(6000.0)
        s.Update()
        e = s.GetOutput()
        self.assertIsNotNone(e)
        self.assertTrue(isinstance(e, vtk.vtkPolyData))
        return


###############################################################################

class TestCreateUniformGrid(TestBase):
    """
    Test the `CreateUniformGrid` source
    """

    def test_generation(self):
        """`CreateUniformGrid`: make sure works."""
        g = CreateUniformGrid()
        g.set_extent(20, 10, 35)
        g.set_origin(33.3, 45.5, 6.6)
        g.set_spacing(5,1,7)
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

class TestCreateEvenRectilinearGrid(TestBase):
    """
    Test the `CreateEvenRectilinearGrid` source
    """

    def test_generation(self):
        """`CreateEvenRectilinearGrid`: make sure works."""
        g = CreateEvenRectilinearGrid()
        g.set_extent(20, 10, 35)
        g.set_x_range(0, 100)
        g.set_y_range(-100, 0)
        g.set_z_range(10, 50)
        g.Update()
        grid = g.GetOutput()
        self.assertIsNotNone(grid)
        self.assertEqual(grid.GetNumberOfCells(), (20*10*35))
        self.assertEqual(grid.GetNumberOfPoints(), (21*11*36))
        bounds = grid.GetBounds()
        tb = (0, 100, -100, 0, 10, 50)
        self.assertEqual(bounds, tb)


###############################################################################

class TestCreateTensorMesh(TestBase):
    """
    Test the `CreateTensorMesh` source
    """

    def test_generation(self):
        """`CreateTensorMesh`: make sure works."""
        g = CreateTensorMesh()
        g.set_x_cells_str('200 100 50 30*50.0 50 100 200')
        g.set_y_cells_str('200 100 50 25*50.0 50 100 200')
        g.set_z_cells_str('25*25.0 50 100 200')
        g.set_origin(-300.0, -450.0, 10.0)
        g.Update()
        grid = g.GetOutput()
        self.assertIsNotNone(grid)
        self.assertEqual(grid.GetNumberOfCells(), (36*31*28))
        bounds = grid.GetBounds()
        tb = (-300.0, 1900, -450, 1500, -965, 10)
        self.assertEqual(bounds, tb)


###############################################################################


###############################################################################
###############################################################################
###############################################################################
if __name__ == '__main__':
    import unittest
    unittest.main()
###############################################################################
###############################################################################
###############################################################################
