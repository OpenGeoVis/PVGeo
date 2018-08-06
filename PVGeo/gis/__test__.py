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
from .__init__ import *


RTOL = 0.000001

###############################################################################

class TestGSLibReader(unittest.TestCase):
    """
    Test the `EsriGridReader`
    """
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.fname = os.path.join(self.test_dir, 'test.dat')
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
        with open(self.fname, 'w') as f:
            f.write(sample)


    def tearDown(self):
        # Remove the test data directory after the test
        shutil.rmtree(self.test_dir)

    ###########################################

    def test_read(self):
        """`EsriGridReader`: Test the read"""
        reader = EsriGridReader()
        reader.AddFileName(self.fname)
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
