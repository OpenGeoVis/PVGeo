from base import TestBase
import numpy as np
import shutil
import tempfile
import os

# VTK imports:
import vtk
from vtk.numpy_interface import dataset_adapter as dsa

import PVGeo
from PVGeo import _helpers
from PVGeo import interface
# Functionality to test:
from PVGeo.grids import *

RTOL = 0.000001


###############################################################################

class TestTableToTimeGrid(TestBase):
    """
    Test the `TableToTimeGrid` filter
    """
    def setUp(self):
        TestBase.setUp(self)
        # Create some input tables
        self.table = vtk.vtkTable()
        # Populate the tables
        self.arrs = [None, None, None]
        self.n = 400
        self.titles = ('Array 0', 'Array 1', 'Array 2')
        self.arrs[0] = np.random.random(self.n)
        self.arrs[1] = np.random.random(self.n)
        self.arrs[2] = np.random.random(self.n)
        self.table.AddColumn(interface.convertArray(self.arrs[0], self.titles[0]))
        self.table.AddColumn(interface.convertArray(self.arrs[1], self.titles[1]))
        self.table.AddColumn(interface.convertArray(self.arrs[2], self.titles[2]))
        return

    def check_data_fidelity(self, ido, checkme, points=False):
        """`TableToTimeGrid`: data fidelity"""
        wido = dsa.WrapDataObject(ido)
        for i, title in enumerate(self.titles):
            if points:
                arr = wido.PointData[title]
            else:
                arr = wido.CellData[title]
            self.assertTrue(np.allclose(arr, checkme[i], rtol=RTOL))

    def test_simple(self):
        """`TableToTimeGrid`: check simple"""
        # Use filter
        f = TableToTimeGrid()
        f.SetInputDataObject(self.table)
        f.set_dimensions(0, 1, 2, 3)
        f.set_extent(20, 2, 5, 2)
        f.set_spacing(5, 5, 5)
        f.set_origin(3.3, 6.0, 7)
        f.set_use_points(False)
        f.set_order('C')
        for t in range(2):
            f.UpdateTimeStep(t)
            ido = f.GetOutput()
            checkme = [None] * len(self.arrs)
            for i, arr in enumerate(self.arrs):
                a = arr.reshape((20, 2, 5, 2))[:,:,:,t]
                checkme[i] = a.flatten(order='F') # Order F because in XYZ format
            self.check_data_fidelity(ido, checkme, points=False)
        f.set_use_points(True)
        f.Update()
        for t in range(2):
            f.UpdateTimeStep(t)
            ido = f.GetOutput()
            checkme = [None] * len(self.arrs)
            for i, arr in enumerate(self.arrs):
                a = arr.reshape((20, 2, 5, 2))[:,:,:,t]
                checkme[i] = a.flatten(order='F') # Order F because in XYZ format
            self.check_data_fidelity(ido, checkme, points=True)
        return


    def test_seplib(self):
        """`TableToTimeGrid`: check a SEPLib ordered array"""
        def sepit(a):
            a = a.swapaxes(0, 2)
            a = a.swapaxes(0, 1)
            return a

        # Use filter
        f = TableToTimeGrid()
        f.SetInputDataObject(self.table)
        f.set_dimensions(1, 2, 0, 3)
        f.set_extent(20, 2, 5, 2)
        f.set_spacing(5, 5, 5)
        f.set_origin(3.3, 6.0, 7)
        f.set_use_points(False)
        f.set_order('F')
        for t in range(2):
            f.UpdateTimeStep(t)
            ido = f.GetOutput()
            self.assertEqual(ido.GetDimensions(), (3, 6, 21))
            checkme = [None] * len(self.arrs)
            for i, arr in enumerate(self.arrs):
                a = arr.reshape((20, 2, 5, 2), order='F')[:,:,:,t]
                a = sepit(a)
                checkme[i] = a.flatten(order='F') # Order F because in XYZ format

            self.check_data_fidelity(ido, checkme, points=False)
        f.set_use_points(True)
        f.Update()
        for t in range(2):
            f.UpdateTimeStep(t)
            ido = f.GetOutput()
            self.assertEqual(ido.GetDimensions(), (2, 5, 20))
            checkme = [None] * len(self.arrs)
            for i, arr in enumerate(self.arrs):
                a = arr.reshape((20, 2, 5, 2), order='F')[:,:,:,t]
                a = sepit(a)
                checkme[i] = a.flatten(order='F') # Order F because in XYZ format
            self.check_data_fidelity(ido, checkme, points=True)
        return





