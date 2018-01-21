import numpy as np
import csv
import os
from vtk.util import numpy_support as nps
import vtk

def sgemsGrid(FileName, deli=' ', useTab=False, pdo=None):
    """
    Description
    -----------
    Generates vtkImageData from the uniform grid defined in the inout file in the SGeMS grid format. This format is simply the GSLIB format where the header line defines the dimensions of the uniform grid.

    Parameters
    ----------
    `FileName` : str

    - The file name / absolute path for the input file in SGeMS grid format.

    `deli` : str, optional

    - The input files delimiter. To use a tab delimiter please set the `useTab`.

    `useTab` : boolean, optional

    - A boolean that describes whether to use a tab delimiter.

    Returns
    -------
    Returns vtkImageData

    """
    if pdo is None:
        pdo = vtk.vtkImageData() # vtkImageData

    if (useTab):
        deli = '\t'

    titles = []
    data = []
    with open(FileName) as f:
        reader = csv.reader(f, delimiter=deli)

        h = reader.next()
        n1,n2,n3 = int(h[0]), int(h[1]), int(h[2])

        pdo.SetDimensions(n1, n2, n3)
        pdo.SetExtent(0,n1-1, 0,n2-1, 0,n3-1)


        # Get titles
        numCols = int(next(f))
        for i in range(numCols):
            titles.append(next(f).rstrip('\r\n'))

        # Read data
        for row in reader:
            data.append(row)
        f.close()

    # Put first column into data arrays
    for i in range(numCols):
        col = []
        for row in data:
            col.append(row[i])
        VTK_data = nps.numpy_to_vtk(num_array=col, deep=True, array_type=vtk.VTK_FLOAT)
        VTK_data.SetName(titles[i])
        pdo.GetPointData().AddArray(VTK_data)
        #TODO: pdo.GetCellData().AddArray(VTK_data)

    return pdo

def sgemsExtent(FileName, deli=' ', useTab=False):
    """
    Description
    -----------
    Reads the input file for the SGeMS format to get output extents. Computationally inexpensive method to discover whole output extent.

    Parameters
    ----------
    `FileName` : str

    - The file name / absolute path for the input file in SGeMS grid format.

    `deli` : str, optional

    - The input files delimiter. To use a tab delimiter please set the `useTab`.

    `useTab` : boolean, optional

    - A boolean that describes whether to use a tab delimiter.

    Returns
    -------
    This returns a tuple of the whole extent for the uniform grid to be made of the input file (0,n1-1, 0,n2-1, 0,n3-1). This output should be directly passed to util.SetOutputWholeExtent() when used in programmable filters or source generation on the pipeline.

    """
    with open(FileName) as f:
        if (useTab):
            deli = '\t'
        reader = csv.reader(f, delimiter=deli)
        h = reader.next()
        n1,n2,n3 = int(h[0]), int(h[1]), int(h[2])
        f.close()
        return (0,n1-1, 0,n2-1, 0,n3-1)
