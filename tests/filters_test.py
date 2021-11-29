import os

import numpy as np
import pandas as pd
import pyvista

# VTK imports:
import vtk
from vtk.numpy_interface import dataset_adapter as dsa

import PVGeo
from base import TestBase
from PVGeo import interface

# Functionality to test:
from PVGeo.filters import (
    AddCellConnToPoints,
    ArrayMath,
    ArraysToRGBA,
    BuildSurfaceFromPoints,
    CombineTables,
    ExtractPoints,
    LonLatToUTM,
    ManySlicesAlongAxis,
    ManySlicesAlongPoints,
    NormalizeArray,
    PercentThreshold,
    PointsToTube,
    ReshapeTable,
    RotatePoints,
    RotationTool,
    SliceThroughTime,
    SlideSliceAlongPoints,
    VoxelizePoints,
)

RTOL = 0.000001


###############################################################################
###############################################################################


class TestCombineTables(TestBase):
    """
    Test the `CombineTables` filter
    """

    def setUp(self):
        TestBase.setUp(self)
        # Create some input tables
        self.t0 = vtk.vtkTable()
        self.t1 = vtk.vtkTable()
        # Populate the tables
        self.n = 100
        self.titles = ('Array 0', 'Array 1', 'Array 2')
        self.arrs = [None, None, None]
        self.arrs[0] = np.random.random(self.n)  # Table 0
        self.arrs[1] = np.random.random(self.n)  # Table 0
        self.arrs[2] = np.random.random(self.n)  # Table 1
        self.t0.AddColumn(interface.convert_array(self.arrs[0], self.titles[0]))
        self.t0.AddColumn(interface.convert_array(self.arrs[1], self.titles[1]))
        self.t1.AddColumn(interface.convert_array(self.arrs[2], self.titles[2]))
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
        for i, title in enumerate(self.titles):
            self.assertEqual(self.TABLE.GetColumnName(i), title)

    def test_data_fidelity(self):
        """`CombineTables`: data fidelity"""
        wpdi = dsa.WrapDataObject(self.TABLE)
        for i, title in enumerate(self.titles):
            arr = wpdi.RowData[title]
            self.assertTrue(np.allclose(arr, self.arrs[i], rtol=RTOL))


###############################################################################


class TestReshapeTable(TestBase):
    """
    Test the `ReshapeTable` filter
    """

    def setUp(self):
        TestBase.setUp(self)
        # Create some input tables
        self.t0 = vtk.vtkTable()
        # Populate the tables
        self.arrs = [None, None, None]
        self.n = 400
        self.ncols = 2
        self.nrows = int(self.n * len(self.arrs) / self.ncols)
        self.titles = ('Array 0', 'Array 1', 'Array 2')
        self.arrs[0] = np.random.random(self.n)  # Table 0
        self.arrs[1] = np.random.random(self.n)  # Table 0
        self.arrs[2] = np.random.random(self.n)  # Table 1
        self.t0.AddColumn(interface.convert_array(self.arrs[0], self.titles[0]))
        self.t0.AddColumn(interface.convert_array(self.arrs[1], self.titles[1]))
        self.t0.AddColumn(interface.convert_array(self.arrs[2], self.titles[2]))
        return

    def _check_shape(self, table):
        self.assertEqual(table.GetNumberOfRows(), self.nrows)
        self.assertEqual(table.GetNumberOfColumns(), self.ncols)
        return

    def _check_data_fidelity(self, table, order):
        wpdi = dsa.WrapDataObject(table)
        tarr = np.zeros((self.nrows, self.ncols))
        for i in range(self.ncols):
            tarr[:, i] = wpdi.RowData[i]
        arrs = np.array(self.arrs).T
        arrs = arrs.flatten()
        arrs = np.reshape(arrs, (self.nrows, self.ncols), order=order)
        self.assertEqual(tarr.shape, arrs.shape)
        self.assertTrue(np.allclose(tarr, arrs, rtol=RTOL))
        return

    def _check_data_array_titles(self, table, titles):
        for i, title in enumerate(titles):
            self.assertEqual(table.GetColumnName(i), title)
        return

    def _generate_output(self, order, titles=None):
        f = ReshapeTable()
        f.SetInputDataObject(0, self.t0)
        f.set_number_of_columns(self.ncols)
        f.set_number_of_rows(self.nrows)
        f.set_order(order)
        if titles is not None:
            f.set_names(titles)
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
        self._check_data_array_titles(
            table, ['Field %d' % i for i in range(self.ncols)]
        )
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

