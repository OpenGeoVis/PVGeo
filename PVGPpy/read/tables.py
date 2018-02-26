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


"""def _getVTKtype(typ):
    """

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

    # Put first column into table
    for i in range(numCols):
        col = []
        for row in data:
            col.append(row[i])
        VTK_data = nps.numpy_to_vtk(num_array=col, deep=True, array_type=vtk.VTK_FLOAT)
        VTK_data.SetName(titles[i])
        pdo.AddColumn(VTK_data)

    return pdo, header


def packedBinaries(FileName, dblVals=False, dataNm='values', pdo=None, endian='>'):
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

    num_bytes = 4 # FLOAT
    typ = 'f' #FLOAT
    if dblVals:
        num_bytes = 8 # DOUBLE
        typ = 'd' # DOUBLE

    tn = os.stat(FileName).st_size / num_bytes
    tn_string = str(tn)
    raw = []
    with open(FileName, 'rb') as file:
        # Unpack by num_bytes
        raw = struct.unpack(endian+tn_string+typ, file.read(num_bytes*tn))

    # Put raw data into vtk array
    # TODO: dynamic typing
    data = nps.numpy_to_vtk(num_array=raw, deep=True, array_type=vtk.VTK_FLOAT)
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
            rr = []
            for r in row:
                rr.append(_parseString(r))
            data.append(row)
    # now rotate data and extract numpy arrays of same array_type
    dlist = []
    for i in range(len(titles)):
        col = []
        for row in data:
            col.append(row[i])
        arr = np.asarray(col, dtype=type(col[0]))
        dlist.append(arr)


    # Put columns into table
    for i in range(len(dlist)):
        typ = _getVTKtype(type(dlist[i][0]))

        VTK_data = nps.numpy_to_vtk(num_array=dlist[i], deep=True, array_type=typ)

        VTK_data.SetName(titles[i])
        pdo.AddColumn(VTK_data)

    return pdo
