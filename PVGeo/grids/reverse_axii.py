__all__ = [
    'ReverseImageDataAxii',
]

from vtk.util import numpy_support as nps
from vtk.numpy_interface import dataset_adapter as dsa
import numpy as np
# Import Helpers:
from ..base import FilterBase
from .. import _helpers


#---- Reverse Grid Axii ----#


class ReverseImageDataAxii(FilterBase):
    """This filter will flip ``vtkImageData`` on any of the three cartesian axii. A checkbox is provided for each axis on which you may desire to flip the data."""
    __displayname__ = 'Reverse Image Data Axii'
    __type__ = 'filter'
    def __init__(self, axes=[True, True, True]):
        FilterBase.__init__(self,
            nInputPorts=1, inputType='vtkImageData',
            nOutputPorts=1, outputType='vtkImageData')
        self.__axes = axes[::-1] # Z Y X (FORTRAN)

    def _ReverseGridAxii(self, idi, ido):
        # Copy over input to output to be flipped around
        # Deep copy keeps us from messing with the input data
        ox, oy, oz = idi.GetOrigin()
        ido.SetOrigin(ox, oy, oz)
        sx, sy, sz = idi.GetSpacing()
        ido.SetSpacing(sx, sy, sz)
        ext = idi.GetExtent()
        nx, ny, nz = ext[1]+1, ext[3]+1, ext[5]+1
        ido.SetDimensions(nx, ny, nz)

        widi = dsa.WrapDataObject(idi)
        # Iterate over all array in the PointData
        for j in range(idi.GetPointData().GetNumberOfArrays()):
            # Go through each axis and rotate if needed
            arr = widi.PointData[j]
            arr = np.reshape(arr, (nz,ny,nx))
            for i in range(3):
                if self.__axes[i]:
                    arr = np.flip(arr, axis=i)
            # Now add that data array to the output
            data = nps.numpy_to_vtk(num_array=arr.flatten(), deep=True)
            data.SetName(idi.GetPointData().GetArrayName(j))
            ido.GetPointData().AddArray(data)

        # Iterate over all array in the CellData
        for j in range(idi.GetCellData().GetNumberOfArrays()):
            # Go through each axis and rotate if needed
            arr = widi.CellData[j]
            arr = np.reshape(arr, (nz-1,ny-1,nx-1))
            for i in range(3):
                if self.__axes[i]:
                    arr = np.flip(arr, axis=i)
            # Now add that data array to the output
            data = nps.numpy_to_vtk(num_array=arr.flatten(), deep=True)
            data.SetName(idi.GetCellData().GetArrayName(j))
            ido.GetCellData().AddArray(data)

        return ido

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output.
        """
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        pdo = self.GetOutputData(outInfo, 0)
        # Perfrom task
        self._ReverseGridAxii(pdi, pdo)
        return 1


    #### Seters and Geters ####


    def SetFlipX(self, flag):
        """Set the filter to flip th input data along the X-axis
        """
        if self.__axes[2] != flag:
            self.__axes[2] = flag
            self.Modified()

    def SetFlipY(self, flag):
        """Set the filter to flip th input data along the Y-axis
        """
        if self.__axes[1] != flag:
            self.__axes[1] = flag
            self.Modified()

    def SetFlipZ(self, flag):
        """Set the filter to flip th input data along the Z-axis
        """
        if self.__axes[0] != flag:
            self.__axes[0] = flag
            self.Modified()
