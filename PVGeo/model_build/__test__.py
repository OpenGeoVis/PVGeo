import unittest
import numpy as np

# VTK imports:
import vtk
from vtk.util import numpy_support as nps
from vtk.numpy_interface import dataset_adapter as dsa

# Functionality to test:
from .earth import *
from .evenModel import *
from .oddModel import *

###############################################################################

class TestEarthSource(unittest.TestCase):
    """
    Test the `EarthSource` source
    """

    def test_(self):
        self.assertTrue(False)


###############################################################################

class TestCreateUniformGrid(unittest.TestCase):
    """
    Test the `CreateUniformGrid` source
    """

    def test_(self):
        self.assertTrue(False)


###############################################################################

class TestCreateEvenRectilinearGrid(unittest.TestCase):
    """
    Test the `CreateEvenRectilinearGrid` source
    """

    def test_(self):
        self.assertTrue(False)


###############################################################################

class TestCreateTensorMesh(unittest.TestCase):
    """
    Test the `CreateTensorMesh` source
    """

    def test_(self):
        self.assertTrue(False)


###############################################################################