###############################################################################

class TestReverseImageDataAxii(TestBase):
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
        data = interface.convertArray(arr.flatten(), name='Data', deep=True)
        cellData = interface.convertArray(arrCells.flatten(), name='CellData', deep=True)
        image.GetPointData().AddArray(data)
        image.GetCellData().AddArray(cellData)
        # Now perfrom the reverse for only X:
        f = ReverseImageDataAxii()
        f.SetInputDataObject(image)
        f.set_flip_x(True)
        f.set_flip_y(False)
        f.set_flip_z(False)
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
        f.set_flip_x(True)
        f.set_flip_y(True)
        f.set_flip_z(True)
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


###############################################################################

class TestTranslateGridOrigin(TestBase):
    """
    Test the `TranslateGridOrigin` filter
    """
    def setUp(self):
        TestBase.setUp(self)
        # Create some input tables
        self.idi = vtk.vtkImageData()
        self.idi.SetDimensions(20, 2, 10)
        self.idi.SetSpacing(1, 1, 1)
        self.idi.SetOrigin(100, 100, 100)
        # Populate the tables
        self.n = 400
        self.title = 'Array 0'
        self.arr = np.random.random(self.n)
        self.idi.GetPointData().AddArray(interface.convertArray(self.arr, self.title))
        return

    def test_all(self):
        """`TranslateGridOrigin`: make sure works"""
        f = TranslateGridOrigin()
        f.SetInputDataObject(self.idi)
        f.set_corner(1)
        f.Update()
        ido = f.GetOutput()
        ox, oy, oz = ido.GetOrigin()
        self.assertEqual(ox, 100-19)
        self.assertEqual(oy, 100)
        self.assertEqual(oz, 100)
        f.set_corner(2)
        f.Update()
        ido = f.GetOutput()
        ox, oy, oz = ido.GetOrigin()
        self.assertEqual(ox, 100)
        self.assertEqual(oy, 100-1)
        self.assertEqual(oz, 100)
        f.set_corner(3)
        f.Update()
        ido = f.GetOutput()
        ox, oy, oz = ido.GetOrigin()
        self.assertEqual(ox, 100-19)
        self.assertEqual(oy, 100-1)
        self.assertEqual(oz, 100)
        f.set_corner(4)
        f.Update()
        ido = f.GetOutput()
        ox, oy, oz = ido.GetOrigin()
        self.assertEqual(ox, 100)
        self.assertEqual(oy, 100)
        self.assertEqual(oz, 100-9)
        f.set_corner(5)
        f.Update()
        ido = f.GetOutput()
        ox, oy, oz = ido.GetOrigin()
        self.assertEqual(ox, 100-19)
        self.assertEqual(oy, 100)
        self.assertEqual(oz, 100-9)
        f.set_corner(6)
        f.Update()
        ido = f.GetOutput()
        ox, oy, oz = ido.GetOrigin()
        self.assertEqual(ox, 100)
        self.assertEqual(oy, 100-1)
        self.assertEqual(oz, 100-9)
        f.set_corner(7)
        f.Update()
        ido = f.GetOutput()
        ox, oy, oz = ido.GetOrigin()
        self.assertEqual(ox, 100-19)
        self.assertEqual(oy, 100-1)
        self.assertEqual(oz, 100-9)


###############################################################################