ROTATED_POINTS = np.genfromtxt(
    (line.encode('utf8') for line in ROTATED_TEXT.split('\n')),
    delimiter=',' '',
    dtype=float,
)


class TestRotationTool(TestBase):
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
        TestBase.setUp(self)
        self.RTOL = 0.00001  # As high as rotation precision can get
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
        pts = np.concatenate((x, y, z), axis=1)
        rot = np.deg2rad(-33.3)
        pts[:, 0:2] = r.rotate(pts[:, 0:2], rot)
        xx, yy, zz, dx, dy, angle = r.estimate_and_rotate(
            pts[:, 0], pts[:, 1], pts[:, 2]
        )
        rpts = np.vstack((xx, yy, zz)).T
        self.assertTrue(
            np.allclose(angle, np.deg2rad(33.3), rtol=RTOL),
            msg='Recovered angle is incorrect.',
        )
        self.assertTrue(
            np.allclose(dx, 1.0, rtol=RTOL), msg='Recovered x-spacing is incorrect.'
        )
        self.assertTrue(
            np.allclose(dy, 1.0, rtol=RTOL), msg='Recovered y-spacing is incorrect.'
        )
        # Now check coordinates...
        self.assertTrue(
            np.allclose(rpts, np.concatenate((x, y, z), axis=1), rtol=self.RTOL),
            msg='Recovered coordinates are incorrect.',
        )
        return

    def test_bradys(self):
        """`RotationTool`: This is primarily to make sure no errors arise"""
        r = RotationTool()
        pts = ROTATED_POINTS
        dx, dy, angle = r.estimate_and_rotate(pts[:, 0], pts[:, 1], pts[:, 2])[3::]
        self.assertTrue(
            np.allclose(angle, np.deg2rad(53.55), rtol=self.RTOL),
            msg='Recovered angle is incorrect.',
        )
        self.assertTrue(
            np.allclose(dx, 25.0, rtol=0.1), msg='Recovered x-spacing is incorrect.'
        )
        self.assertTrue(
            np.allclose(dy, 25.0, rtol=0.1), msg='Recovered y-spacing is incorrect.'
        )
        return


class TestRotatePoints(TestBase):
    """
    Test the `RotatePoints` filter
    """

    def setUp(self):
        TestBase.setUp(self)
        self.RTOL = 0.00001  # As higi as rotation precision can get
        x = np.array([0.0, 1.0, 0.0])
        y = np.array([0.0, 0.0, 1.0])
        z = np.array([0.0, 0.0, 0.0])
        x = np.reshape(x, (len(x), -1))
        y = np.reshape(y, (len(y), -1))
        z = np.reshape(z, (len(z), -1))
        self.pts = np.concatenate((x, y, z), axis=1)
        self.vtkpoints = interface.points_to_poly_data(self.pts)
        return

    def test_rotation(self):
        """`RotatePoints`: Assert produces and output"""
        f = RotatePoints()
        f.SetInputDataObject(self.vtkpoints)
        f.set_rotation_degrees(33.3)
        f.Update()
        output = f.GetOutput()
        self.assertIsNotNone(output)
        # TODO: needs further testing
        return


###############################################################################


