__all__ = [
    'WriteCellCenterData',
]

import vtk
import numpy as np
from vtk.numpy_interface import dataset_adapter as dsa

from ..base import WriterBase

#------------------------------------------------------------------------------

class WriteCellCenterData(WriterBase):
    """This writer will save a file of the XYZ points for an input dataset's
    cell centers and its cell data. Use in tandom with ParaView's native CSV
    writer which saves the PointData.
    """
    __displayname__ = 'Write Cell Centers To CSV'
    __category__ = 'writer'
    def __init__(self):
        WriterBase.__init__(self, inputType='vtkDataSet')
        self.__delimiter = ','


    def PerformWriteOut(self, inputDataObject, filename):
        # Find cell centers
        filt = vtk.vtkCellCenters()
        filt.SetInputDataObject(inputDataObject)
        filt.Update()
        centers = dsa.WrapDataObject(filt.GetOutput(0)).Points
        # Get CellData
        wpdi = dsa.WrapDataObject(inputDataObject)
        celldata = wpdi.CellData
        keys = celldata.keys()
        # Save out using numpy
        arr = np.zeros((len(centers), 3 + len(keys)))
        arr[:,0:3] = centers
        for i, name in enumerate(keys):
            arr[:,i+3] = celldata[name]
        # Now write out the data
        # Clean data titles to make sure they do not contain the delimiter
        repl = '_' if self.__delimiter != '_' else '-'
        for i, name in enumerate(keys):
            keys[i] = name.replace(self.__delimiter, repl)
        header = ('%s' % self.__delimiter).join(['X', 'Y', 'Z'] + keys)
        np.savetxt(filename, arr,
                   header=header,
                   delimiter=self.__delimiter,
                   fmt=self.GetFormat(),
                   comments='')
        # Success for pipeline
        return 1

    def SetDelimiter(self, delimiter):
        """The string delimiter to use"""
        if self.__delimiter != delimiter:
            self.__delimiter = delimiter
            self.Modified()
