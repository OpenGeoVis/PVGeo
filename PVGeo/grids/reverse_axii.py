__all__ = [
    'ReverseImageDataAxii',
]

import vtk
from vtk.util import numpy_support as nps
import numpy as np
# Import Helpers:
from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase
from .. import _helpers


#---- Reverse Grid Axii ----#


class ReverseImageDataAxii(VTKPythonAlgorithmBase):
    def __init__(self):
        VTKPythonAlgorithmBase.__init__(self,
            nInputPorts=1, inputType='vtkImageData',
            nOutputPorts=1, outputType='vtkImageData')
        self.__axes = [True, True, True]

    def _ReverseGridAxii(self, pdi, pdo):
        """
        Reverses data along different axial directions

        TODO: Description
        """

        # Copy over input to output to be flipped around
        # Deep copy keeps us from messing with the input data
        pdo.DeepCopy(pdi)
        print(self.__axes)

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
                if self.__axes[i]:
                    flipper = vtk.vtkImageFlip()
                    flipper.SetInputData(pdo)
                    flipper.SetFilteredAxis(i)
                    flipper.Update()
                    flipper.UpdateWholeExtent()
                    pdo.ShallowCopy(flipper.GetOutput())
        # TODO: flip the cell data as well!
        return pdo

    def RequestData(self, request, inInfo, outInfo):
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        pdo = self.GetOutputData(outInfo, 0)
        # Perfrom task
        self._ReverseGridAxii(pdi, pdo)
        return 1


    #### Seters and Geters ####


    def SetFlipX(self, flag):
        if self.__axes[0] != flag:
            self.__axes[0] = flag
            self.Modified()

    def SetFlipY(self, flag):
        if self.__axes[1] != flag:
            self.__axes[1] = flag
            self.Modified()

    def SetFlipZ(self, flag):
        if self.__axes[2] != flag:
            self.__axes[2] = flag
            self.Modified()
