import unittest
import numpy as np

# VTK imports:
import vtk
from vtk.util import numpy_support as nps
from vtk.numpy_interface import dataset_adapter as dsa

# Functionality to test:
from .reverse_axii import *
from .table2grid import *
from .trans_origin import *

###############################################################################

class TestTableToGrid(unittest.TestCase):
    """
    Test the `TableToGrid` filter
    """

    def test_(self):
        self.assertTrue(False)


###############################################################################

class TestReverseImageDataAxii(unittest.TestCase):
    """
    Test the `ReverseImageDataAxii` filter
    """

    def test_(self):
        self.assertTrue(False)


###############################################################################

class TestTranslateGridOrigin(unittest.TestCase):
    """
    Test the `TranslateGridOrigin` filter
    """

    def test_(self):
        self.assertTrue(False)


###############################################################################
