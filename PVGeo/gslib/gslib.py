__all__ = [
    'gslibRead',
]

import numpy as np
from vtk.util import numpy_support as nps
import vtk
# Import Helpers:
from .. import _helpers


def gslibRead(FileName, deli=' ', useTab=False, skiprows=0, comments='#', pdo=None):
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
    retAll = False
    if pdo is None:
        pdo = vtk.vtkTable() # vtkTable
        retAll = True

    if (useTab):
        deli = '\t'

    fileLines = np.genfromtxt(FileName, dtype=str, delimiter='\n', comments=comments,)

    header = fileLines[0+skiprows]

    try:
        num = int(fileLines[1+skiprows]) # number of data columns
    except ValueError:
        raise Exception('This file is not in proper GSLIB format.')

    titles = []
    for i in range(2+skiprows,2+num+skiprows):
        titles.append(fileLines[i].rstrip('\r\n'))

    data = np.genfromtxt((line.encode('utf8') for line in fileLines[2+num+skiprows::]), dtype=None)

    _helpers._placeArrInTable(data, titles, pdo)

    if retAll:
        return pdo, header
    return header
