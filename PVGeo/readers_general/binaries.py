__all__ = [
    'PackedBinariesReader',
    'MadagascarReader']

import numpy as np
from vtk.util import numpy_support as nps
import vtk
import warnings
# Import Helpers:
from .. import _helpers
from ..base import PVGeoReaderBase



class PackedBinariesReader(PVGeoReaderBase):
    """@desc: This reads in float or double data that is packed into a binary file format. It will treat the data as one long array and make a `vtkTable` with one column of that data. The reader uses defaults to import as floats with native endianness. Use the Table to Uniform Grid or the Reshape Table filters to give more meaning to the data. We chose to use a `vtkTable` object as the output of this reader because it gives us more flexibility in the filters we can apply to this data down the pipeline and keeps thing simple when using filters in this repository.
    """
    def __init__(self):
        PVGeoReaderBase.__init__(self,
            nOutputPorts=1, outputType='vtkTable')
        # Other Parameters
        self.__dataName = "Data"
        self.__dtypechar = 'f'
        self.__endian = ''
        self.__dtype, self.__vtktype = _helpers.getdTypes(dtype=self.__dtypechar, endian=self.__endian)
        self.__madagascar = False
        # Data objects to hold the read data for access by the pipeline methods
        self.__data = []

    def _ReadRawFile(self, fileName):
        dtype = self.__dtype
        if dtype == np.dtype('>f'):
            # Checks if big-endian and fixes read
            dtype = np.dtype('f')
        arr = np.fromfile(fileName, dtype=dtype)
        return np.asarray(arr, dtype=self.__dtype)

    def _GetFileContents(self, idx=None):
        if idx is not None:
            fileNames = [self.GetFileNames(idx=idx)]
        else:
            fileNames = self.GetFileNames()
        contents = []
        for f in fileNames:
            contents.append(self._ReadRawFile(f))
        if idx is not None: return contents[0]
        return contents


    def _ReadUpFront(self):
        """Should not need to be overridden"""
        # Perform Read
        self.__data = self._GetFileContents()
        self.NeedToRead(flag=False)
        return 1

    def _GetRawData(self, idx=0):
        """@desc: This will return the proper data for the given timestep"""
        return self.__data[idx]

    def ConvertArray(self, arr):
        # Put raw data into vtk array
        data = nps.numpy_to_vtk(num_array=arr, deep=True, array_type=self.__vtktype)
        data.SetName(self.__dataName)
        return data


    def RequestData(self, request, inInfo, outInfo):
        # Get output:
        output = vtk.vtkTable.GetData(outInfo)
        if self.NeedToRead():
            self._ReadUpFront()
        # Get requested time index
        i = _helpers.GetRequestedTime(self, outInfo)
        # Generate the data object
        arr = self._GetRawData(idx=i)
        data = self.ConvertArray(arr)
        output.AddColumn(data)
        return 1


    #### Seters and Geters ####


    def SetEndian(self, endian):
        """@desc: The endianness of the data file. `Little = '<'` or `Big = '>'`"""
        pos = ['', '<', '>']
        if isinstance(endian, int):
            endian = pos[endian]
        if endian != self.__endian:
            self.__endian = endian
            self.__dtype, self.__vtktype = _helpers.getdTypes(dtype=self.__dtypechar, endian=self.__endian)
            self.Modified()

    def GetEndian(self):
        return self.__endian

    def SetDataType(self, dtype):
        """@desc: The data type of the binary file: `double='d'`, `float='f'`, `int='i'`"""
        pos = ['d', 'f', 'i']
        if isinstance(dtype, int):
            dtype = pos[dtype]
        if dtype != self.__dtype:
            self.__dtypechar = dtype
            self.__dtype, self.__vtktype = _helpers.getdTypes(dtype=self.__dtypechar, endian=self.__endian)
            self.Modified()

    def GetDataTypes(self):
        return self.__dtype, self.__vtktype

    def SetDataName(self, dataName):
        """@desc: The string name of the data array generated from the inut file."""
        if dataName != self.__dataName:
            self.__dataName = dataName
            self.Modified(readAgain=False) # Don't re-read. Just request data again


    def GetDataName(self):
        return self.__dataName



class MadagascarReader(PackedBinariesReader):
    """@desc: This reads in float or double data that is packed into a Madagascar binary file format with a leader header. The reader ignores all of the ascii header details by searching for the sequence of three special characters: EOL EOL EOT (\014\014\004) and it will treat the followng binary packed data as one long array and make a `vtkTable` with one column of that data. The reader uses defaults to import as floats with native endianness. Use the Table to Uniform Grid or the Reshape Table filters to give more meaning to the data. We will later implement the ability to create a gridded volume from the header info. This reader is a quick fix for Samir. We chose to use a `vtkTable` object as the output of this reader because it gives us more flexibility in the filters we can apply to this data down the pipeline and keeps thing simple when using filters in this repository.
    [Details Here](http://www.ahay.org/wiki/RSF_Comprehensive_Description#Single-stream_RSF)
    """
    def __init__(self):
        PackedBinariesReader.__init__(self)

    def _ReadRawFile(self, fileName):
        dtype, vtktype = self.GetDataTypes()
        CTLSEQ = b'\014\014\004' # The control sequence to seperate header from data
        rpl = b''
        raw = []
        with open(fileName, 'rb') as file:
            raw = file.read()
            idx = raw.find(CTLSEQ)
            if idx == -1:
                warnings.warn('This is not a single stream RSF format file. Treating entire file as packed binary data.')
            else:
                raw = raw[idx:] # deletes the header
                raw = raw.replace(CTLSEQ, rpl) # removes the control sequence
        arr = np.fromstring(raw, dtype=dtype)
        return arr
