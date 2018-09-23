__all__ = [
    'WriteTableToGSLib',
    'WriteImageDataToSGeMS',
]

import numpy as np
import vtk
import os


from ..base import WriterBase
from .. import _helpers
from .. import interface


class WriteTableToGSLib(WriterBase):
    """Write the row data in a ``vtkTable`` to the GSLib Format"""
    __displayname__ = 'Write ``vtkTable`` To GSLib Format'
    __category__ = 'writer'
    def __init__(self, inputType='vtkTable'):
        WriterBase.__init__(self, inputType=inputType, ext='gslib')
        self.__header = 'Data saved by PVGeo'


    def PerformWriteOut(self, inputDataObject, filename):
        # Get the input data object
        table = inputDataObject

        numArrs = table.GetRowData().GetNumberOfArrays()
        arrs = []

        titles = []
        # Get data arrays
        for i in range(numArrs):
            vtkarr = table.GetRowData().GetArray(i)
            arrs.append(interface.convertArray(vtkarr))
            titles.append(vtkarr.GetName())

        header = '%s\n' % self.__header
        header += '%d\n' % len(titles)
        datanames = '\n'.join(titles)
        header += datanames

        arrs = np.array(arrs).T
        np.savetxt(filename, arrs, comments='', header=header, fmt=self.GetFormat())

        return 1


    def SetHeader(self, header):
        """Set the file header string"""
        if self.__header != header:
            self.__header = header
            self.Modified()





class WriteImageDataToSGeMS(WriterBase):
    """Writes a ``vtkImageData`` object to the SGeMS uniform grid format.
    This writer can only handle point data.
    """
    __displayname__ = 'Write ``vtkImageData`` To SGeMS Grid Format'
    __category__ = 'writer'
    def __init__(self, inputType='vtkImageData'):
        WriterBase.__init__(self, inputType=inputType, ext='SGeMS')


    def PerformWriteOut(self, inputDataObject, filename):
        # Get the input data object
        grd = inputDataObject

        # Get grid dimensions
        nx, ny, nz = grd.GetDimensions()

        numArrs = grd.GetPointData().GetNumberOfArrays()
        arrs = []

        titles = []
        # Get data arrays
        for i in range(numArrs):
            vtkarr = grd.GetPointData().GetArray(i)
            arrs.append(interface.convertArray(vtkarr))
            titles.append(vtkarr.GetName())

        header = '%d %d %d\n' % (nx, ny, nz)
        header += '%d\n' % len(titles)
        datanames = '\n'.join(titles)
        header += datanames

        arrs = np.array(arrs).T
        np.savetxt(filename, arrs, comments='', header=header, fmt=self.GetFormat())

        return 1
