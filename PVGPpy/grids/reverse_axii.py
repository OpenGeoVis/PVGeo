__all__ = [
    'reverseGridAxii',
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
