import unittest
import shutil
import tempfile
import os
import numpy as np

# VTK imports:
from vtk.util import numpy_support as nps

from .. import _helpers
# Functionality to test:
from .reader import *


RTOL = 0.000001

###############################################################################

class TestOMFReader(unittest.TestCase):
    """
    Test the `OMFReader`
    """

    def test_commpile(self):
        """Simply makes sure code compiles"""
        reader = OMFReader()
        return
