__all__ = [
    'reverseGridAxii',
    'translateGridOrigin'
]

import vtk
from vtk.util import numpy_support as nps
import numpy as np


#---- Reverse Grid Axii ----#




def reverseGridAxii(pdi, axes=(True,True,True), pdo=None):
    """
    Reverses data along different axial directions

    TODO: Description
    """
    if pdo is None:
        pdo = vtk.vtkImageData()

    # Copy over input to output to be flipped around
    # Deep copy keeps us from messing with the input data
    pdo.DeepCopy(pdi)

    # Iterate over all array in the PointData
    for j in range(pdo.GetPointData().GetNumberOfArrays()):
        # Swap Scalars with all Arrays in PointData so that all data gets filtered
        scal = pdo.GetPointData().GetScalars()
        arr = pdi.GetPointData().GetArray(j)
        pdo.GetPointData().SetScalars(arr)
        pdo.GetPointData().AddArray(scal)
        for i in range(3):
            # Rotate ImageData on each axis if needed
            # Go through each axis and rotate if needed
            # Note: ShallowCopy is necessary!!
            if axes[i]:
                flipper = vtk.vtkImageFlip()
                flipper.SetInputData(pdo)
                flipper.SetFilteredAxis(i)
                flipper.Update()
                flipper.UpdateWholeExtent()
                pdo.ShallowCopy(flipper.GetOutput())
    return pdo




#---- Translate Grid Origin ----#


def translateGridOrigin(pdi, corner=1, pdo=None):
    """
    TODO: Description


    <Entry value="1" text="South East Bottom"/>
    <Entry value="2" text="North West Bottom"/>
    <Entry value="3" text="North East Bottom"/>
    <Entry value="4" text="South West Top"/>
    <Entry value="5" text="South East Top"/>
    <Entry value="6" text="North West Top"/>
    <Entry value="7" text="North East Top"/>
    """
    if pdo is None:
        pdo = vtk.vtkImageData()

    [nx, ny, nz] = pdi.GetDimensions()
    [ox, oy, oz] = pdi.GetOrigin()

    pdo.DeepCopy(pdi)

    xx,yy,zz = 0.0,0.0,0.0

    if Corner == 1:
        # South East Bottom
        xx = ox - nx
        yy = oy
        zz = oz
    elif Corner == 2:
        # North West Bottom
        xx = ox
        yy = oy - ny
        zz = oz
    elif Corner == 3:
        # North East Bottom
        xx = ox - nx
        yy = oy - ny
        zz = oz
    elif Corner == 4:
        # South West Top
        xx = ox
        yy = oy
        zz = oz - nz
    elif Corner == 5:
        # South East Top
        xx = ox - nx
        yy = oy
        zz = oz - nz
    elif Corner == 6:
        # North West Top
        xx = ox
        yy = oy - ny
        zz = oz - nz
    elif Corner == 7:
        # North East Top
        xx = ox - nx
        yy = oy - ny
        zz = oz - nz

    pdo.SetOrigin(xx, yy, zz)

    return pdo
