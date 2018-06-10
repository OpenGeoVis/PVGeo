__all__ = [
    'packedBinaries',
    'madagascar']

import numpy as np
import csv
import os
from vtk.util import numpy_support as nps
import vtk
import ast
import warnings
# Import Helpers:
from ._helpers import *


def packedBinaries(FileName, dataNm=None, endian=None, dtype='f', pdo=None):
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
    if pdo is None:
        pdo = vtk.vtkTable() # vtkTable

    dtype, vtktype = _getdTypes(dtype=dtype, endian=endian)

    raw = np.fromfile(FileName, dtype=dtype)

    # Put raw data into vtk array
    data = nps.numpy_to_vtk(num_array=raw, deep=True, array_type=vtktype)
    data.SetName(_cleanDataNm(dataNm, FileName))

    # Table with single column of data only
    pdo.AddColumn(data)

    return pdo

def madagascar(FileName, dataNm=None, endian=None, dtype='f', pdo=None):
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
    if pdo is None:
        pdo = vtk.vtkTable() # vtkTable

    dtype, vtktype = _getdTypes(dtype=dtype, endian=endian)

    CTLSEQ = b'\014\014\004' # The control sequence to seperate header from data
    rpl = b''
    raw = []
    with open(FileName, 'r') as file:
        raw = file.read()
        idx = raw.find(CTLSEQ)
        if idx == -1:
            warnings.warn('This is not a single stream RSF format file. Treating entire file as packed binary data.')
        else:
            raw = raw[idx:] # deletes the header
            raw = raw.replace(CTLSEQ, rpl) # removes the control sequence
        raw = np.fromstring(raw, dtype=dtype)

    # Put raw data into vtk array
    data = nps.numpy_to_vtk(num_array=raw, deep=True, array_type=vtktype)
    data.SetName(_cleanDataNm(dataNm, FileName))

    # Table with single column of data only
    pdo.AddColumn(data)

    return pdo
