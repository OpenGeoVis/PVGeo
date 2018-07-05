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
        """`CombineTables`: table shape"""
        self.assertEqual(self.TABLE.GetNumberOfColumns(), len(self.titles))
        self.assertEqual(self.TABLE.GetNumberOfRows(), self.n)

    def test_data_array_names(self):
        """`CombineTables`: data array names"""
        for i in range(len(self.titles)):
            self.assertEqual(self.TABLE.GetColumnName(i), self.titles[i])

    def test_data_fidelity(self):
        """`CombineTables`: data fidelity"""
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
        """`ReshapeTable`: F-order, no input names"""
        order = 'F'
        table = self._generate_output(order, titles=None)
        # Check output:
        self._check_shape(table)
        self._check_data_fidelity(table, order)
        self._check_data_array_titles(table, ['Field %d' % i for i in range(self.ncols)])
        return

    def test_reshape_f_names(self):
        """`ReshapeTable`: F-order, input names given"""
        order = 'F'
        titles = ['Title %d' % i for i in range(self.ncols)]
        table = self._generate_output(order, titles=titles)
        # Check output:
        self._check_shape(table)
        self._check_data_fidelity(table, order)
        self._check_data_array_titles(table, titles)
        return


    def test_reshape_c(self):
        """`ReshapeTable`: C-order, no input names"""
        order = 'C'
        table = self._generate_output(order, titles=None)
        # Check output:
        self._check_shape(table)
        self._check_data_fidelity(table, order)
        self._check_data_array_titles(table, ['Field %d' % i for i in range(self.ncols)])
        return

    def test_reshape_c_names(self):
        """`ReshapeTable`: C-order, input names given"""
        order = 'C'
        titles = ['Title %d' % i for i in range(self.ncols)]
        table = self._generate_output(order, titles=titles)
        # Check output:
        self._check_shape(table)
        self._check_data_fidelity(table, order)
        self._check_data_array_titles(table, titles)
        return




###############################################################################

ROTATED_TEXT = """326819.497,4407450.636,1287.5
326834.34,4407470.753,1287.5
326849.183,4407490.87,1287.5
326864.027,4407510.986,1287.5
326878.87,4407531.103,1287.5
326893.713,4407551.22,1287.5
326908.556,4407571.336,1287.5
326923.399,4407591.453,1287.5
326938.242,4407611.57,1287.5
326953.086,4407631.686,1287.5"""

ROTATED_POINTS = np.genfromtxt((line.encode('utf8') for line in ROTATED_TEXT.split('\n')), delimiter=',''', dtype=float)

class TestRotationTool(unittest.TestCase):
    """
    Test the `RotationTool` filter
    """
    # An example voxel:
    # voxel = np.array([
    #     [0,0,0],
    #     [0,0,1],
    #     [0,1,1],
    #     [1,1,1],
    #     [0,1,0],
    #     [1,0,0],
    #     [1,1,0],
    # ])

    def setUp(self):
        # Create some input tables
        self.RTOL = 0.00001 # As higi as rotation precision can get
        return


    def test_recovery(self):
        """`RotationTool`: Test a simple rotation recovery"""
        r = RotationTool()
        # Input points
        x = np.array([1.1, 1.1, 1.1, 2.1, 2.1, 2.1])
        y = np.array([1.0, 2.0, 3.0, 1.0, 2.0, 3.0])
        z = np.zeros(len(x))
        x = np.reshape(x, (len(x), -1))
        y = np.reshape(y, (len(y), -1))
        z = np.reshape(z, (len(z), -1))
        pts = np.concatenate((x,y,z), axis=1)
        rot = np.deg2rad(-33.3)
        pts[:, 0:2] = r.Rotate(pts[:, 0:2], rot)
        xx, yy, zz, dx, dy, angle = r.EstimateAndRotate(pts[:,0], pts[:,1], pts[:,2])
        rpts = np.vstack((xx,yy,zz)).T
        self.assertTrue(np.allclose(angle, np.deg2rad(33.3), rtol=RTOL), msg='Recovered angle is incorrect.')
        self.assertTrue(np.allclose(dx, 1.0, rtol=RTOL), msg='Recovered x-spacing is incorrect.')
        self.assertTrue(np.allclose(dy, 1.0, rtol=RTOL), msg='Recovered y-spacing is incorrect.')
        # Now check coordinates...
        self.assertTrue(np.allclose(rpts, np.concatenate((x,y,z), axis=1), rtol=self.RTOL), msg='Recovered coordinates are incorrect.')
        return

    def test_bradys(self):
        """`RotationTool`: This is primarily to make sure no errors arise"""
        r = RotationTool()
        pts = ROTATED_POINTS
        xx, yy, zz, dx, dy, angle = r.EstimateAndRotate(pts[:,0], pts[:,1], pts[:,2])
        self.assertTrue(np.allclose(angle, np.deg2rad(53.55), rtol=self.RTOL), msg='Recovered angle is incorrect.')
        self.assertTrue(np.allclose(dx, 25.0, rtol=self.RTOL), msg='Recovered x-spacing is incorrect.')
        self.assertTrue(np.allclose(dy, 25.0, rtol=self.RTOL), msg='Recovered y-spacing is incorrect.')
        return



        # pts = np.array([[-193663.0, 1964850.0, 0.0], [-192847.0, 1963460.0, 0.0]])
        #print(pts[:,0])