class TestVoxelizePoints(TestBase):
    """
    Test the `VoxelizePoints` filter
    """

    def test_simple_case(self):
        """`VoxelizePoints`: simple case"""
        x = np.array([0.0, 1.0, 0.0])
        y = np.array([0.0, 0.0, 1.0])
        z = np.array([0.0, 0.0, 0.0])
        x = np.reshape(x, (len(x), -1))
        y = np.reshape(y, (len(y), -1))
        z = np.reshape(z, (len(z), -1))
        pts = np.concatenate((x, y, z), axis=1)
        vtkpoints = interface.points_to_poly_data(pts)
        # Use filter
        v = VoxelizePoints()
        v.SetInputDataObject(vtkpoints)
        v.set_safe_size(5.0)
        v.Update()
        grid = v.GetOutput()
        # Checkout output:
        self.assertEqual(grid.GetNumberOfCells(), 3, msg='Number of CELLS is incorrect')
        self.assertEqual(
            grid.GetNumberOfPoints(), 16, msg='Number of POINTS is incorrect'
        )
        bounds = grid.GetBounds()
        self.assertEqual(
            bounds, (-0.5, 1.5, -0.5, 1.5, -2.5, 2.5), msg='Grid bounds are incorrect.'
        )  # Z bounds from SAFE
        return

    def test_simple_rotated_case(self):
        """`VoxelizePoints`: simple rotated case"""
        pts = ROTATED_POINTS
        vtkpoints = interface.points_to_poly_data(ROTATED_POINTS)
        # Use filter
        v = VoxelizePoints()
        v.SetInputDataObject(vtkpoints)
        v.set_safe_size(5.0)
        v.Update()
        grid = v.GetOutput()
        # Checkout output:
        # - Assumes this same data's rotation was checked by `TestRotationTool`
        self.assertEqual(
            grid.GetNumberOfCells(), len(pts), msg='Number of CELLS is incorrect'
        )
        numPts = (len(pts) * 8) - (
            (len(pts) - 1) * 4
        )  # Works because points make a line
        self.assertEqual(
            grid.GetNumberOfPoints(), numPts, msg='Number of POINTS is incorrect'
        )
        return

    def test_mesh_grid_uniform(self):
        """`VoxelizePoints`: uniform mesh grid with given spacings"""
        # make the mesh grid
        dd = 5
        x = y = z = np.arange(0, 100, dd, dtype=float)
        g = np.meshgrid(x, y, z)
        # Convert to XYZ points
        points = np.vstack(list(map(np.ravel, g))).T
        rand = np.random.random(len(points))
        vtkpoints = interface.points_to_poly_data(points)
        vtkpoints.GetPointData().AddArray(interface.convert_array(rand, 'Random'))
        # Use filter
        v = VoxelizePoints()
        v.SetInputDataObject(vtkpoints)
        v.set_estimate_grid(False)  # Cell size is explicitly set
        v.set_delta_x(10)
        v.set_delta_y(10)
        v.set_delta_z(10)
        v.Update()
        grid = v.GetOutput()
        wgrd = dsa.WrapDataObject(grid)
        celldata = wgrd.CellData['Random']
        # Checkout output:
        self.assertEqual(
            grid.GetNumberOfCells(), 8 * 10 ** 3, msg='Number of CELLS is incorrect'
        )
        numPts = (len(x) + 2) ** 3
        self.assertEqual(
            grid.GetNumberOfPoints(), numPts, msg='Number of POINTS is incorrect'
        )
        self.assertTrue(np.allclose(celldata, rand))

        # Now check that we can set the spacing for every cell
        spac = np.full((len(points)), 10.0)
        v.set_deltas(spac, spac, spac)
        v.Update()
        grid = v.GetOutput()
        wgrd = dsa.WrapDataObject(grid)
        celldata = wgrd.CellData['Random']
        self.assertEqual(
            grid.GetNumberOfCells(), 8 * 10 ** 3, msg='Number of CELLS is incorrect'
        )
        self.assertEqual(
            grid.GetNumberOfPoints(), numPts, msg='Number of POINTS is incorrect'
        )
        self.assertTrue(np.allclose(celldata, rand))
        return


###############################################################################


class TestExtractPoints(TestBase):
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
        self.assertTrue(f.error_occurred())
        return


###############################################################################


