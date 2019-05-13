__all__ = [
    'PackedBinariesReader',
    'MadagascarReader',
]

__displayname__ = 'Binary/Serialized File I/O'

import numpy as np
import vtk
import warnings

from .. import _helpers
from ..base import ReaderBase
from .. import interface



class PackedBinariesReader(ReaderBase):
    """This reads in float or double data that is packed into a binary file
    format. It will treat the data as one long array and make a ``vtkTable``
    with one column of that data. The reader uses defaults to import as floats
    with native endianness. Use the Table to Uniform Grid or the Reshape Table
    filters to give more meaning to the data. We chose to use a ``vtkTable``
    object as the output of this reader because it gives us more flexibility in
    the filters we can apply to this data down the pipeline and keeps thing
    simple when using filters in this repository.
    """
    __displayname__ = 'Packed Binaries Reader'
    __category__ = 'reader'
    extensions = 'H@ bin rsf rsf@ HH npz'
    description = 'PVGeo: Packed Binaries Reader'
    def __init__(self, **kwargs):
        ReaderBase.__init__(self,
            nOutputPorts=1, outputType='vtkTable', **kwargs)
        # Other Parameters
        self.__data_name = kwargs.get('dataname', 'Data')
        self.__dtypechar = kwargs.get('dtype', 'f')
        self.__endian = kwargs.get('endian', '')
        self.__dtype, self.__vtktype = interface.get_dtypes(dtype=self.__dtypechar, endian=self.__endian)
        # Data objects to hold the read data for access by the pipeline methods
        self.__data = []

    def _read_raw_file(self, filename):
        """Interanl helper to read the raw data from the file"""
        dtype = self.__dtype
        if dtype == np.dtype('>f'):
            # Checks if big-endian and fixes read
            dtype = np.dtype('f')
        try:
            arr = np.fromfile(filename, dtype=dtype)
        except (IOError, OSError) as fe:
            raise _helpers.PVGeoError(str(fe))
        return np.asarray(arr, dtype=self.__dtype)

    def _get_file_contents(self, idx=None):
        """Interanl helper to get all contents for all files"""
        if idx is not None:
            filenames = [self.get_file_names(idx=idx)]
        else:
            filenames = self.get_file_names()
        contents = []
        for f in filenames:
            contents.append(self._read_raw_file(f))
        if idx is not None: return contents[0]
        return contents


    def _read_up_front(self):
        """Should not need to be overridden
        """
        # Perform Read
        self.__data = self._get_file_contents()
        self.need_to_read(flag=False)
        return 1

    def _get_raw_data(self, idx=0):
        """This will return the proper data for the given timestep
        """
        return self.__data[idx]

    def convert_array(self, arr):
        """Converts the numpy array to a vtkDataArray
        """
        # Put raw data into vtk array
        data = interface.convert_array(arr, name=self.__data_name, deep=True, array_type=self.__vtktype)
        return data


    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to request data for current timestep
        """
        # Get output:
        output = vtk.vtkTable.GetData(outInfo)
        if self.need_to_read():
            self._read_up_front()
        # Get requested time index
        i = _helpers.get_requested_time(self, outInfo)
        # Generate the data object
        arr = self._get_raw_data(idx=i)
        data = self.convert_array(arr)
        output.AddColumn(data)
        return 1


    #### Seters and Geters ####


    def set_endian(self, endian):
        """Set the endianness of the data file.

        Args:
            endian (int or char): no preference = '' or 0, Little = 1 or `<` or Big = 2 `>`.
        """
        pos = ['', '<', '>']
        if isinstance(endian, int):
            endian = pos[endian]
        if endian != self.__endian:
            self.__endian = endian
            self.__dtype, self.__vtktype = interface.get_dtypes(dtype=self.__dtypechar, endian=self.__endian)
            self.Modified()

    def get_endian(self):
        """Get the endianness of the data file."""
        return self.__endian

    def set_data_type(self, dtype):
        """Set the data type of the binary file: `double='d'`, `float='f'`, `int='i'`
        """
        pos = ['d', 'f', 'i']
        if isinstance(dtype, int):
            dtype = pos[dtype]
        if dtype != self.__dtype:
            self.__dtypechar = dtype
            self.__dtype, self.__vtktype = interface.get_dtypes(dtype=self.__dtypechar, endian=self.__endian)
            self.Modified()

    def get_data_types(self):
        """Get the data type of the binary file"""
        return self.__dtype, self.__vtktype

    def set_data_name(self, data_name):
        """The string name of the data array generated from the inut file.
        """
        if data_name != self.__data_name:
            self.__data_name = data_name
            self.Modified(read_again=False) # Don't re-read. Just request data again


    def get_data_name(self):
        """Get name used for the data array"""
        return self.__data_name



class MadagascarReader(PackedBinariesReader):
    """This reads in float or double data that is packed into a Madagascar
    binary file format with a leader header. The reader ignores all of the ascii
    header details by searching for the sequence of three special characters:
    EOL EOL EOT and it will treat the followng binary packed data as one long
    array and make a ``vtkTable`` with one column of that data. The reader uses
    defaults to import as floats with native endianness. Use the Table to
    Uniform Grid or the Reshape Table filters to give more meaning to the data.
    We will later implement the ability to create a gridded volume from the
    header info. This reader is a quick fix for Samir. We chose to use a
    ``vtkTable`` object as the output of this reader because it gives us more
    flexibility in the filters we can apply to this data down the pipeline and
    keeps thing simple when using filters in this repository.
    `Details Here`_.

    .. _Details Here: http://www.ahay.org/wiki/RSF_Comprehensive_Description#Single-stream_RSF
    """
    __displayname__ = 'Madagascar SSRSF Reader'
    __category__ = 'reader'
    # extensions are inherrited from PackedBinariesReader
    description = 'PVGeo: Madagascar Single Stream RSF Files'
    def __init__(self, **kwargs):
        PackedBinariesReader.__init__(self, **kwargs)

    def _read_raw_file(self, filename):
        """Reads the raw data from the file for Madagascar SSRSF files"""
        dtype, vtktype = self.get_data_types()
        CTLSEQ = b'\014\014\004' # The control sequence to seperate header from data
        rpl = b''
        raw = []
        with open(filename, 'rb') as file:
            raw = file.read()
            idx = raw.find(CTLSEQ)
            if idx == -1:
                warnings.warn('This is not a single stream RSF format file. Treating entire file as packed binary data.')
            else:
                raw = raw[idx:] # deletes the header
                raw = raw.replace(CTLSEQ, rpl) # removes the control sequence
        arr = np.fromstring(raw, dtype=dtype)
        return arr
