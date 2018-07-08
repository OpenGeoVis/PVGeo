import unittest
import warnings
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
        # TODO: write out a temporary file to test the reader
        """# Script for making a test file:
        # Adopted from: http://docs.simpeg.xyz/content/examples/08-nsem/plot_foward_MTTipper3D.html#sphx-glr-content-examples-08-nsem-plot-foward-mttipper3d-py
        import SimPEG as simpeg
        from SimPEG.EM import NSEM
        import numpy as np

        # Make a mesh
        M = simpeg.Mesh.TensorMesh(
            [
                [(100, 9, -1.5), (100., 13), (100, 9, 1.5)],
                [(100, 9, -1.5), (100., 13), (100, 9, 1.5)],
                [(50, 10, -1.6), (50., 10), (50, 6, 2)]
            ], x0=['C', 'C', -14926.8217]
        )
        # Setup the model
        conds = [1,1e-2]
        sig = simpeg.Utils.ModelBuilder.defineBlock(
            M.gridCC, [-100, -100, -350], [100, 100, -150], conds
        )
        sig[M.gridCC[:, 2] > 0] = 1e-8
        sig[M.gridCC[:, 2] < -1000] = 1e-1
        sigBG = np.zeros(M.nC) + conds[1]
        sigBG[M.gridCC[:, 2] > 0] = 1e-8

        # Now saveout
        import PVGeo
        PVGeo.ws3d._write_ws3d(fname, M, sig)
        """

        # Set up the reader
        reader = wsMesh3DReader()
        reader.AddFileName(fname)

        # TODO: Edit Parameters as needed:
        reader.SetAngle(self.rot)
        reader.SetOrigin(self.x0, self.y0, self.z0)

        # Perform the read
        # TODO: reader.Update() # NOTE: BE SURE TO UNCOMMENT THIS LINE
        self.GRID = reader.GetOutput()
        return

    def tearDown(self):
        # Remove the test data directory after the test
        shutil.rmtree(self.test_dir)

    ###########################################

    def test_data_fidelity(self):
        """`wsMesh3DReader`: check data fidelity"""
        # self.assertTrue(False)
        warnings.warn('`wsMesh3DReader`: not fully implemented')

    def test_shape(self):
        """`wsMesh3DReader`: check output grid's shape"""
        # self.assertTrue(False)
        warnings.warn('`wsMesh3DReader`: not fully implemented')

    def test_spatial_reference(self):
        """`wsMesh3DReader`: check output grid's spatial reference"""
        # bounds = self.GRID.GetBounds()
        # corner = (bounds[0], bounds[2], bounds[4]) # TODO: maybe change Z to 5th index?
        # self.assertEqual(corner, (self.x0, self.y0, self.z0))
        warnings.warn('`wsMesh3DReader`: not fully implemented')
