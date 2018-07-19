import unittest
import numpy as np

# VTK imports:
import vtk
from vtk.util import numpy_support as nps
from vtk.numpy_interface import dataset_adapter as dsa
from .. import _helpers

# Functionality to test:
from .poly import *
from .slicing import *
from .tables import *
from .voxelize import *
from .xyz import *

RTOL = 0.000001


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
        self.t0.AddColumn(_helpers.numToVTK(self.arrs[0], self.titles[0]))
        self.t0.AddColumn(_helpers.numToVTK(self.arrs[1], self.titles[1]))
        self.t1.AddColumn(_helpers.numToVTK(self.arrs[2], self.titles[2]))
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
        self.n = 400
        self.ncols = 2
        self.nrows = int(self.n * len(self.arrs) / self.ncols)
        self.titles = ('Array 0', 'Array 1', 'Array 2')
        self.arrs[0] = np.random.random(self.n) # Table 0
        self.arrs[1] = np.random.random(self.n) # Table 0
        self.arrs[2] = np.random.random(self.n) # Table 1
        self.t0.AddColumn(_helpers.numToVTK(self.arrs[0], self.titles[0]))
        self.t0.AddColumn(_helpers.numToVTK(self.arrs[1], self.titles[1]))
        self.t0.AddColumn(_helpers.numToVTK(self.arrs[2], self.titles[2]))
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
        """`ReshapeTable`: C-order, input names given as string"""
        order = 'C'
        titles = ['Title %d' % i for i in range(self.ncols)]
        ts = ';'.join(t for t in titles)
        table = self._generate_output(order, titles=ts)
        # Check output:
        self._check_shape(table)
        self._check_data_fidelity(table, order)
        self._check_data_array_titles(table, titles)
        return

    def test_reshape_c_names(self):
        """`ReshapeTable`: C-order, few input names given"""
        order = 'C'
        fewtitles = ['Title %d' % i for i in range(self.ncols - 2)]
        rest = ['Field %d' % i for i in range(2)]
        table = self._generate_output(order, titles=fewtitles)
        # Check output:
        self._check_shape(table)
        self._check_data_fidelity(table, order)
        self._check_data_array_titles(table, fewtitles + rest)
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
        dx, dy, angle = r.EstimateAndRotate(pts[:,0], pts[:,1], pts[:,2])[3::]
        self.assertTrue(np.allclose(angle, np.deg2rad(53.55), rtol=self.RTOL), msg='Recovered angle is incorrect.')
        self.assertTrue(np.allclose(dx, 25.0, rtol=self.RTOL), msg='Recovered x-spacing is incorrect.')
        self.assertTrue(np.allclose(dy, 25.0, rtol=self.RTOL), msg='Recovered y-spacing is incorrect.')
        return



class TestRotatePoints(unittest.TestCase):
    """
    Test the `RotatePoints` filter
    """
    def setUp(self):
        self.RTOL = 0.00001 # As higi as rotation precision can get
        x = np.array([0.0,1.0,0.0])
        y = np.array([0.0,0.0,1.0])
        z = np.array([0.0,0.0,0.0])
        x = np.reshape(x, (len(x), -1))
        y = np.reshape(y, (len(y), -1))
        z = np.reshape(z, (len(z), -1))
        self.pts = np.concatenate((x,y,z), axis=1)
        self.vtkpoints = PointsToPolyData(self.pts)
        return

    def test_rotation(self):
        f = RotatePoints()
        f.SetInputDataObject(self.vtkpoints)
        f.SetRotationDegrees(33.3)
        f.Update()
        output = f.GetOutput()
        self.assertIsNotNone(output)


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
        grid = v.GetOutput()
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
        grid = v.GetOutput()
        # Checkout output:
        #- Assumes this same data's rotation was checked by `TestRotationTool`
        self.assertEqual(grid.GetNumberOfCells(), len(pts), msg='Number of CELLS is incorrect')
        numPts = (len(pts) * 8) - ((len(pts) - 1) * 4) # Works because points make a line
        self.assertEqual(grid.GetNumberOfPoints(), numPts, msg='Number of POINTS is incorrect')
        return

    def test_mesh_grid_uniform(self):
        """`VoxelizePoints`: uniform mesh grid with given spacings"""
        # make the mesh grid
        dd = 5
        x = y = z = np.arange(0, 100, dd, dtype=float)
        g = np.meshgrid(x, y, z)
        # Convert to XYZ points
        points = np.vstack(map(np.ravel, g)).T
        rand = np.random.random(len(points))
        vtkpoints = PointsToPolyData(points)
        vtkpoints.GetPointData().AddArray(_helpers.numToVTK(rand, 'Random'))
        # Use filter
        v = VoxelizePoints()
        v.SetInputDataObject(vtkpoints)
        v.SetEstimateGrid(False) # Cell size is explicitly set
        v.SetDeltaX(10)
        v.SetDeltaY(10)
        v.SetDeltaZ(10)
        v.Update()
        grid = v.GetOutput()
        wgrd = dsa.WrapDataObject(grid)
        celldata = wgrd.CellData['Random']
        # Checkout output:
        self.assertEqual(grid.GetNumberOfCells(), 8*10**3, msg='Number of CELLS is incorrect')
        numPts = (len(x)+2)**3
        self.assertEqual(grid.GetNumberOfPoints(), numPts, msg='Number of POINTS is incorrect')
        self.assertTrue(np.allclose(celldata, rand))

        # Now check that we can set the spacing for every cell
        spac = np.full((len(points)), 10.0)
        v.SetDeltas(spac, spac, spac)
        v.Update()
        grid = v.GetOutput()
        wgrd = dsa.WrapDataObject(grid)
        celldata = wgrd.CellData['Random']
        self.assertEqual(grid.GetNumberOfCells(), 8*10**3, msg='Number of CELLS is incorrect')
        self.assertEqual(grid.GetNumberOfPoints(), numPts, msg='Number of POINTS is incorrect')
        self.assertTrue(np.allclose(celldata, rand))
        return