class TestSurferGridReader(TestBase):
    """
    Test the `SurferGridReader` and `WriteImageDataToSurfer`
    """
    def setUp(self):
        TestBase.setUp(self)
        self.test_dir = tempfile.mkdtemp()
        self.filename = os.path.join(os.path.dirname(__file__), 'data/surfer-grid.grd')


    def tearDown(self):
        # Remove the test data directory after the test
        shutil.rmtree(self.test_dir)
        TestBase.tearDown(self)


    def test(self):
        """`SurferGridReader` and `WriteImageDataToSurfer`: Test reader and writer for Surfer format"""
        reader = SurferGridReader()
        reader.AddFileName(self.filename)
        reader.set_data_name('foo')
        reader.Update()
        img = reader.GetOutput()
        self.assertIsNotNone(img)
        # Check shapes of the surfer grid
        nx, ny, nz = img.GetDimensions()
        self.assertEqual(nx, 222)
        self.assertEqual(ny, 182)
        self.assertEqual(nz, 1)

        # Now test writer
        writer = WriteImageDataToSurfer()
        filename = os.path.join(self.test_dir, 'test-writer.grd')
        writer.SetFileName(filename)
        writer.Write(img, 'foo')

        # Read again and compare
        reader = SurferGridReader()
        reader.AddFileName(filename)
        reader.set_data_name('foo2')
        reader.Update()
        read = reader.GetOutput()
        self.assertIsNotNone(read)
        nx, ny, nz = read.GetDimensions()
        self.assertEqual(nx, 222)
        self.assertEqual(ny, 182)
        self.assertEqual(nz, 1)
        self.assertEqual(img.GetBounds(), read.GetBounds())
        # Check the data arrays
        imgArr = dsa.WrapDataObject(img).PointData['foo']
        readArr = dsa.WrapDataObject(read).PointData['foo2']
        self.assertTrue(np.allclose(imgArr, readArr))
        return



###############################################################################


class TestExtractTopography(TestBase):
    """
    Test the `ExtractTopography` filter
    """
    def setUp(self):
        TestBase.setUp(self)
        # create a volumetric data set
        self.grid = PVGeo.model_build.CreateTensorMesh().apply()
        # create an unudulating surface in the grid domain
        #   make XY random in the grid bounds
        #   make Z ranome within a very small domain inside the grid
        bnds = self.grid.GetBounds()
        x = np.random.uniform(bnds[0], bnds[1], 5000)
        y = np.random.uniform(bnds[2], bnds[3], 5000)
        z = np.random.uniform(-200, -100, 5000)
        self.points = interface.pointsToPolyData(np.c_[x,y,z])

    def test_simple_run(self):
        """`ExtractTopography`: Test extraction on simple data"""
        # Produce some input data
        data = vtk.vtkImageData()
        data.SetOrigin(0.0, 0.0, 0.0)
        data.SetSpacing(5.0, 5.0, 5.0)
        data.SetDimensions(20, 20, 20)
        x = y = np.linspace(0, 100, num=50, dtype=float)
        g = np.meshgrid(x, y)
        # Convert to XYZ points
        points = np.vstack(map(np.ravel, g)).T
        z = np.reshape(np.full(len(points), 55.0), (len(points), -1))
        #z = np.reshape(np.random.uniform(low=55.0, high=65.0, size=(len(points),)), (len(points), -1))
        points = np.concatenate((points, z), axis=1)
        topo = interface.pointsToPolyData(points)


        # # apply filter
        f = ExtractTopography()
        grd = f.apply(data, topo)

        # Test the output
        self.assertIsNotNone(grd)
        self.assertEqual(grd.GetDimensions(), data.GetDimensions())
        self.assertEqual(grd.GetSpacing(), data.GetSpacing())
        self.assertEqual(grd.GetOrigin(), data.GetOrigin())
        # Now check the active topo cell data?
        # TODO: implement
        active = dsa.WrapDataObject(grd).CellData['Extracted']
        for i in range(grd.GetNumberOfCells()):
            cell = grd.GetCell(i)
            bounds = cell.GetBounds()
            z = bounds[5]#(bounds[4]+bounds[5])/2.0
            if z <= 55.0:
                self.assertTrue(active[i])
            elif z > 55.0:
                self.assertFalse(active[i])
            else:
                self.fail(msg='Non-testable cell encountered')

        return


    def test_underneath(self):
        """`ExtractTopography`: Test extraction on underneath surface"""
        extracted = ExtractTopography(op='underneath').apply(self.grid, self.points)


    def test_intersection(self):
        """`ExtractTopography`: Test extraction on surface"""
        extracted = ExtractTopography(op='intersection', tolerance=50).apply(self.grid, self.points)

    def test_shifted_surface(self):
        """`ExtractTopography`: Test extraction for shifted surface"""
        extracted = ExtractTopography(op='intersection', tolerance=50, offset=-250).apply(self.grid, self.points)


