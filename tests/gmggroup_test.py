import unittest
import os

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
            self.fname = os.path.join(os.path.dirname(__file__), 'data/test_file.omf')


        def test_read_project(self):
            """`OMFReader`: read whole project file"""
            proj = OMFReader().Apply(self.fname)
            self.assertIsNotNone(proj)
            self.assertEqual(proj.GetNumberOfBlocks(), 9)
