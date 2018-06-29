__all__ = [
    'DelimitedTextReader',
    'XYZTextReader'
]

import numpy as np
from vtk.util import numpy_support as nps
import vtk

# Import Helpers:
from PVGeo import ReaderBase
from .. import _helpers


class DelimitedTextReader(ReaderBase):
    """
    @desc:
    This reader will take in any delimited text file and make a vtkTable from it. This is not much different than the default .txt or .csv reader in ParaView, however it gives us room to use our own extensions and a little more flexibility in the structure of the files we import.


    @params:
    FileName : str: req : The absolute file name with path to read.
    deli : str : opt : The input files delimiter. To use a tab delimiter please set the `useTab`.
    useTab : boolean : opt : A boolean that describes whether to use a tab delimiter
    hasTits : boolean : opt : A boolean for if the delimited file has header titles for the data arrays.
    skiprows : int : opt : The integer number of rows to skip at the top of the file
    comments : char : opt : The identifier for comments within the file.
    pdo : vtk.vtkTable : opt : A pointer to the output data object.

    @return:
    vtkTable : Returns a vtkTable of the input data file.

    """
    def __init__(self, nOutputPorts=1, outputType='vtkTable'):
        ReaderBase.__init__(self,
            nOutputPorts=nOutputPorts, outputType=outputType)

        # Other Parameters:
        self.__delimiter = " "
        self.__useTab = False
        self.__skipRows = 0
        self.__comments = "#"
        self.__hasTitles = True


    def _GetDeli(self):
        """For itenral use"""
        if self.__useTab:
            return '\t'
        return self.__delimiter

    def _GetFileLines(self, idx=0):
        return np.genfromtxt(self.GetFileNames(idx=idx), dtype=str, delimiter='\n', comments=self.__comments)[self.__skipRows::]

    def _ExtractHeader(self, fileLines):
        idx = 0
        if self.__hasTitles:
            titles = fileLines[idx].split(self._GetDeli())
            idx += 1
        else:
            cols = len(fileLines[idx].split(self._GetDeli()))
            titles = []
            for i in range(cols):
                titles.append('Field %d' % i)
        return titles, fileLines[idx::]


    def _GetNumPyData(self, fileLines):
        return np.genfromtxt((line.encode('utf8') for line in fileLines), delimiter=self._GetDeli(), dtype=None)



    def RequestData(self, request, inInfo, outInfo):
        # Get output:
        output = vtk.vtkTable.GetData(outInfo)
        # Get requested time index
        i = self._GetRequestedTime(outInfo)
        # Perform Read
        fileLines = self._GetFileLines(idx=i)
        titles, fileLines = self._ExtractHeader(fileLines)
        data = self._GetNumPyData(fileLines)
        # Generate the data object
        _helpers._placeArrInTable(data, titles, output)
        return 1


    #### Seters and Geters ####
    def SetDelimiter(self, deli):
        if deli != self.__delimiter:
            self.__delimiter = deli
            self.Modified()

    def SetUseTab(self, flag):
        if flag != self.__useTab:
            self.__useTab = flag
            self.Modified()

    def SetSkipRows(self, skip):
        if skip != self.__skipRows:
            self.__skipRows = skip
            self.Modified()

    def GetSkipRows(self):
        return self.__skipRows

    def SetComments(self, identifier):
        if identifier != self.__comments:
            self.__comments = identifier
            self.Modified()

    def SetHasTitles(self, flag):
        """A boolean for if the delimited file has header titles for the data arrays."""
        if self.__hasTitles != flag:
            self.__hasTitles = flag
            self.Modified()

    def GetHasTitles(self):
        return self.__hasTitles




class XYZTextReader(DelimitedTextReader):
    def __init__(self):
        DelimitedTextReader.__init__(self)

    # Simply override the extract titles functionality
    def _ExtractHeader(self, fileLines):
        titles = fileLines[0][2::].split(', ') # first two characers of header is '! '
        return titles, fileLines[1::]
