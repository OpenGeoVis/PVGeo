__all__ = [
    'DelimitedTextReader',
    'XYZTextReader'
]

import numpy as np
from vtk.util import numpy_support as nps
import vtk

# Import Helpers:
from ..base import PVGeoReaderBase
from .. import _helpers


class DelimitedTextReader(PVGeoReaderBase):
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
        PVGeoReaderBase.__init__(self,
            nOutputPorts=nOutputPorts, outputType=outputType)

        # Parameters to control the file read:
        #- if these are set/changed, we must reperform the read
        self.__delimiter = " "
        self.__useTab = False
        self.__skipRows = 0
        self.__comments = "#"
        self.__hasTitles = True
        # Data objects to hold the read data for access by the pipeline methods
        self.__data = []
        self.__titles = []

    def _GetDeli(self):
        """For itenral use"""
        if self.__useTab:
            return '\t'
        return self.__delimiter

    #### Methods for performing the read ####

    def _GetFileContents(self, idx=None):
        if idx is not None:
            fileNames = [self.GetFileNames(idx=idx)]
        else:
            fileNames = self.GetFileNames()
        contents = []
        for f in fileNames:
            contents.append(np.genfromtxt(f, dtype=str, delimiter='\n', comments=self.__comments)[self.__skipRows::])
        if idx is not None: return contents[0]
        return contents

    def _ExtractHeader(self, content):
        """Override this. Remove header from single file's content"""
        if len(np.shape(content)) > 2:
            raise RuntimeError("`_ExtractHeader()` can only handle a sigle file's content")
        idx = 0
        if self.__hasTitles:
            titles = content[idx].split(self._GetDeli())
            idx += 1
        else:
            cols = len(content[idx].split(self._GetDeli()))
            titles = []
            for i in range(cols):
                titles.append('Field %d' % i)
        return titles, content[idx::]

    def __ExtractHeaders(self, contents):
        """Should NOT be overriden"""
        ts = []
        for i in range(len(contents)):
            titles, newcontent = self._ExtractHeader(contents[i])
            contents[i] = newcontent
            ts.append(titles)
        # Check that the titles are the same across files:
        ts = np.unique(np.asarray(ts), axis=0)
        if len(ts) > 1:
            raise RuntimeError('Data array titles varied across file timesteps. This data is invalid as a timeseries.')
        return ts[0], contents


    def __FileContentsToDataArray(self, contents):
        """Should not need to be overriden"""
        data = []
        for content in contents:
            data.append(np.genfromtxt((line.encode('utf8') for line in content), delimiter=self._GetDeli(), dtype=None))
        return data

    def _ReadUpFront(self):
        """Should not need to be overridden"""
        # Perform Read
        contents = self._GetFileContents()
        self.__titles, contents = self.__ExtractHeaders(contents)
        self.__data = self.__FileContentsToDataArray(contents)
        self.NeedToRead(flag=False)
        return 1

    #### Methods for accessing the data read in #####

    def _GetRawData(self, idx=0):
        """This will return the proper data for the given timestep"""
        return self.__data[idx]


    #### Algorithm Methods ####

    def RequestData(self, request, inInfo, outInfo):
        # Get output:
        output = self.GetOutputData(outInfo, 0)
        # Get requested time index
        i = _helpers.GetRequestedTime(self, outInfo)
        if self.NeedToRead():
            self._ReadUpFront()
        # Generate the data object
        _helpers._placeArrInTable(self._GetRawData(idx=i), self.__titles, output)
        return 1


    #### Seters and Geters ####


    def SetDelimiter(self, deli):
        """The input file's delimiter. To use a tab delimiter please use `SetUseTab()`"""
        if deli != self.__delimiter:
            self.__delimiter = deli
            self.Modified()

    def SetUseTab(self, flag):
        """A boolean to override the SetDelimiter() and use a Tab delimiter."""
        if flag != self.__useTab:
            self.__useTab = flag
            self.Modified()

    def SetSkipRows(self, skip):
        """The integer number of rows to skip at the top of the file"""
        if skip != self.__skipRows:
            self.__skipRows = skip
            self.Modified()

    def GetSkipRows(self):
        return self.__skipRows

    def SetComments(self, identifier):
        """The character identifier for comments within the file."""
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

    def GetTitles(self):
        return self.__titles




class XYZTextReader(DelimitedTextReader):
    """A makeshift reader for XYZ files where titles have comma delimiter and data has space delimiter"""
    def __init__(self):
        DelimitedTextReader.__init__(self)

    # Simply override the extract titles functionality
    def _ExtractHeader(self, fileLines):
        titles = fileLines[0][2::].split(', ') # first two characers of header is '! '
        return titles, fileLines[1::]