###############################################################################


class TestExtractPoints(unittest.TestCase):
    """
    Test the `ExtractPoints` filter
    """
    def test_bad_extraction(self):
        """`ExtractPoints`: catch a bad extraction"""
        img = vtk.vtkImageData()
        img.SetDimensions(10, 10, 10)
        f = ExtractPoints()
        f.SetInputDataObject(img)
        f.Update()
        self.assertTrue(f.ErrorOccurred())
        return



###############################################################################

class TestArrayMath(unittest.TestCase):
    """
    Test the `ArrayMath` filter
    """

    def setUp(self):
        # Create some input tables
        self.t0 = vtk.vtkTable()
        # Populate the tables
        self.arrs = [None, None]
        self.n = 400
        self.titles = ('Array 0', 'Array 1')
        self.arrs[0] = np.random.random(self.n) # Table 0
        self.arrs[1] = np.random.random(self.n) # Table 0
        self.t0.AddColumn(_helpers.numToVTK(self.arrs[0], self.titles[0]))
        self.t0.AddColumn(_helpers.numToVTK(self.arrs[1], self.titles[1]))
        return

    def test_get_operations(self):
        op = ArrayMath.GetOperation('add')
        self.assertIsNotNone(op)
        op = ArrayMath.GetOperation('subtract')
        self.assertIsNotNone(op)
        op = ArrayMath.GetOperation('multiply')
        self.assertIsNotNone(op)
        op = ArrayMath.GetOperation('divide')
        self.assertIsNotNone(op)
        op = ArrayMath.GetOperation('correlate')
        self.assertIsNotNone(op)

    def _gen_and_check(self, op, check, flip=False):
        # Perform filter
        f = ArrayMath()
        f.SetInputDataObject(self.t0)
        if flip:
            f.SetInputArrayToProcess(1, 0, 0, 6, self.titles[0]) # field 6 is row data
            f.SetInputArrayToProcess(0, 0, 0, 6, self.titles[1]) # field 6 is row data
        else:
            f.SetInputArrayToProcess(0, 0, 0, 6, self.titles[0]) # field 6 is row data
            f.SetInputArrayToProcess(1, 0, 0, 6, self.titles[1]) # field 6 is row data
        f.SetOperation(op)
        f.SetNewArrayName('test')
        f.Update()
        # Now test the result
        output = f.GetOutput()
        wout = dsa.WrapDataObject(output)
        arr = wout.RowData['test']
        self.assertTrue(np.allclose(arr, check, rtol=RTOL))


    def test_add(self):
        op = ArrayMath.GetOperation('add')
        check = self.arrs[0] + self.arrs[1]
        self._gen_and_check(op, check)
        # now flip order and check
        # result should be same
        self._gen_and_check(op, check, flip=True)


    def test_subtract(self):
        op = ArrayMath.GetOperation('subtract')
        check = self.arrs[0] - self.arrs[1]
        self._gen_and_check(op, check)
        # now flip order and check
        check = self.arrs[1] - self.arrs[0]
        self._gen_and_check(op, check, flip=True)

    def test_multiply(self):
        op = ArrayMath.GetOperation('multiply')
        check = self.arrs[0] * self.arrs[1]
        self._gen_and_check(op, check)
        # now flip order and check
        # result should be same
        self._gen_and_check(op, check, flip=True)

    def test_divide(self):
        op = ArrayMath.GetOperation('divide')
        check = self.arrs[0] / self.arrs[1]
        self._gen_and_check(op, check)
        # now flip order and check
        check = self.arrs[1] / self.arrs[0]
        self._gen_and_check(op, check, flip=True)

    def test_correlate(self):
        op = ArrayMath.GetOperation('correlate')
        check = np.correlate(self.arrs[0], self.arrs[1], mode='same')
        self._gen_and_check(op, check)
        # now flip order and check
        check = np.correlate(self.arrs[1], self.arrs[0], mode='same')
        self._gen_and_check(op, check, flip=True)



