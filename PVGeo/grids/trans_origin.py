__all__ = [
    'TranslateGridOrigin'
]

import vtk
import numpy as np
# Import Helpers:
from ..base import FilterBase


#---- Translate Grid Origin ----#

class TranslateGridOrigin(FilterBase):
    """This filter will translate the origin of `vtkImageData` to any specified Corner of the data set assuming it is currently in the South West Bottom Corner (will not work if Corner was moved prior).
    """
    __displayname__ = 'Translate Grid Origin'
    __category__ = 'filter'
    def __init__(self, corner=1):
        FilterBase.__init__(self,
            nInputPorts=1, inputType='vtkImageData',
            nOutputPorts=1, outputType='vtkImageData')
        self.__corner = corner


    def _Translate(self, pdi, pdo):
        if pdo is None:
            pdo = vtk.vtkImageData()

        [nx, ny, nz] = pdi.GetDimensions()
        [sx, sy, sz] = pdi.GetSpacing()
        [ox, oy, oz] = pdi.GetOrigin()

        pdo.DeepCopy(pdi)

        xx,yy,zz = 0.0,0.0,0.0

        if self.__corner == 1:
            # South East Bottom
            xx = ox - (nx-1)*sx
            yy = oy
            zz = oz
        elif self.__corner == 2:
            # North West Bottom
            xx = ox
            yy = oy - (ny-1)*sy
            zz = oz
        elif self.__corner == 3:
            # North East Bottom
            xx = ox - (nx-1)*sx
            yy = oy - (ny-1)*sy
            zz = oz
        elif self.__corner == 4:
            # South West Top
            xx = ox
            yy = oy
            zz = oz - (nz-1)*sz
        elif self.__corner == 5:
            # South East Top
            xx = ox - (nx-1)*sx
            yy = oy
            zz = oz - (nz-1)*sz
        elif self.__corner == 6:
            # North West Top
            xx = ox
            yy = oy - (ny-1)*sy
            zz = oz - (nz-1)*sz
        elif self.__corner == 7:
            # North East Top
            xx = ox - (nx-1)*sx
            yy = oy - (ny-1)*sy
            zz = oz - (nz-1)*sz

        pdo.SetOrigin(xx, yy, zz)

        return pdo

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output.
        """
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        pdo = self.GetOutputData(outInfo, 0)
        # Perfrom task
        self._Translate(pdi, pdo)
        return 1


    #### Seters and Geters ####


    def SetCorner(self, corner):
        """Set the corner to use

        Args:
            corner (int) : corner location; see note.

        Note:
            * 1: South East Bottom
            * 2: North West Bottom
            * 3: North East Bottom
            * 4: South West Top
            * 5: South East Top
            * 6: North West Top
            * 7: North East Top
        """
        if self.__corner != corner:
            self.__corner = corner
            self.Modified()