###############################################################################

class TestVoxelizePoints(unittest.TestCase):
    """
    Test the `VoxelizePoints` filter
    """

    def test_simple_case(self):
        """`VoxelizePoints`: simple case"""
        x = np.array([0.0,1.0,0.0])
        y = np.array([0.0,0.0,1.0])
        z = np.array([0.0,0.0,0.0])
        x = np.reshape(x, (len(x), -1))
        y = np.reshape(y, (len(y), -1))
        z = np.reshape(z, (len(z), -1))
        pts = np.concatenate((x,y,z), axis=1)
        vtkpoints = PointsToPolyData(pts)
        # Use filter
        v = VoxelizePoints()
        v.SetInputDataObject(vtkpoints)
        v.SetSafeSize(5.0)
        v.Update()
        grid = v.GetOutputDataObject(0)
        # Checkout output:
        self.assertEqual(grid.GetNumberOfCells(), 3, msg='Number of CELLS is incorrect')
        self.assertEqual(grid.GetNumberOfPoints(), 16, msg='Number of POINTS is incorrect')
        bounds = grid.GetBounds()
        self.assertEqual(bounds, (-0.5,1.5, -0.5,1.5, -2.5,2.5), msg='Grid bounds are incorrect.') # Z bounds from SAFE
        return


    def test_simple_rotated_case(self):
        """`VoxelizePoints`: simple rotated case"""
        pts = ROTATED_POINTS
        vtkpoints = PointsToPolyData(ROTATED_POINTS)
        # Use filter
        v = VoxelizePoints()
        v.SetInputDataObject(vtkpoints)
        v.SetSafeSize(5.0)
        v.Update()
        grid = v.GetOutputDataObject(0)
        # Checkout output:
        #- Assumes this same data's rotation was checked by `TestRotationTool`
        self.assertEqual(grid.GetNumberOfCells(), len(pts), msg='Number of CELLS is incorrect')
        numPts = (len(pts) * 8) - ((len(pts) - 1) * 4) # Works because points make a line
        self.assertEqual(grid.GetNumberOfPoints(), numPts, msg='Number of POINTS is incorrect')
        return




###############################################################################

class TestArrayMath(unittest.TestCase):
    """
    Test the `ArrayMath` filter
    """

    def test_(self):
        self.assertTrue(False)



###############################################################################

class TestNormalizeArray(unittest.TestCase):
    """
    Test the `NormalizeArray` filter
    """

    def test_(self):
        self.assertTrue(False)


###############################################################################

class TestAddCellConnToPoints(unittest.TestCase):
    """
    Test the `AddCellConnToPoints` filter
    """

    def test_(self):
        self.assertTrue(False)


###############################################################################

class TestPointsToTube(unittest.TestCase):
    """
    Test the `PointsToTube` filter
    """

    def test_(self):
        self.assertTrue(False)


###############################################################################


class TestManySlicesAlongPoints(unittest.TestCase):
    """
    Test the `ManySlicesAlongPoints` filter
    """

    def test_(self):
        self.assertTrue(False)



###############################################################################

class TestManySlicesAlongAxis(unittest.TestCase):
    """
    Test the `ManySlicesAlongAxis` filter
    """

    def test_(self):
        self.assertTrue(False)


###############################################################################

class TestSliceThroughTime(unittest.TestCase):
    """
    Test the `SliceThroughTime` filter
    """

    def test_(self):
        self.assertTrue(False)


###############################################################################


class TestPointsToPolyData(unittest.TestCase):
    """
    Test the `PointsToPolyData` filter
    """

    def test_(self):
        self.assertTrue(False)


###############################################################################

class TestExtractPoints(unittest.TestCase):
    """
    Test the `ExtractPoints` filter
    """

    def test_(self):
        self.assertTrue(False)


###############################################################################

class TestRotateCoordinates(unittest.TestCase):
    """
    Test the `ExtractPoints` filter
    """

    def test_(self):
        self.assertTrue(False)


###############################################################################
