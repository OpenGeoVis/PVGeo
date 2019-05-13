__all__ = [
    'GSLibReader',
    'GSLibPointSetReader',
    'WriteTableToGSLib',
]

__displayname__ = 'GSLib/GeoEAS File I/O'

import numpy as np
import os

from ..readers import DelimitedTextReader, DelimitedPointsReaderBase
from ..base import WriterBase
from .. import _helpers
from .. import interface


class _GSLibReaderMethods(object):
    """A helper class to handle overriding of delimited text reading methods
    for all GSLib readers."""
    # NOTE: order of inherritance matters ALOT!
    _header = None
    extensions = 'sgems dat geoeas gslib GSLIB txt SGEMS SGeMS'

    def _extract_header(self, content):
        self._header = content[0]
        try:
            num = int(content[1]) # number of data columns
        except ValueError:
            raise _helpers.PVGeoError('This file is not in proper GSLIB format.')
        titles = [ln.rstrip('\r\n') for ln in content[2:2+num]]
        return titles, content[2 + num::]


    #### Seters and Geters ####

    def get_file_header(self):
        """Returns the file header. If file hasn't been read, returns ``None``
        """
        return self._header

class GSLibReader(_GSLibReaderMethods, DelimitedTextReader):
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
    description = 'PVGeo: GSLib Table'
    def __init__(self, outputType='vtkTable', **kwargs):
        DelimitedTextReader.__init__(self, outputType=outputType, **kwargs)
        self.set_split_on_white_space(True)


class GSLibPointSetReader(_GSLibReaderMethods, DelimitedPointsReaderBase):
    """Reads a GSLib point set file where the first three columns are the XYZ
    coordinates and the remainder of the data is consistent with the
    :class:`GSLibReader` specifications."""
    __displayname__ = 'GSLib Point Set Reader'
    __category__ = 'reader'
    description = 'PVGeo: GSLib Point Set'
    extensions = _GSLibReaderMethods.extensions + 'gslibpts ptset gpts'
    def __init__(self, **kwargs):
        DelimitedPointsReaderBase.__init__(self, **kwargs)
        self.set_split_on_white_space(True)



class WriteTableToGSLib(WriterBase):
    """Write the row data in a ``vtkTable`` to the GSLib Format"""
    __displayname__ = 'Write ``vtkTable`` To GSLib Format'
    __category__ = 'writer'
    def __init__(self, inputType='vtkTable'):
        WriterBase.__init__(self, inputType=inputType, ext='gslib')
        self._header = 'Data saved by PVGeo'


    def perform_write_out(self, input_data_object, filename, object_name):
        """Write out the input data object to the GSLib file format"""
        # Get the input data object
        table = input_data_object

        numArrs = table.GetRowData().GetNumberOfArrays()
        arrs = []

        titles = []
        # Get data arrays
        for i in range(numArrs):
            vtkarr = table.GetRowData().GetArray(i)
            arrs.append(interface.convert_array(vtkarr))
            titles.append(vtkarr.GetName())

        header = '%s\n' % self._header
        header += '%d\n' % len(titles)
        datanames = '\n'.join(titles)
        header += datanames

        arrs = np.array(arrs).T
        np.savetxt(filename, arrs, comments='', header=header, fmt=self.get_format())

        return 1


    def set_header(self, header):
        """Set the file header string"""
        if self._header != header:
            self._header = header
            self.Modified()
