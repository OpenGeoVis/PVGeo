__all__ = [
    'delimitedText']

import numpy as np
from vtk.util import numpy_support as nps
import vtk
# Import Helpers:
from .. import _helpers



def delimitedText(FileName, deli=' ', useTab=False, hasTits=True, skiprows=0, comments='#', pdo=None):
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
    if pdo is None:
        pdo = vtk.vtkTable() # vtkTable

    if (useTab):
        deli = '\t'

    fileLines = np.genfromtxt(FileName, dtype=str, delimiter='\n', comments=comments)

    idx = 0
    if hasTits:
        titles = fileLines[idx+skiprows].split(deli)
        idx += 1
    else:
        titles = []

    data = np.genfromtxt((line.encode('utf8') for line in fileLines[idx+skiprows::]), dtype=None)

    if not hasTits:
        cols = np.shape(data)[1]
        for i in range(cols):titles.append('Field %d' % i)

    _helpers._placeArrInTable(data, titles, pdo)

    return pdo
