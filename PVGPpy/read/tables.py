__all__ = [
    'gslib',
    'packedBinaries',
    'madagascar',
    'delimitedText']

import numpy as np
import csv
import os
from vtk.util import numpy_support as nps
import vtk
import ast
import warnings
# Import Helpers:
from ._helpers import *


def gslib(FileName, deli=' ', useTab=False, numIgLns=0, pdo=None):
    """
    @desc:
    Reads a GSLIB file format to a vtkTable. The GSLIB file format has headers lines followed by the data as a space delimited ASCI file (this filter is set up to allow you to choose any single character delimiter). The first header line is the title and will be printed to the console. This line may have the dimensions for a grid to be made of the data. The second line is the number (n) of columns of data. The next n lines are the variable names for the data in each column. You are allowed up to ten characters for the variable name. The data follow with a space between each field (column).

    @params:
    FileName : str : req : The absolute file name with path to read.
    deli : str : opt :The input files delimiter. To use a tab delimiter please set the `useTab`.
    useTab : boolean : opt : A boolean that describes whether to use a tab delimiter.
    numIgLns : int : opt : The integer number of lines to ignore.
    pdo : vtk.vtkTable : opt : A pointer to the output data object.

    @return:
    vtkTable : Returns a vtkTable of the input data file.

    """
    if pdo is None:
        pdo = vtk.vtkTable() # vtkTable

    if (useTab):
        deli = '\t'

    titles = []
    data = []
    with open(FileName) as f:
        reader = csv.reader(f, delimiter=deli)
        # Skip defined lines
        for i in range(numIgLns):
            next(f)

        # Get file header (part of format)
        header = next(f) # TODO: do something with the header
        #print(os.path.basename(FileName) + ': ' + header)
        # Get titles
        numCols = int(next(f))
        for i in range(numCols):
            titles.append(next(f).rstrip('\r\n'))

        # Read data
        for row in reader:
            data.append(row)

    _rows2table(data, titles, pdo)

    return pdo, header



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


def delimitedText(FileName, deli=' ', useTab=False, hasTits=True, numIgLns=0, pdo=None):
    """
    @desc:
    This reader will take in any delimited text file and make a vtkTable from it. This is not much different than the default .txt or .csv reader in ParaView, however it gives us room to use our own extensions and a little more flexibility in the structure of the files we import.


    @params:
    FileName : str: req : The absolute file name with path to read.
    deli : str : opt : The input files delimiter. To use a tab delimiter please set the `useTab`.
    useTab : boolean : opt : A boolean that describes whether to use a tab delimiter
    hasTits : boolean : opt : A boolean for if the delimited file has header titles for the data arrays.
    numIgLns : int : opt : The integer number of lines to ignore
    pdo : vtk.vtkTable : opt : A pointer to the output data object.

    @return:
    vtkTable : Returns a vtkTable of the input data file.

    """
    if pdo is None:
        pdo = vtk.vtkTable() # vtkTable

    if (useTab):
        deli = '\t'

    titles = []
    data = []
    with open(FileName) as f:
        reader = csv.reader(f, delimiter=deli)
        # Skip header lines
        for i in range(numIgLns):
            reader.next()
        # Get titles
        if (hasTits):
            titles = reader.next()
        else:
            # Bulild arbitrary titles for length of first row
            row = reader.next()
            data.append(row)
            for i in range(len(row)):
                titles.append('Field %d' % i)
        # Read data
        for row in reader:
            # Parse values here
            data.append(row)

    _rows2table(data, titles, pdo)

    return pdo
