__all__ = [
    'PackedBinariesReader',
    'MadagascarReader']

import numpy as np
from vtk.util import numpy_support as nps
import vtk
import warnings
# Import Helpers:
from .. import _helpers
from ..base import ReaderBase



class PackedBinariesReader(ReaderBase):
    """
    @desc:
    This reads in float or double data that is packed into a binary file format. It will treat the data as one long array and make a vtkTable with one column of that data. The reader uses defaults to import as floats with native endianness. Use the Table to Uniform Grid or the Reshape Table filters to give more meaning to the data. We chose to use a vtkTable object as the output of this reader because it gives us more flexibility in the filters we can apply to this data down the pipeline and keeps thing simple when using filters in this repository.

    @params:
    FileName : str : req : The absolute file name with path to read.
    dataNm : str : opt : A string name to use for the constructed vtkDataArray.
    endian : char : opt : The endianness to unpack the values. Defaults to Native.
    dtype : char : opt : A char to chose the data type when unpacking. `d` for float64 (double), `f` for float32 (float), or `i` for int
    pdo : vtk.vtkTable : opt : A pointer to the output data object.

    @return:
    vtkTable : Returns a vtkTable of the input data file with a single column being the data read.
    """
    def __init__(self):
        ReaderBase.__init__(self,
            nOutputPorts=1, outputType='vtkTable')
        # Other Parameters
        self.__dataName = "Data"
        self.__endian = ''
        self.__dtype = 'f'
        self.__madagascar = False

    def _GetTypes(self):
        # Usage: dtype, vtktype = self._GetTypes()
        return _helpers._getdTypes(dtype=self.__dtype, endian=self.__endian)

    def _ReadRawFile(self, idx=0):
        dtype, vtktype = _helpers._getdTypes(dtype=self.__dtype, endian=self.__endian)
        arr = np.fromfile(self.GetFileNames(idx=idx), dtype=dtype)
        return arr


    def _ConvertArray(self, arr):
        # Put raw data into vtk array
        dtype, vtktype = _helpers._getdTypes(dtype=self.__dtype, endian=self.__endian)
        data = nps.numpy_to_vtk(num_array=arr, deep=True, array_type=vtktype)
        data.SetName(self.__dataName)
        return data


    def RequestData(self, request, inInfo, outInfo):
        # Get output:
        output = vtk.vtkTable.GetData(outInfo)
        # Get requested time index
        i = _helpers.GetRequestedTime(self, outInfo)
        arr = self._ReadRawFile(idx=i)
        data = self._ConvertArray(arr)
        output.AddColumn(data)
        return 1


    #### Seters and Geters ####
    def SetEndian(self, endian):
        """The endianness of the data file. Little='<' or Big='>'"""
        pos = ['', '<', '>']
        if isinstance(endian, int):
            endian = pos[endian]
        if endian != self.__endian:
            self.__endian = endian
            self.Modified()

    def GetEndian(self):
        return self.__endian

    def SetDType(self, dtype):
        """The data type of the binary file: double='d', float='f', int='i'"""
        pos = ['d', 'f', 'i']
        if isinstance(dtype, int):
            dtype = pos[dtype]
        if dtype != self.__dtype:
            self.__dtype = dtype
            self.Modified()

    def GetDType(self):
        return self.__dtype

    def SetDataName(self, dataName):
        """The string name of the data array generated from the inut file."""
        if dataName != self.__dataName:
            self.__dataName = dataName
            self.Modified()

    def GetDataName(self):
        return self.__dataName



class MadagascarReader(PackedBinariesReader):
    """
    @desc:
    This reads in float or double data that is packed into a Madagascar binary file format with a leader header. The reader ignores all of the ascii header details by searching for the sequence of three special characters: EOL EOL EOT (\014\014\004) and it will treat the followng binary packed data as one long array and make a vtkTable with one column of that data. The reader uses defaults to import as floats with native endianness. Use the Table to Uniform Grid or the Reshape Table filters to give more meaning to the data. We will later implement the ability to create a gridded volume from the header info. This reader is a quick fix for Samir. We chose to use a vtkTable object as the output of this reader because it gives us more flexibility in the filters we can apply to this data down the pipeline and keeps thing simple when using filters in this repository.
    [Details Here](http://www.ahay.org/wiki/RSF_Comprehensive_Description#Single-stream_RSF)

    @params:
    FileName : str : req : The absolute file name with path to read.
    dataNm : str : opt : A string name to use for the constructed vtkDataArray.
    endian : char : opt : The endianness to unpack the values. Defaults to Native.
    dtype : char : opt : A char to chose the data type when unpacking. `d` for float64 (double), `f` for float32 (float), or `i` for int
    pdo : vtk.vtkTable : opt : A pointer to the output data object.

    @return:
    vtkTable : Returns a vtkTable of the input data file with a single column being the data read.

    """
    def __init__(self):
        PackedBinariesReader.__init__(self)

    def _ReadRawFile(self, idx=0):
        dtype, vtktype = self._GetTypes()
        CTLSEQ = b'\014\014\004' # The control sequence to seperate header from data
        rpl = b''
        raw = []
        with open(self.GetFileNames(idx=idx), 'rb') as file:
            raw = file.read()
            idx = raw.find(CTLSEQ)
            if idx == -1:
                warnings.warn('This is not a single stream RSF format file. Treating entire file as packed binary data.')
            else:
                raw = raw[idx:] # deletes the header
                raw = raw.replace(CTLSEQ, rpl) # removes the control sequence
        arr = np.fromstring(raw, dtype=dtype)
        return arr