class TestCellCenterWriter(TestBase):
    """
    Test the `WriteCellCenterData`
    """
    def setUp(self):
        TestBase.setUp(self)
        self.test_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.test_dir, 'test.txt')


    def tearDown(self):
        # Remove the test data directory after the test
        shutil.rmtree(self.test_dir)
        TestBase.tearDown(self)


    def test(self):
        """`SurferGridReader` and `WriteImageDataToSurfer`: Test reader and writer for Surfer format"""
        # create some input datasets
        grid0 = PVGeo.model_build.CreateTensorMesh().apply()
        grid1 = PVGeo.model_build.CreateEvenRectilinearGrid().apply()

        # make a composite dataset
        comp = vtk.vtkMultiBlockDataSet()
        comp.SetBlock(0, grid0)
        comp.SetBlock(1, grid1)


        # test the wirter
        writer = WriteCellCenterData()
        filename = os.path.join(self.filename)
        writer.SetFileName(filename)
        writer.Write(comp)


###############################################################################

class TestEsriGridReader(TestBase):
    """
    Test the `EsriGridReader`
    """
    def setUp(self):
        TestBase.setUp(self)
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.test_dir, 'test.dat')
        sample = """ncols         4
nrows         6
xllcorner     100.0
yllcorner     50.0
cellsize      50.0
NODATA_value  -9999
-9999 -9999 5 2
-9999 20 100 36
3 8 35 10
32 42 50 6
88 75 27 9
13 5 1 -9999
"""
        with open(self.filename, 'w') as f:
            f.write(sample)


    def tearDown(self):
        # Remove the test data directory after the test
        shutil.rmtree(self.test_dir)
        TestBase.tearDown(self)

    ###########################################

    def test_read(self):
        """`EsriGridReader`: Test the read"""
        reader = EsriGridReader()
        reader.AddFileName(self.filename)
        reader.Update()
        img = reader.GetOutput()
        # Test data object
        self.assertIsNotNone(img)
        nx, ny, nz = img.GetDimensions()
        self.assertEqual(nx, 4)
        self.assertEqual(ny, 6)
        dx, dy, dz = img.GetSpacing()
        self.assertTrue(50.0 == dx == dy == dz)
        ox, oy, oz = img.GetOrigin()
        self.assertEqual(ox, 100.0)
        self.assertEqual(oy, 50.0)
        self.assertEqual(oz, 0.0)
        return

    # def test_read_big(self):
    #     """`EsriGridReader`: Test the read"""
    #     reader = EsriGridReader()
    #     reader.AddFileName('/Users/bane/Documents/OpenGeoVis/Data/data-testing/Readers/ESRI/DEM/la1.dem')
    #     reader.Update()
    #     img = reader.GetOutput()
    #     # Test data object
    #     self.assertIsNotNone(img)
    #     nx, ny, nz = img.GetDimensions()
    #     self.assertEqual(nx, 7317)
    #     self.assertEqual(ny, 8160)
    #     dx, dy, dz = img.GetSpacing()
    #     self.assertTrue(3.0 == dx == dy == dz)
    #     ox, oy, oz = img.GetOrigin()
    #     self.assertTrue(abs(ox - 385440.22544667) < RTOL)
    #     self.assertTrue(abs(oy - 3729089.022415) < RTOL)
    #     self.assertEqual(oz, 0.0)
    #     return


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