class TestArrayMath(TestBase):
    """
    Test the `ArrayMath` filter
    """

    def setUp(self):
        TestBase.setUp(self)
        # Create some input tables
        self.t0 = vtk.vtkTable()
        # Populate the tables
        self.arrs = [None, None]
        self.n = 400
        self.titles = ('Array 0', 'Array 1')
        self.arrs[0] = np.random.random(self.n)  # Table 0
        self.arrs[1] = np.random.random(self.n)  # Table 0
        self.t0.AddColumn(interface.convert_array(self.arrs[0], self.titles[0]))
        self.t0.AddColumn(interface.convert_array(self.arrs[1], self.titles[1]))
        return

    def test_get_operations(self):
        """`ArrayMath`: get operations"""
        op = ArrayMath.get_operation('add')
        self.assertIsNotNone(op)
        op = ArrayMath.get_operation('subtract')
        self.assertIsNotNone(op)
        op = ArrayMath.get_operation('multiply')
        self.assertIsNotNone(op)
        op = ArrayMath.get_operation('divide')
        self.assertIsNotNone(op)
        op = ArrayMath.get_operation('correlate')
        self.assertIsNotNone(op)

    def _gen_and_check(self, op, check, flip=False):
        # Perform filter
        f = ArrayMath()
        f.set_operation(op)
        f.set_new_array_name('test')
        if flip:
            output = f.apply(self.t0, self.titles[1], self.titles[0])
        else:
            output = f.apply(self.t0, self.titles[0], self.titles[1])
        wout = dsa.WrapDataObject(output)
        arr = wout.RowData['test']
        self.assertTrue(np.allclose(arr, check, rtol=RTOL))

    def test_add(self):
        """`ArrayMath`: ADD"""
        op = ArrayMath.get_operation('add')
        check = self.arrs[0] + self.arrs[1]
        self._gen_and_check(op, check)
        # now flip order and check
        # result should be same
        self._gen_and_check(op, check, flip=True)

    def test_subtract(self):
        """`ArrayMath`: SUBTRACT"""
        op = ArrayMath.get_operation('subtract')
        check = self.arrs[0] - self.arrs[1]
        self._gen_and_check(op, check)
        # now flip order and check
        check = self.arrs[1] - self.arrs[0]
        self._gen_and_check(op, check, flip=True)

    def test_multiply(self):
        """`ArrayMath`: MULTIPLY"""
        op = ArrayMath.get_operation('multiply')
        check = self.arrs[0] * self.arrs[1]
        self._gen_and_check(op, check)
        # now flip order and check
        # result should be same
        self._gen_and_check(op, check, flip=True)

    def test_divide(self):
        """`ArrayMath`: DIVIDE"""
        op = ArrayMath.get_operation('divide')
        check = self.arrs[0] / self.arrs[1]
        self._gen_and_check(op, check)
        # now flip order and check
        check = self.arrs[1] / self.arrs[0]
        self._gen_and_check(op, check, flip=True)

    def test_correlate(self):
        """`ArrayMath`: CORRELATE"""
        op = ArrayMath.get_operation('correlate')
        check = np.correlate(self.arrs[0], self.arrs[1], mode='same')
        self._gen_and_check(op, check)
        # now flip order and check
        check = np.correlate(self.arrs[1], self.arrs[0], mode='same')
        self._gen_and_check(op, check, flip=True)


###############################################################################


class TestNormalizeArray(TestBase):
    """
    Test the `NormalizeArray` filter
    """

    def setUp(self):
        TestBase.setUp(self)
        # Create some input tables
        self.t0 = vtk.vtkTable()
        # Populate the tables
        self.n = 400
        self.title = 'Array 0'
        self.arr = np.random.random(self.n)  # Table 0
        self.t0.AddColumn(interface.convert_array(self.arr, self.title))
        return

    def test_get_operations(self):
        """`NormalizeArray`: get operations"""
        op = NormalizeArray.get_normalization('feature_scale')
        self.assertIsNotNone(op)
        op = NormalizeArray.get_normalization('standard_score')
        self.assertIsNotNone(op)
        op = NormalizeArray.get_normalization('log10')
        self.assertIsNotNone(op)
        op = NormalizeArray.get_normalization('natural_log')
        self.assertIsNotNone(op)
        op = NormalizeArray.get_normalization('just_multiply')
        self.assertIsNotNone(op)

    def _gen_and_check(self, op, check, flip=False):
        # Perform filter
        f = NormalizeArray()
        f.set_normalization(op)
        f.set_new_array_name('test')
        # Now test the result
        output = f.apply(self.t0, self.title)
        wout = dsa.WrapDataObject(output)
        arr = wout.RowData['test']
        self.assertTrue(np.allclose(arr, check, rtol=RTOL))

    def test_feature_scale(self):
        """`NormalizeArray`: FEATURE SCALE"""
        op = NormalizeArray.get_normalization('feature_scale')
        check = NormalizeArray._feature_scale(self.arr)
        self._gen_and_check(op, check)

    def test_standard_score(self):
        """`NormalizeArray`: STANDARD SCORE"""
        op = NormalizeArray.get_normalization('standard_score')
        check = NormalizeArray._standard_score(self.arr)
        self._gen_and_check(op, check)

    def test_log10(self):
        """`NormalizeArray`: LOG10"""
        op = NormalizeArray.get_normalization('log10')
        check = NormalizeArray._log10(self.arr)
        self._gen_and_check(op, check)

    def test_natural_log(self):
        """`NormalizeArray`: NATURAL LOG"""
        op = NormalizeArray.get_normalization('natural_log')
        check = NormalizeArray._log_nat(self.arr)
        self._gen_and_check(op, check)

    def test_just_multiply(self):
        """`NormalizeArray`: MULTIPLY"""
        op = NormalizeArray.get_normalization('just_multiply')
        check = NormalizeArray._pass_array(self.arr)
        self._gen_and_check(op, check)


