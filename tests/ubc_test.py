from base import TestBase
import shutil
import tempfile
import os
import warnings
import numpy as np

# VTK imports:
from vtk.util import numpy_support as nps
from vtk.numpy_interface import dataset_adapter as dsa

# Functionality to test:
from PVGeo.ubc import *
import PVGeo

discretize_available = False
try:
    with PVGeo._helpers.HiddenPrints():
        import discretize
except ImportError:
    warnings.warn('`discretize` is NOT available. Be sure to install it.')
else:
    discretize_available = True

RTOL = 0.000001

###############################################################################

class ubcMeshTesterBase(TestBase):

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

class Test3DTensorMesh(ubcMeshTesterBase):
    """
    Test the `TensorMeshReader`, `TensorMeshAppender`, `TopoMeshAppender`, and  `WriteRectilinearGridToUBC` for 3D data
    """
    def _write_mesh(self):
        filename = os.path.join(self.test_dir, 'test.msh')
        with open(filename, 'w') as f:
            f.write('%d %d %d\n' % self.shape)
            f.write('%d %d %d\n' % self.origin)
            f.write('%s\n' % self.xCells)
            f.write('%s\n' % self.yCells)
            f.write('%s\n' % self.zCells)
        return filename

    def _write_model(self, filename='test.mod'):
        filename = os.path.join(self.test_dir, filename)
        model = np.random.random(self.n)
        np.savetxt(filename, model, delimiter=' ', comments='! ')
        model = np.reshape(model, self.shape)
        model = np.swapaxes(model,0,1)
        model = np.swapaxes(model,0,2)
        # Now reverse Z axis
        model = model[::-1,:,:] # Note it is in Fortran ordering
        model = model.flatten()
        return filename, model

    def _write_model_multi(self, filename='test.fld'):
        """writes a multi component model"""
        filename = os.path.join(self.test_dir, filename)
        model = np.random.random((self.n, 3))
        np.savetxt(filename, model, delimiter=' ', comments='! ')
        shp = self.shape
        model = np.reshape(model, (shp[0], shp[1], shp[2], 3) )
        model = np.swapaxes(model,0,1)
        model = np.swapaxes(model,0,2)
        # Now reverse Z axis
        model = model[::-1,:,:,:] # Note it is in Fortran ordering
        model = np.reshape(model, (shp[0]*shp[1]*shp[2], 3))
        return filename, model

    def setUp(self):
        TestBase.setUp(self)
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.origin = (-350, -400, 0)
        self.xCells = '200 100 50 20*50.0 50 100 200'
        self.yCells = '200 100 50 21*50.0 50 100 200'
        self.zCells = '20*25.0 50 100 200'
        self.shape = (26, 27, 23)
        self.n = self.shape[0]*self.shape[1]*self.shape[2]
        self.extent = (0, self.shape[0], 0, self.shape[1], 0, self.shape[2])
        self.data_name = 'foo'
        ##### Now generate output for testing ####
        # Produce data and write out files:
        self.meshname = self._write_mesh()
        self.modname, self.data = self._write_model()
        self.modname_multi, self.data_multi = self._write_model_multi()
        # Set up the reader:
        reader = TensorMeshReader()
        reader.set_mesh_filename(self.meshname)
        # Get and test output:
        reader.Update() # Read only mesh upfront
        reader.add_model_file_name(self.modname)
        reader.set_data_name(self.data_name)
        reader.Update() # Read models upfront
        self.GRID = reader.GetOutput()
        #### Now read mesh with multi component data
        # Set up the reader:
        reader = TensorMeshReader()
        reader.set_mesh_filename(self.meshname)
        # Get and test output:
        reader.Update() # Read only mesh upfront
        reader.add_model_file_name(self.modname_multi)
        reader.set_data_name(self.data_name)
        reader.Update() # Read models upfront
        self.GRID_MULTI = reader.GetOutput()

    def tearDown(self):
        # Remove the test data directory after the test
        shutil.rmtree(self.test_dir)
        TestBase.tearDown(self)

    ###########################################

    def test_grid_spatial_reference(self):
        """`TensorMeshReader` 3D: Spatial reference"""
        self._check_spatial_reference(self.GRID)
        self._check_spatial_reference(self.GRID_MULTI)

    def test_grid_shape(self):
        """`TensorMeshReader` 3D: Shape of output grid"""
        self._check_shape(self.GRID)
        self._check_shape(self.GRID_MULTI)

    def test_grid_data(self):
        """`TensorMeshReader` 3D: Data fidelity"""
        self._check_data(self.GRID, self.data)
        self._check_data(self.GRID_MULTI, self.data_multi)

    def test_grid_data_name(self):
        """`TensorMeshReader` 3D: Data array name"""
        self.assertEqual(self.GRID.GetCellData().GetArrayName(0), self.data_name)
        self.assertEqual(self.GRID_MULTI.GetCellData().GetArrayName(0), self.data_name)

    def test_model_appender(self):
        """`TensorMeshAppender` 3D: Data array name"""
        modname, appdata = self._write_model('testApp.mod')
        f = TensorMeshAppender()
        f.SetInputDataObject(self.GRID)
        f.add_model_file_name(modname)
        f.set_data_name('appended')
        f.Update()
        output = f.GetOutput()
        self.assertEqual(output.GetCellData().GetNumberOfArrays(), 2)
        self.assertEqual(output.GetCellData().GetArrayName(1), 'appended')

    def test_topo_appender(self):
        """`TopoMeshAppender` 3D:Test topography appender"""
        indices = np.array([[0,0,1], [0,1,1], [0,2,1], [1,0,1], [1,1,1],
            [1,2,1], [2,0,1], [2,1,1], [2,2,2], ], dtype=int)
        filename = os.path.join(self.test_dir, 'disc-topo.txt')
        np.savetxt(filename, X=indices, fmt='%d', comments='', header='3 3')
        # Create input grid
        grid = PVGeo.model_build.CreateTensorMesh(xcellstr='1.0 1.0 1.0',
                    ycellstr='1.0 1.0 1.0', zcellstr='1.0 1.0 1.0').apply()
        # run the filter
        f = TopoMeshAppender()
        f.SetInputDataObject(grid)
        f.set_topo_filename(filename)
        f.Update()
        output = f.GetOutput()
        # TODO: check output
        self.assertIsNotNone(output)


    def test_writer(self):
        """`WriteRectilinearGridToUBC`: Test data integretiy across I/O"""
        # Write known data back out using the writer:
        writer = WriteRectilinearGridToUBC()
        filename = os.path.join(self.test_dir, 'test-writer.msh')
        writer.SetFileName(filename)
        writer.Write(self.GRID)
        # Now read in the data again and compare!
        reader = TensorMeshReader()
        reader.set_mesh_filename(filename)
        modname = os.path.join(self.test_dir, '%s.mod' % self.data_name)
        reader.add_model_file_name(modname)
        reader.set_data_name(self.data_name)
        reader.Update()
        test = reader.GetOutput()
        # Compare the data
        self._check_shape(test)
        self._check_spatial_reference(test)
        self._check_data(test, self.data)
        self.assertEqual(test.GetCellData().GetArrayName(0), self.data_name)
        return

