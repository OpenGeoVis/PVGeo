__all__ = [
    'GSLibReader',
]

import numpy as np
from vtk.util import numpy_support as nps
import vtk
# Import Helpers:
from .. import _helpers
from ..readers_general import DelimitedTextReader

class GSLibReader(DelimitedTextReader):
    """
    @desc:
    Reads a GSLIB file format to a vtkTable. The GSLIB file format has headers lines followed by the data as a space delimited ASCI file (this filter is set up to allow you to choose any single character delimiter). The first header line is the title and will be printed to the console. This line may have the dimensions for a grid to be made of the data. The second line is the number (n) of columns of data. The next n lines are the variable names for the data in each column. You are allowed up to ten characters for the variable name. The data follow with a space between each field (column).

    @params:
    FileName : str : req : The absolute file name with path to read.
    deli : str : opt :The input files delimiter. To use a tab delimiter please set the `useTab`.
    useTab : boolean : opt : A boolean that describes whether to use a tab delimiter.
    skiprows : int : opt : The integer number of rows to skip at the top of the file.
    comments : char : opt : The identifier for comments within the file.
    pdo : vtk.vtkTable : opt : A pointer to the output data object.

    @return:
    vtkTable : Returns a vtkTable of the input data file.

    """
    def __init__(self, outputType='vtkTable'):
        DelimitedTextReader.__init__(self, outputType=outputType)
        self.SetDelimiter(" ")
        # These are attributes the derived from file contents:
        self.__header = None

    def _ExtractHeader(self, content):
        self.__header = content[0]
        try:
            num = int(content[1]) # number of data columns
        except ValueError:
            raise RuntimeError('This file is not in proper GSLIB format.')

        titles = []
        for i in range(2, 2 + num):
            titles.append(content[i].rstrip('\r\n'))
        return titles, content[2 + num::]


    #### Seters and Geters ####

    def GetFileHeader(self):
        if self.__header is None:
            raise RuntimeError("Input file has not been read yet.")
        return self.__header

    def _SetFileHeader(self, header):
        self.__header = header
        return 1