###############################################################################


class TestAddCellConnToPoints(TestBase):
    """
    Test the `AddCellConnToPoints` filter
    """

    def makeSimpleInput(self):
        x = np.array([0.0, 1.0, 0.0])
        y = np.array([0.0, 0.0, 1.0])
        z = np.array([0.0, 0.0, 0.0])
        x = np.reshape(x, (len(x), -1))
        y = np.reshape(y, (len(y), -1))
        z = np.reshape(z, (len(z), -1))
        self.pts = np.concatenate((x, y, z), axis=1)
        self.vtkpoints = interface.points_to_poly_data(self.pts)

    def makeComplicatedInput(self, shuffle=True):
        def path1(y):
            # Equation: x = a(y-h)^2 + k
            k = 110.0
            h = 0.0
            a = -k / 160.0 ** 2
            x = a * (y - h) ** 2 + k
            idxs = np.argwhere(x > 0)
            return x[idxs][:, 0], y[idxs][:, 0]

        y = np.arange(0.0, 10.0)
        zo = np.linspace(9.0, 11.0, num=len(y))
        x, y = path1(y)

        coords = np.zeros((len(y), 3))
        coords[:, 0] = x
        coords[:, 1] = y
        coords[:, 2] = zo

        np.random.shuffle(coords)
        self.pts = coords
        self.vtkpoints = interface.points_to_poly_data(self.pts)

    def test_poly_line(self):
        """`AddCellConnToPoints`: POLY LINE"""
        self.makeSimpleInput()
        f = AddCellConnToPoints()
        f.SetInputDataObject(self.vtkpoints)
        f.set_cell_type(vtk.VTK_POLY_LINE)
        f.Update()
        output = f.GetOutput()
        self.assertEqual(1, output.GetNumberOfCells())
        # Now test nearest neighbor functionality
        self.makeComplicatedInput()
        f = AddCellConnToPoints()
        f.SetInputDataObject(self.vtkpoints)
        f.set_cell_type(vtk.VTK_POLY_LINE)
        f.set_use_nearest_nbr(True)
        f.Update()
        output = f.GetOutput()
        self.assertEqual(1, output.GetNumberOfCells())
        # Its fairly difficult to test the nearest neighbor approximations...
        # This was done visually
        # The above test is just there to make sure no errors are thrown
        # NOTE: assumes developers visually inspect if functionality changes
        return

    def test_line(self):
        """`AddCellConnToPoints`: LINE"""
        self.makeSimpleInput()
        f = AddCellConnToPoints()
        f.SetInputDataObject(self.vtkpoints)
        f.set_cell_type(vtk.VTK_LINE)
        f.Update()
        output = f.GetOutput()
        self.assertEqual(len(self.pts) - 1, output.GetNumberOfCells())
        # Now test nearest neighbor functionality
        self.makeComplicatedInput()
        f = AddCellConnToPoints()
        f.SetInputDataObject(self.vtkpoints)
        f.set_cell_type(vtk.VTK_LINE)
        f.set_use_nearest_nbr(True)
        f.Update()
        output = f.GetOutput()
        self.assertEqual(len(self.pts) - 1, output.GetNumberOfCells())
        # Its fairly difficult to test the nearest neighbor approximations...
        # This was done visually in ParaView.
        # The above test is just there to make sure no errors are thrown
        # NOTE: assumes developers visually inspect in ParaView if functionality changes
        return

    def test_line_closed(self):
        """`AddCellConnToPoints`: LINE"""
        self.makeSimpleInput()
        f = AddCellConnToPoints(close_loop=True)
        f.SetInputDataObject(self.vtkpoints)
        f.set_cell_type(vtk.VTK_LINE)
        f.Update()
        output = f.GetOutput()
        self.assertEqual(len(self.pts), output.GetNumberOfCells())
        # Now test nearest neighbor functionality
        self.makeComplicatedInput()
        f = AddCellConnToPoints(close_loop=True)
        f.SetInputDataObject(self.vtkpoints)
        f.set_cell_type(vtk.VTK_LINE)
        f.set_use_nearest_nbr(True)
        f.Update()
        output = f.GetOutput()
        # NOTE: the algorithm adds vertice and line cells
        self.assertEqual(len(self.pts), output.GetNumberOfCells())
        # Its fairly difficult to test the nearest neighbor approximations...
        # This was done visually in ParaView.
        # The above test is just there to make sure no errors are thrown
        # NOTE: assumes developers visually inspect in ParaView if functionality changes
        return