###############################################################################

class Test2DTensorMeshReader(ubcMeshTesterBase):
    """
    Test the `TensorMeshReader` and `TensorMeshAppender` for 2D data
    """

    def _write_mesh(self):
        filename = os.path.join(self.test_dir, 'test.msh')
        with open(filename, 'w') as f:
            f.write(self.mesh)
        return filename

    def _write_model(self, filename='test.mod'):
        filename = os.path.join(self.test_dir, filename)
        model = np.random.random((self.nz,self.nx))
        with open(filename, 'w') as f:
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
        return filename, model

    def setUp(self):
        TestBase.setUp(self)
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
        self.data_name = 'foo'
        ##### Now generate output for testing ####
        # Produce data and write out files:
        meshname = self._write_mesh()
        modname, self.data = self._write_model()
        # Set up the reader:
        reader = TensorMeshReader()
        reader.set_mesh_filename(meshname)
        # Get and test output:
        reader.Update() # Test the read up front for the mesh
        reader.add_model_file_name(modname)
        reader.set_data_name(self.data_name)
        reader.Update() # Now read the models upfront
        self.GRID = reader.GetOutput()
        return

    def tearDown(self):
        # Remove the test data directory after the test
        shutil.rmtree(self.test_dir)
        TestBase.tearDown(self)

    ###########################################

    def test_grid_spatial_reference(self):
        """`TensorMeshReader` 2D: Spatial reference"""
        self._check_spatial_reference(self.GRID)

    def test_grid_shape(self):
        """`TensorMeshReader` 2D: Shape of output grid"""
        self._check_shape(self.GRID)

    def test_grid_data(self):
        """`TensorMeshReader` 2D: Data fidelity"""
        self._check_data(self.GRID, self.data)

    def test_grid_data_name(self):
        """`TensorMeshReader` 2D: Data array name"""
        self.assertEqual(self.GRID.GetCellData().GetArrayName(0), self.data_name)

    def test_model_appender(self):
        """`TensorMeshAppender` 2D: Data array name"""
        modname, appdata = self._write_model('testApp.mod')
        f = TensorMeshAppender()
        f.SetInputDataObject(self.GRID)
        f.add_model_file_name(modname)
        f.set_data_name('appended')
        f.Update()
        output = f.GetOutput()
        self.assertEqual(output.GetCellData().GetNumberOfArrays(), 2)
        self.assertEqual(output.GetCellData().GetArrayName(1), 'appended')


