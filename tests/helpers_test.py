from base import TestBase
import numpy as np
import pandas as pd

# VTK imports:
import vtk
from vtk.numpy_interface import dataset_adapter as dsa

# Functionality to test:
from PVGeo._helpers import xml
from PVGeo import _helpers
from PVGeo import interface


RTOL = 0.000001

class TestXML(TestBase):
    """
    Test the XML Helpers to make sure no errors are thrown
    """

    def test_simple(self):
        """XML: Make sure no errors arise"""
        x = xml.getPythonPathProperty()
        x = xml.getReaderTimeStepValues('txt dat', 'A description')
        m = xml.getVTKTypeMap()
        self.assertEqual(m['vtkUnstructuredGrid'], 4)
        x = xml.getPropertyXml('foo', 'SetFoo', 4, panel_visibility='default', help='foo help')
        x = xml.getPropertyXml('foo', 'SetFoo', True, panel_visibility='default', help='foo help')
        x = xml.getFileReaderXml('txt dat', reader_description='desc!!', command="AddFileName")
        x = xml.getDropDownXml('foo', 'SetFoo', ['foo1', 'foo2'], help='Help the foo', values=[1, 2])
        x = xml.getInputArrayXml(labels=['foo'], nInputPorts=1, n_arrays=1, input_names='Input')

        return


class TestDataFrameConversions(TestBase):
    """
    Test the pandas DataFrames conversions to VTK data objects
    """

    def test_df_to_table(self):
        """`tableToDataFrame`: test interface conversion for tables"""
        names = ['x', 'y', 'z', 'a', 'b']
        data = np.random.rand(100, len(names))
        df = pd.DataFrame(data=data, columns=names)
        table = vtk.vtkTable()
        interface.dataFrameToTable(df, table)
        wtbl = dsa.WrapDataObject(table)
        # Now check the vtkTable
        for i, name in enumerate(names):
            # Check data aray names
            self.assertEqual(table.GetColumnName(i), name)
            # Check data contents
            arr = wtbl.RowData[name]
            self.assertTrue(np.allclose(arr, df[name].values, rtol=RTOL))

        # Now test backwards compatability
        dfo = interface.tableToDataFrame(table)
        self.assertTrue(df.equals(dfo))
        return




###############################################################################
###############################################################################
###############################################################################
if __name__ == '__main__':
    import unittest
    unittest.main()
###############################################################################
###############################################################################
###############################################################################