###############################################################################


class TestPointsToTube(TestBase):
    """
    Test the `PointsToTube` filter
    """

    def makeComplicatedInput(self, shuffle=True):
        def path1(y):
            # Equation: x = a(y-h)^2 + k
            k = 110.0
            h = 0.0
            a = -k / 160.0 ** 2
            x = a * (y - h) ** 2 + k
            idxs = np.argwhere(x > 0)
            return x[idxs][:, 0], y[idxs][:, 0]

        y = np.linspace(0.0, 200.0, num=100)
        x, y = path1(y)
        zo = np.linspace(9.0, 11.0, num=len(y))

        coords = np.zeros((len(y), 3))
        coords[:, 0] = x
        coords[:, 1] = y
        coords[:, 2] = zo

        np.random.shuffle(coords)
        self.pts = coords
        self.vtkpoints = interface.points_to_poly_data(self.pts)

    def test_tube_from_shuffled_points(self):
        """`PointsToTube`: Test generation of tube from shuffled points"""
        self.makeComplicatedInput()
        f = PointsToTube()
        f.SetInputDataObject(self.vtkpoints)
        f.set_radius(20)
        f.set_number_of_sides(10)
        f.set_use_nearest_nbr(True)
        f.Update()
        output = f.GetOutput()
        self.assertTrue(output.GetNumberOfCells() > 0)
        self.assertTrue(output.GetNumberOfPoints() > 0)


###############################################################################

proj = False
try:
    import pyproj

    proj = True
except ImportError:
    pass


if proj:

    class TestLonLatToUTM(TestBase):
        """
        Test the `LonLatToUTM` filter
        """

        # NOTE: ``pyproj`` MUST be installed

        def test_conversion(self):
            """`LonLatToUTM`: CONVERSION"""
            self.filename = os.path.join(
                os.path.dirname(__file__), 'data/das-coords.csv'
            )
            # read in data that has Lat/Lon and pre converted points in zone 11
            data = pd.read_csv(self.filename)
            points = interface.points_to_poly_data(
                data[['longitude', 'latitude', 'altitude']]
            )
            converted = LonLatToUTM(zone=11).apply(points)
            converted.GetPoints()
            wpdi = dsa.WrapDataObject(converted)
            points = np.array(wpdi.Points)
            self.assertTrue(np.allclose(points, data[['x_utm', 'y_utm', 'altitude']]))
            return True


###############################################################################


class TestManySlicesAlongPoints(TestBase):
    """
    Test the `ManySlicesAlongPoints`, `ManySlicesAlongAxis`, and `SliceThroughTime` filters
    """

    def setUp(self):
        TestBase.setUp(self)
        # create a volumetric data set
        self.grid = PVGeo.model_build.CreateTensorMesh().apply()
        # create a spline throught the data set

        def path1(y):
            """Equation: x = a(y-h)^2 + k"""
            a = -0.0001
            x = a * y ** 2 + 1000
            idxs = np.argwhere(x > 0)
            return x[idxs][:, 0], y[idxs][:, 0]

        x, y = path1(np.arange(-500.0, 1500.0, 25.0))
        zo = np.linspace(9.0, 11.0, num=len(y))
        coords = np.vstack((x, y, zo)).T
        self.points = interface.points_to_poly_data(coords)

    def test_along_points(self):
        """`ManySlicesAlongPoints`: slice along points"""
        # run the algorithms
        slices = ManySlicesAlongPoints(n_slices=10).apply(self.points, self.grid)
        self.assertTrue(isinstance(slices, vtk.vtkMultiBlockDataSet))
        self.assertEqual(10, slices.GetNumberOfBlocks())
        # Can we really test anything further on this?
        #   Testing the slice positions would be crazy difficult

    def test_slider(self):
        """`SlideSliceAlongPoints`: use slider"""
        # Set up the algorithm
        alg = SlideSliceAlongPoints(n_slices=10)
        slc = alg.apply(self.points, self.grid)
        self.assertTrue(isinstance(slc, vtk.vtkPolyData))
        alg.set_location(30)
        alg.Update()
        self.assertTrue(isinstance(slc, vtk.vtkPolyData))
        alg.set_location(95)
        alg.Update()
        self.assertTrue(isinstance(slc, vtk.vtkPolyData))
        # Can we really test anything further on this?
        #   Testing the slice positions would be crazy difficult


