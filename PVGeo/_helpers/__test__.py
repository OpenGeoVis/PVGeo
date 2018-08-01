import unittest
import numpy as np

# VTK imports:
import vtk
from vtk.util import numpy_support as nps
from vtk.numpy_interface import dataset_adapter as dsa
from .. import _helpers

# Functionality to test:
from . import xml

class TestTableToGrid(unittest.TestCase):
    """
    Test the XML Helpers to make sure no errors are thrown
    """

    def test_simple(self):
        """XML: Make sure no errors arise"""
        x = xml.getPythonPathProperty()
        x = xml.getReaderTimeStepValues('txt dat', 'A description')
        m = xml.getVTKTypeMap()
        self.assertEqual(m['vtkUnstructuredGrid'], 4)
        x = xml.getPropertyXml('foo', 'SetFoo', 4, visibility='default', help='foo help')
        x = xml.getPropertyXml('foo', 'SetFoo', True, visibility='default', help='foo help')
        x = xml.getFileReaderXml('txt dat', readerDescription='desc!!', command="AddFileName")
        x = xml.getDropDownXml('foo', 'SetFoo', ['foo1', 'foo2'], help='Help the foo', values=[1, 2])
        x = xml.getInputArrayXml(labels=['foo'], nInputPorts=1, numArrays=1, inputNames='Input')

        return
