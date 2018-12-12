__all__ = [
    'GSLibReader',
    'WriteTableToGSLib',
]

__displayname__ = 'GSLib/GeoEAS File I/O'

import numpy as np
import vtk
import os

from ..readers import DelimitedTextReader
from ..base import WriterBase
from .. import _helpers
from .. import interface


class GSLibReader(DelimitedTextReader):
    """Reads a GSLIB file format to a ``vtkTable``. The GSLIB file format has
    headers lines followed by the data as a space delimited ASCI file (this
    filter is set up to allow you to choose any single character delimiter).
    The first header line is the title and will be printed to the console.
    This line may have the dimensions for a grid to be made of the data.
    The second line is the number (n) of columns of data. The next n lines are
    the variable names for the data in each column. You are allowed up to ten
    characters for the variable name. The data follow with a space between each
    field (column).
    """
    __displayname__ = 'GSLib Table Reader'
    __category__ = 'reader'
    extensions = 'sgems dat geoeas gslib GSLIB txt SGEMS SGeMS'
    description = 'PVGeo: GSLib Table'
    def __init__(self, outputType='vtkTable', **kwargs):
        DelimitedTextReader.__init__(self, outputType=outputType, **kwargs)
        self.SetSplitOnWhiteSpace(True)
        # These are attributes the derived from file contents:
        self.__header = None

    def _ExtractHeader(self, content):
        self.__header = content[0]
        try:
            num = int(content[1]) # number of data columns
        except ValueError:
            raise _helpers.PVGeoError('This file is not in proper GSLIB format.')
        titles = [ln.rstrip('\r\n') for ln in content[2:2+num]]
        return titles, content[2 + num::]


    #### Seters and Geters ####

    def GetFileHeader(self):
        """Returns the file header. If file hasn't been read, returns ``None``
        """
        return self.__header


class WriteTableToGSLib(WriterBase):
    """Write the row data in a ``vtkTable`` to the GSLib Format"""
    __displayname__ = 'Write ``vtkTable`` To GSLib Format'
    __category__ = 'writer'
    def __init__(self, inputType='vtkTable'):
        WriterBase.__init__(self, inputType=inputType, ext='gslib')
        self.__header = 'Data saved by PVGeo'


    def PerformWriteOut(self, inputDataObject, filename, objectName):
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
