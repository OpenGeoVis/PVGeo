import unittest
import shutil
import tempfile
import os
import numpy as np

# VTK imports:
from vtk.util import numpy_support as nps
from vtk.numpy_interface import dataset_adapter as dsa

# Functionality to test:
from .tensor_mesh import *

RTOL = 0.000001

###############################################################################

class ubcMeshTesterBase(unittest.TestCase):

    def _check_shape(self, grid):
        self.assertEqual(grid.GetExtent(), self.extent)
        self.assertEqual(grid.GetNumberOfCells(), self.extent[1]*self.extent[3]*self.extent[5])
        return

    def _check_data(self, grid, data):
        arr = nps.vtk_to_numpy(grid.GetCellData().GetArray(0))
        self.assertTrue(np.allclose(data, arr, rtol=RTOL))
        return

    def _check_spatial_reference(self, grid):
        bounds = grid.GetBounds()
        corner = (bounds[0], bounds[2], bounds[5])
        self.assertEqual(corner, self.origin)
        return

###############################################################################

class Test3DTensorMeshReader(ubcMeshTesterBase):
    """
    Test the `ubcTensorMeshReader` for 3D data
    """
    def _write_mesh(self):
        fname = os.path.join(self.test_dir, 'test.msh')
        with open(fname, 'w') as f:
            f.write('%d %d %d\n' % self.shape)
            f.write('%d %d %d\n' % self.origin)
            f.write('%s\n' % self.xCells)
            f.write('%s\n' % self.yCells)
            f.write('%s\n' % self.zCells)
        return fname

    def _write_model(self):
        fname = os.path.join(self.test_dir, 'test.mod')
        model = np.random.random(self.n)
        np.savetxt(fname, model, delimiter=' ', comments='! ')
        model = np.reshape(model, self.shape)
        model = np.swapaxes(model,0,1)
        model = np.swapaxes(model,0,2)
        # Now reverse Z axis
        model = model[::-1,:,:] # Note it is in Fortran ordering
        model = model.flatten()
        return fname, model

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.origin = (-350, -400, 0)
        self.xCells = '200 100 50 20*50.0 50 100 200'
        self.yCells = '200 100 50 21*50.0 50 100 200'
        self.zCells = '20*25.0 50 100 200'
        self.shape = (26, 27, 23)
        self.n = self.shape[0]*self.shape[1]*self.shape[2]
        self.extent = (0, self.shape[0], 0, self.shape[1], 0, self.shape[2])
        self.dataName = 'foo'
        ##### Now generate output for testing ####
        # Produce data and write out files:
        meshname = self._write_mesh()
        modname, self.data = self._write_model()
        # Set up the reader:
        reader = ubcTensorMeshReader()
        reader.SetMeshFileName(meshname)
        reader.AddModelFileName(modname)
        reader.SetDataName(self.dataName)
        # Get and test output:
        reader.Update()
        self.GRID = reader.GetOutputDataObject(0)

    def tearDown(self):
        # Remove the test data directory after the test
        shutil.rmtree(self.test_dir)

    ###########################################

    def test_grid_spatial_reference(self):
        """Test 3D `ubcTensorMeshReader`: Spatial reference"""
        self._check_spatial_reference(self.GRID)

    def test_grid_shape(self):
        """Test 3D `ubcTensorMeshReader`: Shape of output grid"""
        self._check_shape(self.GRID)

    def test_grid_data(self):
        """Test 3D `ubcTensorMeshReader`: Data fidelity"""
        self._check_data(self.GRID, self.data)

    def test_grid_data_name(self):
        """Test 3D `ubcTensorMeshReader`: Data array name"""
        self.assertEqual(self.GRID.GetCellData().GetArrayName(0), self.dataName)

###############################################################################

class Test2DTensorMeshReader(ubcMeshTesterBase):
    """
    Test the `ubcTensorMeshReader` for 2D data
    """

    def _write_mesh(self):
        fname = os.path.join(self.test_dir, 'test.msh')
        with open(fname, 'w') as f:
            f.write(self.mesh)
        return fname

    def _write_model(self):
        fname = os.path.join(self.test_dir, 'test.mod')
        model = np.random.random((self.nz,self.nx))
        with open(fname, 'w') as f:
            f.write('%d %d\n' % (self.nx, self.nz))
            for k in range(self.nz):
                for i in range(self.nx):
                    f.write('%.6e ' % model[k,i])
                f.write('\n')
            f.close()
        model = np.reshape(model.flatten(order='F'), self.shape)
        model = np.swapaxes(model,0,1)
        model = np.swapaxes(model,0,2)
        # Now reverse Z axis
        model = model[::-1,:,:] # Note it is in Fortran ordering
        model = model.flatten()
        return fname, model

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.mesh = """9
 -300.0   -180.0     1
          -130.0     1
          -110.0     1
          -100.0     1
           100.0    40
           110.0     1
           130.0     1
           180.0     1
           300.0     1
14
 -10.0      10.0     5
            22.0     4
            42.0     5
            57.0     3
            63.0     1
            71.0     1
            81.0     1
            95.0     1
           115.0     1
           140.0     1
           170.0     1
           205.0     1
           245.0     1
           300.0     1
"""
        self.origin = (-300, 0, 10)
        self.nx = 48
        self.nz = 27
        self.shape = (self.nx, 1, self.nz)
        self.extent = (0, self.shape[0], 0, self.shape[1], 0, self.shape[2])
        self.dataName = 'foo'
        ##### Now generate output for testing ####
        # Produce data and write out files:
        meshname = self._write_mesh()
        modname, self.data = self._write_model()
        # Set up the reader:
        reader = ubcTensorMeshReader()
        reader.SetMeshFileName(meshname)
        reader.AddModelFileName(modname)
        reader.SetDataName(self.dataName)
        # Get and test output:
        reader.Update()
        self.GRID = reader.GetOutputDataObject(0)
        return

    def tearDown(self):
        # Remove the test data directory after the test
        shutil.rmtree(self.test_dir)

    ###########################################

    def test_grid_spatial_reference(self):
        """Test 2D `ubcTensorMeshReader`: Spatial reference"""
        self._check_spatial_reference(self.GRID)

    def test_grid_shape(self):
        """Test 2D `ubcTensorMeshReader`: Shape of output grid"""
        self._check_shape(self.GRID)

    def test_grid_data(self):
        """Test 2D `ubcTensorMeshReader`: Data fidelity"""
        self._check_data(self.GRID, self.data)

    def test_grid_data_name(self):
        """Test `ubcTensorMeshReader`: Data array name"""
        self.assertEqual(self.GRID.GetCellData().GetArrayName(0), self.dataName)

###############################################################################


if __name__ == '__main__':
    unittest.main()
