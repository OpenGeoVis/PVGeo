import numpy as np
import struct
import csv
import os
from vtk.util import numpy_support as nps
import vtk
import ast

def _parseString(val):
    try:
        val = ast.literal_eval(val)
    except ValueError:
        pass
    return val

def _getVTKtype(typ):
    lookup = dict(
        char=vtk.VTK_CHAR,
        int=vtk.VTK_INT,
        uns_int=vtk.VTK_UNSIGNED_INT,
        long=vtk.VTK_LONG,
        uns_long=vtk.VTK_UNSIGNED_LONG,
        single=vtk.VTK_FLOAT,
        double=vtk.VTK_DOUBLE,
    )
    if typ is str or typ is np.string_:
        return lookup['char']
    if typ is np.float64:
        return lookup['double']
    if typ is float or typ is np.float or typ is np.float32:
        return lookup['single']
    if typ is int or np.int_:
        return lookup['int']
    raise Exception('Data type %s unknown to _getVTKtype() method.' % typ)

def _placeArrInTable(dlist, titles, pdo):
    # Put columns into table
    for i in range(len(dlist)):
        typ = _getVTKtype(type(dlist[i][0]))
        VTK_data = nps.numpy_to_vtk(num_array=dlist[i], deep=True, array_type=typ)
        VTK_data.SetName(titles[i])
        pdo.AddColumn(VTK_data)
    return None


def _rows2table(rows, titles, pdo):
    # now rotate data and extract numpy arrays of same array_type
    data = np.asarray(rows).T
    typs = []
    dlist = []
    for i in range(len(titles)):
        # get data types
        typs.append(type(_parseString(data[i][0])))
        dlist.append(np.asarray(data[i], dtype=typs[i]))
    # Put columns into table
    _placeArrInTable(dlist, titles, pdo)
    return None

#-----------------
# End of Helpers
#-----------------

def gslib(FileName, deli=' ', useTab=False, numIgLns=0, pdo=None):
    """
    Description
    -----------
    Reads a GSLIB file format to a vtkTable. The GSLIB file format has headers lines followed by the data as a space delimited ASCI file (this filter is set up to allow you to choose any single character delimiter). The first header line is the title and will be printed to the console. This line may have the dimensions for a grid to be made of the data. The second line is the number (n) of columns of data. The next n lines are the variable names for the data in each column. You are allowed up to ten characters for the variable name. The data follow with a space between each field (column).

    Parameters
    ----------
    `FileName` : str

    - The absolute file name with path to read.

    `deli` : str

    - The input files delimiter. To use a tab delimiter please set the `useTab`.

    `useTab` : boolean

    - A boolean that describes whether to use a tab delimiter

    `numIgLns` : int

    - The integer number of lines to ignore

    Returns
    -------
    Returns a vtkTable of the input data file.

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



def packedBinaries(FileName, dataNm=None, pdo=None, endian='>', dtype='f'):
    """
    Description
    -----------
    This filter reads in float or double data that is packed into a binary file format. It will treat the data as one long array and make a vtkTable with one column of that data. The reader uses big endian and defaults to import as floats. Use the Table to Uniform Grid or the Reshape Table filters to give more meaning to the data. We chose to use a vtkTable object as the output of this reader because it gives us more flexibility in the filters we can apply to this data down the pipeline and keeps thing simple when using filters in this repository.

    Parameters
    ----------
    `FileName` : str

    - The absolute file name with path to read.

    `dblVals` : boolean, optional

    - A boolean flag to chose to treat the binary packed data as doubles instead of the default floats.

    `dataNm` : str, optional

    - A string name to use for the constructed vtkDataArray

    Returns
    -------
    Returns a vtkTable of the input data file with a single column being the data read.

    """
    if pdo is None:
        pdo = vtk.vtkTable() # vtkTable


    if dtype is 'd':
        num_bytes = 8 # DOUBLE
        vtktype = vtk.VTK_DOUBLE
    elif dtype is 'f':
        num_bytes = 4 # FLOAT
        vtktype = vtk.VTK_FLOAT
    elif dtype is 'i':
        num_bytes = 4 # INTEGER
        vtktype = vtk.VTK_INT
    else:
        raise Exception('dtype \'%s\' unknown/.' % dtype)

    tn = os.stat(FileName).st_size / num_bytes
    tn_string = str(tn)
    raw = []
    with open(FileName, 'rb') as file:
        # Unpack by num_bytes
        raw = struct.unpack(endian+tn_string+dtype, file.read(num_bytes*tn))

    # Put raw data into vtk array
    # TODO: dynamic typing
    data = nps.numpy_to_vtk(num_array=raw, deep=True, array_type=vtktype)

    if dataNm is None or dataNm == '':
        dataNm = os.path.splitext(os.path.basename(FileName))[0]
    data.SetName(dataNm)

    # Table with single column of data only
    pdo.AddColumn(data)

    return pdo


def delimitedText(FileName, deli=' ', useTab=False, hasTits=True, numIgLns=0, pdo=None):
    """
    Description
    -----------
    This reader will take in any delimited text file and make a vtkTable from it. This is not much different than the default .txt or .csv reader in ParaView, however it gives us room to use our own extensions and a little more flexibility in the structure of the files we import.


    Parameters
    ----------
    `FileName` : str

    - The absolute file name with path to read.

    `deli` : str

    - The input files delimiter. To use a tab delimiter please set the `useTab`.

    `useTab` : boolean

    - A boolean that describes whether to use a tab delimiter

    `numIgLns` : int

    - The integer number of lines to ignore

    Returns
    -------
    Returns a vtkTable of the input data file.

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