###############################################################################

if discretize_available:
    class TestOcTreeMeshReader(ubcMeshTesterBase):
        """
        Test the `OcTreeReader`
        """

        def setUp(self):
            TestBase.setUp(self)
            self.test_dir = tempfile.mkdtemp()
            treeMesh = """16 16 16
0.0000 0.0000 48.0000
1.000 2.000 3.000
29
1 1 1 8
9 1 1 8
1 9 1 8
9 9 1 8
1 1 9 4
5 1 9 4
9 1 9 8
1 5 9 4
5 5 9 4
1 9 9 8
9 9 9 8
1 1 13 2
3 1 13 2
5 1 13 4
1 3 13 2
3 3 13 2
1 5 13 4
5 5 13 4
1 1 15 1
2 1 15 1
3 1 15 2
1 2 15 1
2 2 15 1
1 3 15 2
3 3 15 2
1 1 16 1
2 1 16 1
1 2 16 1
2 2 16 1
"""
            # Write out mesh file
            filename = os.path.join(self.test_dir, 'octree.msh')
            self.meshFileName = filename
            with open(filename, 'w') as f:
                f.write(treeMesh)


            # write out model file(s)
            self.nt = 5
            self.modelFileNames = ['model%d.mod' % i for i in range(self.nt)]
            self.modelFileNames = [os.path.join(self.test_dir, self.modelFileNames[i]) for i in range(self.nt)]
            self.arrs = [None] * self.nt
            for i in range(self.nt):
                self.arrs[i] = np.random.random(29)
                np.savetxt(self.modelFileNames[i], self.arrs[i], delimiter=' ', comments='! ')
            return

        def tearDown(self):
            # Remove the test data directory after the test
            shutil.rmtree(self.test_dir)
            TestBase.tearDown(self)

        def reshapeArrs(self, mesh):
            for i in range(self.nt):
                ind_reorder = nps.vtk_to_numpy(
                    mesh.GetCellData().GetArray('index_cell_corner'))
                self.arrs[i] = self.arrs[i][ind_reorder]

        def test_simple_octree(self):
            """`OcTreeReader`: simple octree mesh file"""
            reader = OcTreeReader()
            reader.set_mesh_filename(self.meshFileName)

            reader.Update()

            tree = reader.GetOutput()
            self.assertIsNotNone(tree)
            self.assertEqual(tree.GetNumberOfCells(), 29)
            self.assertEqual(tree.GetNumberOfPoints(), 84)

        def test_simple_octree_models(self):
            """`OcTreeReader`: simple octree mesh with models"""
            reader = OcTreeReader()
            reader.set_mesh_filename(self.meshFileName)
            reader.add_model_file_name(self.modelFileNames)
            reader.set_data_name('foo')

            reader.Update() # Check that normal update works

            tree = reader.GetOutputDataObject(0)
            self.assertIsNotNone(tree)
            self.assertEqual(tree.GetNumberOfCells(), 29)
            self.assertEqual(tree.GetNumberOfPoints(), 84)

            self.reshapeArrs(tree)

            wtree = dsa.WrapDataObject(tree)
            # Now check time series
            for i in range(self.nt):
                reader.UpdateTimeStep(i)
                arr = wtree.CellData['foo']
                self.assertTrue(np.allclose(arr, self.arrs[i], rtol=RTOL))

            return

        def test_model_appender(self):
            """`OcTreeAppender` 2D: Data array name"""
            # Creat a tree mesh to append
            reader = OcTreeReader()
            reader.set_mesh_filename(self.meshFileName)
            reader.add_model_file_name(self.modelFileNames[0])
            reader.set_data_name('Initial Data')
            reader.Update()
            tree = reader.GetOutput()
            self.assertIsNotNone(tree)
            self.assertEqual(tree.GetNumberOfCells(), 29)
            self.assertEqual(tree.GetNumberOfPoints(), 84)

            # Now use the model appender
            f = OcTreeAppender()
            f.SetInputDataObject(tree)
            f.add_model_file_name(self.modelFileNames[1::])
            f.set_data_name('Appended Data')
            f.Update()

            output = f.GetOutput()
            # remember that 2 arrays is added by the reader
            self.assertEqual(output.GetCellData().GetNumberOfArrays(), 4)
            self.assertEqual(output.GetCellData().GetArrayName(3), os.path.basename(self.modelFileNames[1])) # use file as name
            self.assertEqual(len(f.get_time_step_values()), self.nt-1)
            return

###############################################################################
###############################################################################
###############################################################################
if __name__ == '__main__':
    import unittest
    unittest.main()
###############################################################################
###############################################################################
###############################################################################
