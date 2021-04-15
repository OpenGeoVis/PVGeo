import numpy as np
import pandas as pd

# VTK imports:
import vtk
from vtk.numpy_interface import dataset_adapter as dsa

from base import TestBase
from PVGeo import interface

# Functionality to test:
from PVGeo._helpers import xml

RTOL = 0.000001


class TestXML(TestBase):
    """
    Test the XML Helpers to make sure no errors are thrown
    """

    def test_simple(self):
        """XML: Make sure no errors arise"""
        _ = xml.get_python_path_property()
        _ = xml.get_reader_time_step_values('txt dat', 'A description')
        m = xml.get_vtk_type_map()
        self.assertEqual(m['vtkUnstructuredGrid'], 4)
        _ = xml.get_property_xml(
            'foo', 'SetFoo', 4, panel_visibility='default', help='foo help'
        )
        _ = xml.get_property_xml(
            'foo', 'SetFoo', True, panel_visibility='default', help='foo help'
        )
        _ = xml.get_file_reader_xml(
            'txt dat', reader_description='desc!!', command="AddFileName"
        )
        _ = xml.get_drop_down_xml(
            'foo', 'SetFoo', ['foo1', 'foo2'], help='Help the foo', values=[1, 2]
        )
        _ = xml.get_input_array_xml(
            labels=['foo'], nInputPorts=1, n_arrays=1, input_names='Input'
        )
        return


class TestDataFrameConversions(TestBase):
    """
    Test the pandas DataFrames conversions to VTK data objects
    """

    def test_df_to_table(self):
        """`table_to_data_frame`: test interface conversion for tables"""
        names = ['x', 'y', 'z', 'a', 'b']
        data = np.random.rand(100, len(names))
        df = pd.DataFrame(data=data, columns=names)
        table = vtk.vtkTable()
        interface.data_frame_to_table(df, table)
        wtbl = dsa.WrapDataObject(table)
        # Now check the vtkTable
        for i, name in enumerate(names):
            # Check data aray names
            self.assertEqual(table.GetColumnName(i), name)
            # Check data contents
            arr = wtbl.RowData[name]
            self.assertTrue(np.allclose(arr, df[name].values, rtol=RTOL))

        # Now test backwards compatability
        dfo = interface.table_to_data_frame(table)
        # self.assertTrue(df.equals(dfo)) # Sorting is different on Py2.7 and 3.5
        for name in dfo.keys():
            self.assertTrue(np.allclose(df[name], dfo[name], rtol=RTOL))
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
