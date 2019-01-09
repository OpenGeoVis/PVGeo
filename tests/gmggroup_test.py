import unittest
import shutil
import tempfile
import os
import numpy as np

from six.moves import urllib

DATA_URL = "https://raw.githubusercontent.com/gmggroup/omf/master/assets/test_file.omf"


# VTK imports:
from vtk.util import numpy_support as nps

from PVGeo import _helpers

omf_avail = False
try:
    # Functionality to test:
    from PVGeo.gmggroup import *
except ImportError:
    pass
else:
    omf_avail = True


RTOL = 0.000001

###############################################################################

if omf_avail:
    class TestOMFReader(unittest.TestCase):
        """
        Test the `OMFReader`
        """

        def setUp(self):
            self.test_dir = tempfile.mkdtemp()
            self.fname = os.path.join(self.test_dir, 'test_file.omf')
            urllib.request.urlretrieve(DATA_URL, self.fname)

        def tearDown(self):
            # Remove the test data directory after the test
            shutil.rmtree(self.test_dir)

        def test_read_project(self):
            proj = OMFReader().Apply(self.fname)
            self.assertIsNotNone(proj)
            self.assertEqual(proj.GetNumberOfBlocks(), 9)
