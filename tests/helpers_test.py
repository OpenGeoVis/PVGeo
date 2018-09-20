import unittest
import numpy as np
import pandas as pd

# VTK imports:
import vtk
from vtk.numpy_interface import dataset_adapter as dsa

# Functionality to test:
from PVGeo._helpers import xml
from PVGeo import _helpers


RTOL = 0.000001

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


class TestDataFrameConversions(unittest.TestCase):
    """
    Test the pandas DataFrames conversions to VTK data objects
    """

    def test_df_to_table(self):
        names = ['x', 'y', 'z', 'a', 'b']
        data = np.random.rand(100, len(names))
        df = pd.DataFrame(data=data, columns=names)
        table = vtk.vtkTable()
        _helpers.DataFrameToTable(df, table)
        wtbl = dsa.WrapDataObject(table)
        # Now check the vtkTable
        for i, name in enumerate(names):
            # Check data aray names
            self.assertEqual(table.GetColumnName(i), name)
            # Check data contents
            arr = wtbl.RowData[name]
            self.assertTrue(np.allclose(arr, df[name].values, rtol=RTOL))




###############################################################################
###############################################################################
###############################################################################
if __name__ == '__main__':
    unittest.main()
###############################################################################
###############################################################################
###############################################################################
