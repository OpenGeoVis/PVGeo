__all__ = [
    'sgemsGrid',
    'sgemsExtent'
]

import numpy as np
import csv
import os
from vtk.util import numpy_support as nps
import vtk

def sgemsGrid(FileName, deli=' ', useTab=False, skiprows=0, comments='#', pdo=None):
    """
    @desc:
        Generates vtkImageData from the uniform grid defined in the inout file in the SGeMS grid format. This format is simply the GSLIB format where the header line defines the dimensions of the uniform grid.

    @params:
        FileName : str : req : The file name / absolute path for the input file in SGeMS grid format.
        deli : str : opt : The input files delimiter. To use a tab delimiter please set the `useTab`.
        useTab : boolean : opt : A boolean that describes whether to use a tab delimiter.
        skiprows : int : opt : The integer number of rows to skip at the top of the file.
        comments : char : opt : The identifier for comments within the file.
        pdo : vtkImageData : opt : A pointer to the output data object.

    @return:
        vtkImageData : A uniformly spaced gridded volume of data from input file

    """
    from PVGPpy.read import gslib
    if pdo is None:
        pdo = vtk.vtkImageData() # vtkImageData

    table, header = gslib(FileName, deli=deli, useTab=useTab, skiprows=skiprows, comments='#', pdo=None)
    h = header.split(deli)
    n1,n2,n3 = int(h[0]), int(h[1]), int(h[2])

    pdo.SetDimensions(n1, n2, n3)
    pdo.SetExtent(0,n1-1, 0,n2-1, 0,n3-1)

    # now get arrays from table and add to point data of pdo
    for i in range(table.GetNumberOfColumns()):
        pdo.GetPointData().AddArray(table.GetColumn(i))
        #TODO: pdo.GetCellData().AddArray(VTK_data)
    del(table)
    return pdo

def sgemsExtent(FileName, deli=' ', useTab=False):
    """
    @desc:
    Reads the input file for the SGeMS format to get output extents. Computationally inexpensive method to discover whole output extent.

    @params:
    FileName : str : req : The file name / absolute path for the input file in SGeMS grid format.
    deli : str : opt : The input files delimiter. To use a tab delimiter please set the `useTab`.
    useTab : boolean : opt : A boolean that describes whether to use a tab delimiter.

    @return:
    tuple : This returns a tuple of the whole extent for the uniform grid to be made of the input file (0,n1-1, 0,n2-1, 0,n3-1). This output should be directly passed to `util.SetOutputWholeExtent()` when used in programmable filters or source generation on the pipeline.

    """
    with open(FileName) as f:
        if (useTab):
            deli = '\t'
        reader = csv.reader(f, delimiter=deli)
        h = reader.next()
        n1,n2,n3 = int(h[0]), int(h[1]), int(h[2])
        f.close()
    return (0,n1-1, 0,n2-1, 0,n3-1)
