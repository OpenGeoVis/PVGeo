__all__ = [
    'GSLibReader',
]

import numpy as np
# Import Helpers:
from .. import _helpers
from ..readers import DelimitedTextReader

class GSLibReader(DelimitedTextReader):
    """Reads a GSLIB file format to a ``vtkTable``. The GSLIB file format has headers lines followed by the data as a space delimited ASCI file (this filter is set up to allow you to choose any single character delimiter). The first header line is the title and will be printed to the console. This line may have the dimensions for a grid to be made of the data. The second line is the number (n) of columns of data. The next n lines are the variable names for the data in each column. You are allowed up to ten characters for the variable name. The data follow with a space between each field (column).
    """
    __displayname__ = 'GSLib Table Reader'
    __category__ = 'reader'
    def __init__(self, outputType='vtkTable', **kwargs):
        DelimitedTextReader.__init__(self, outputType=outputType, **kwargs)
        self.SetDelimiter(kwargs.get('delimiter', ' '))
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
