`import unittest
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

class TestwsMesh3DReader(unittest.TestCase):
    """
    Test the `wsMesh3DReader`
    """
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        # TODO: parameters
        self.x0 = 150.0
        self.y0 = 250.0
        self.z0 = -200.0
        self.rot = 45.0
        ##### Now generate output for testing ####
        fname = os.path.join(self.test_dir, 'test.ws3d')
        #self.data = np.random.random(100)
        # TODO: write out a temporary file to test the reader

        # Set up the reader
        reader = wsMesh3DReader()
        reader.AddFileName(fname)

        # TODO: Edit Parameters as needed:
        reader.SetAngle(self.rot)
        reader.SetOrigin(self.x0, self.y0, self.z0)

        # Perform the read
        # TODO: reader.Update() # NOTE: BE SURE TO UNCOMMENT THIS LINE
        self.GRID = reader.GetOutputDataObject(0)
        return

    def tearDown(self):
        # Remove the test data directory after the test
        shutil.rmtree(self.test_dir)

    ###########################################

    def test_data_fidelity(self):
        """Test `wsMesh3DReader`: check data fidelity"""
        self.assertTrue(False)

    def test_shape(self):
        """Test `wsMesh3DReader`: check output grid's shape"""
        self.assertTrue(False)

    def test_spatial_reference(self):
        """Test `wsMesh3DReader`: check output grid's spatial reference"""
        bounds = self.GRID.GetBounds()
        corner = (bounds[0], bounds[2], bounds[4]) # TODO: maybe change Z to 5th index?
        self.assertEqual(corner, (self.x0, self.y0, self.z0))