###############################################################################

class TestNormalizeArray(unittest.TestCase):
    """
    Test the `NormalizeArray` filter
    """

    def setUp(self):
        # Create some input tables
        self.t0 = vtk.vtkTable()
        # Populate the tables
        self.n = 400
        self.title = 'Array 0'
        self.arr = np.random.random(self.n) # Table 0
        self.t0.AddColumn(_helpers.numToVTK(self.arr, self.title))
        return

    def test_get_operations(self):
        op = NormalizeArray.GetNormalization('feature_scale')
        self.assertIsNotNone(op)
        op = NormalizeArray.GetNormalization('standard_score')
        self.assertIsNotNone(op)
        op = NormalizeArray.GetNormalization('log10')
        self.assertIsNotNone(op)
        op = NormalizeArray.GetNormalization('natural_log')
        self.assertIsNotNone(op)
        op = NormalizeArray.GetNormalization('just_multiply')
        self.assertIsNotNone(op)

    def _gen_and_check(self, op, check, flip=False):
        # Perform filter
        f = NormalizeArray()
        f.SetInputDataObject(self.t0)
        f.SetInputArrayToProcess(0, 0, 0, 6, self.title) # field 6 is row data
        f.SetNormalization(op)
        f.SetNewArrayName('test')
        f.Update()
        # Now test the result
        output = f.GetOutput()
        wout = dsa.WrapDataObject(output)
        arr = wout.RowData['test']
        self.assertTrue(np.allclose(arr, check, rtol=RTOL))


    def test_feature_scale(self):
        op = NormalizeArray.GetNormalization('feature_scale')
        check = NormalizeArray._featureScale(self.arr)
        self._gen_and_check(op, check)

    def test_standard_score(self):
        op = NormalizeArray.GetNormalization('standard_score')
        check = NormalizeArray._standardScore(self.arr)
        self._gen_and_check(op, check)

    def test_log10(self):
        op = NormalizeArray.GetNormalization('log10')
        check = NormalizeArray._log10(self.arr)
        self._gen_and_check(op, check)

    def test_natural_log(self):
        op = NormalizeArray.GetNormalization('natural_log')
        check = NormalizeArray._logNat(self.arr)
        self._gen_and_check(op, check)

    def test_just_multiply(self):
        op = NormalizeArray.GetNormalization('just_multiply')
        check = NormalizeArray._passArray(self.arr)
        self._gen_and_check(op, check)


###############################################################################