###############################################################################


class TestManySlicesAlongAxis(TestBase):
    """
    Test the `ManySlicesAlongAxis` and `SliceThroughTime` filters
    """

    def setUp(self):
        TestBase.setUp(self)
        # create a volumetric data set
        self.grid = PVGeo.model_build.CreateTensorMesh().apply()

    def test_along_axis(self):
        """`ManySlicesAlongAxis`: along axis"""
        # run the algorithm
        slices = ManySlicesAlongAxis(n_slices=10, axis=0).apply(self.grid)
        self.assertTrue(isinstance(slices, vtk.vtkMultiBlockDataSet))
        self.assertEqual(10, slices.GetNumberOfBlocks())
        # Can we really test anything further on this?
        #   Testing the slice positions would be crazy difficult

    def test_through_time(self):
        """`SliceThroughTime`: along axis"""
        # Set up the algorithm
        alg = SliceThroughTime(n_slices=10, axis=1)
        slc = alg.apply(self.grid)
        self.assertTrue(isinstance(slc, vtk.vtkPolyData))
        alg.UpdateTimeStep(1)
        self.assertTrue(isinstance(slc, vtk.vtkPolyData))
        alg.UpdateTimeStep(3)
        self.assertTrue(isinstance(slc, vtk.vtkPolyData))


###############################################################################


class TestPercentThreshold(TestBase):
    """
    Test the `PercentThreshold` filter
    """

    def test(self):
        """`PercentThreshold`: make sure no errors arise"""
        data = PVGeo.model_build.CreateTensorMesh().apply()
        thresh = PercentThreshold(percent=75).apply(data, 'Random Data')
        self.assertTrue(isinstance(thresh, vtk.vtkUnstructuredGrid))
        return True


###############################################################################


class TestArraysToRGBA(TestBase):
    """
    Test the `ArraysToRGBA` filter
    """

    def test(self):
        """`ArraysToRGBA`: make sure no errors arise"""
        # create an input with three arrays that can be RGB
        r = np.random.randint(0, 255, 300)
        g = np.random.randint(0, 255, 300)
        b = np.random.randint(0, 255, 300)
        a = np.random.uniform(0, 1, 300)
        # now make it an arbirtray dataset
        df = pd.DataFrame(
            data=np.c_[r, g, b, r, g, b, a], columns=['x', 'y', 'z', 'R', 'G', 'B', 'A']
        )
        data = interface.points_to_poly_data(df)
        # Set up the algorithm
        colored = ArraysToRGBA().apply(data, 'R', 'G', 'B', 'A')
        # Make sure there is a new 'Colors' Array
        arr = colored.GetPointData().GetArray('Colors')
        self.assertTrue(isinstance(arr, vtk.vtkUnsignedCharArray))
        return True


###############################################################################


class TestBuildSurfaceFromPoints(TestBase):
    """
    Test the `BuildSurfaceFromPoints` filter
    """

    def test(self):
        """`BuildSurfaceFromPoints`: make sure no errors arise"""
        x = np.arange(100)
        y = 0.01 * x ** 2
        points = np.c_[x, y, np.zeros_like(x)]
        z_range = np.arange(20)
        mesh = BuildSurfaceFromPoints.create_surface(points, z_range)
        assert isinstance(mesh, pyvista.StructuredGrid)
        assert mesh.dimensions == (len(z_range), len(points), 1)
        poly = pyvista.PolyData(points)
        mesh = BuildSurfaceFromPoints(zcoords=z_range).apply(poly)
        assert isinstance(mesh, pyvista.StructuredGrid)
        assert mesh.dimensions == (len(z_range), len(points), 1)
        return True


###############################################################################
###############################################################################
###############################################################################
if __name__ == '__main__':
    import unittest

    unittest.main()
###############################################################################
###############################################################################
###############################################################################
