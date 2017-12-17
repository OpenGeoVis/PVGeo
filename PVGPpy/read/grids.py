import numpy as np
import csv
import os
from vtk.util import numpy_support as nps
import vtk

def readSGeMSGrid(FileName, deli=' ', useTab=False):
    """
    Description
    -----------

    Parameters
    ----------

    Returns
    -------

    """
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

def getSGeMSExtent(FileName, deli=' ', useTab=False):
    """
    Description
    -----------

    Parameters
    ----------

    Returns
    -------

    """
    with open(FileName) as f:
        if (useTab):
            deli = '\t'
        reader = csv.reader(f, delimiter=deli)
        h = reader.next()
        n1,n2,n3 = int(h[0]), int(h[1]), int(h[2])
        f.close()
        return (0,n1-1, 0,n2-1, 0,n3-1)