class TestAddCellConnToPoints(unittest.TestCase):
    """
    Test the `AddCellConnToPoints` filter
    """

    def makeSimpleInput(self):
        x = np.array([0.0,1.0,0.0])
        y = np.array([0.0,0.0,1.0])
        z = np.array([0.0,0.0,0.0])
        x = np.reshape(x, (len(x), -1))
        y = np.reshape(y, (len(y), -1))
        z = np.reshape(z, (len(z), -1))
        self.pts = np.concatenate((x,y,z), axis=1)
        self.vtkpoints = PointsToPolyData(self.pts)

    def makeComplicatedInput(self, shuffle=True):
        def path1(y):
            # Equation: x = a(y-h)^2 + k
            k = 110.0
            h = 0.0
            a = - k / 160.0**2
            x = a*(y-h)**2 + k
            idxs = np.argwhere(x>0)
            return x[idxs][:,0], y[idxs][:,0]

        y = np.arange(0.0,10.0)
        zo = np.linspace(9.0,11.0, num=len(y))
        x,y = path1(y)

        coords = np.zeros((len(y),3))
        coords[:,0] = x
        coords[:,1] = y
        coords[:,2] = zo

        np.random.shuffle(coords)
        self.pts = coords
        self.vtkpoints = PointsToPolyData(self.pts)

    def test_poly_line(self):
        self.makeSimpleInput()
        f = AddCellConnToPoints()
        f.SetInputDataObject(self.vtkpoints)
        f.SetCellType(vtk.VTK_POLY_LINE)
        f.Update()
        output = f.GetOutput()
        self.assertEqual(1, output.GetNumberOfCells())
        # Now test nearest neighbor functionality
        self.makeComplicatedInput()
        f = AddCellConnToPoints()
        f.SetInputDataObject(self.vtkpoints)
        f.SetCellType(vtk.VTK_POLY_LINE)
        f.SetUseNearestNbr(True)
        f.Update()
        output = f.GetOutput()
        self.assertEqual(1, output.GetNumberOfCells())
        # Its fairly difficult to test the nearest neighbor approximations...
        # This was done visually in ParaView.
        # The above test is just there to make sure no errors are thrown
        # NOTE: assumes developers visually inspect in ParaView if functionality changes
        return

    def test_line(self):
        self.makeSimpleInput()
        f = AddCellConnToPoints()
        f.SetInputDataObject(self.vtkpoints)
        f.SetCellType(vtk.VTK_LINE)
        f.Update()
        output = f.GetOutput()
        self.assertEqual(len(self.pts)-1, output.GetNumberOfCells())
        # Now test nearest neighbor functionality
        self.makeComplicatedInput()
        f = AddCellConnToPoints()
        f.SetInputDataObject(self.vtkpoints)
        f.SetCellType(vtk.VTK_LINE)
        f.SetUseNearestNbr(True)
        f.Update()
        output = f.GetOutput()
        self.assertEqual(len(self.pts)-1, output.GetNumberOfCells())
        # Its fairly difficult to test the nearest neighbor approximations...
        # This was done visually in ParaView.
        # The above test is just there to make sure no errors are thrown
        # NOTE: assumes developers visually inspect in ParaView if functionality changes
        return


###############################################################################

class TestPointsToTube(unittest.TestCase):
    """
    Test the `PointsToTube` filter
    """
    def makeComplicatedInput(self, shuffle=True):
        def path1(y):
            # Equation: x = a(y-h)^2 + k
            k = 110.0
            h = 0.0
            a = - k / 160.0**2
            x = a*(y-h)**2 + k
            idxs = np.argwhere(x>0)
            return x[idxs][:,0], y[idxs][:,0]

        y = np.linspace(0.0, 200.0, num=100)
        x,y = path1(y)
        zo = np.linspace(9.0,11.0, num=len(y))

        coords = np.zeros((len(y),3))
        coords[:,0] = x
        coords[:,1] = y
        coords[:,2] = zo

        np.random.shuffle(coords)
        self.pts = coords
        self.vtkpoints = PointsToPolyData(self.pts)

    def test_(self):
        self.makeComplicatedInput()
        f = PointsToTube()
        f.SetInputDataObject(self.vtkpoints)
        f.SetRadius(20)
        f.SetNumberOfSides(10)
        f.SetUseNearestNbr(True)
        f.Update()
        output = f.GetOutput()
        self.assertEqual(10, output.GetNumberOfCells())
        self.assertEqual(10*len(self.pts), output.GetNumberOfPoints())


# ###############################################################################
#
#
# class TestManySlicesAlongPoints(unittest.TestCase):
#     """
#     Test the `ManySlicesAlongPoints` filter
#     """
#
#     def test_(self):
#         self.assertTrue(False)
#
#
#
# ###############################################################################
#
# class TestManySlicesAlongAxis(unittest.TestCase):
#     """
#     Test the `ManySlicesAlongAxis` filter
#     """
#
#     def test_(self):
#         self.assertTrue(False)
#
#
# ###############################################################################
#
# class TestSliceThroughTime(unittest.TestCase):
#     """
#     Test the `SliceThroughTime` filter
#     """
#
#     def test_(self):
#         self.assertTrue(False)
#
#
# ###############################################################################
#
# class TestExtractPoints(unittest.TestCase):
#     """
#     Test the `ExtractPoints` filter
#     """
#
#     def test_(self):
#         self.assertTrue(False)
#
#
# ###############################################################################
