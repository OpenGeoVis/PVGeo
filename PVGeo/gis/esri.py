__all__ = [
    'EsriGridReader',
]

import vtk
import numpy as np
from vtk.util import numpy_support as nps
# Import Helpers:
from .. import _helpers
from ..readers import DelimitedTextReader


class EsriGridReader(DelimitedTextReader):
    """See details: https://en.wikipedia.org/wiki/Esri_grid
    """
    __displayname__ = 'Esri Grid Reader'
    __type__ = 'reader'
    def __init__(self, outputType='vtkImageData', **kwargs):
        DelimitedTextReader.__init__(self, outputType=outputType, **kwargs)
        # These are attributes the derived from file contents:
        self.SetDelimiter(' ')
        self.__nx = None
        self.__ny = None
        self.__xo = None
        self.__yo = None
        self.__cellsize = None
        self.__dataName = 'Data'
        self.NODATA_VALUE = -9999

    def _ExtractHeader(self, content):
        try:
            self.__nx = int(content[0].split()[1])
            self.__ny = int(content[1].split()[1])
            self.__xo = float(content[2].split()[1])
            self.__yo = float(content[3].split()[1])
            self.__cellsize = float(content[4].split()[1])
            self.NODATA_VALUE = float(content[5].split()[1])
        except ValueError:
            raise _helpers.PVGeoError('This file is not in proper Esri ASCII Grid format.')
        return [self.__dataName], content[6::]


    def _GetRawData(self, idx=0):
        """This will return the proper data for the given timestep.
        This method handles Surfer's NaN data values and checkes the value range
        """
        # data =  self._data[idx]
        # args = np.argwhere(data == self.NODATA_VALUE)
        # # TODO: how should we handle bad values on integer arrays?
        # data = np.array(data, dtype=float)
        # data[args] = np.nan
        # return data
        data =  self._data[idx]
        nans = data >= self.NODATA_VALUE
        if np.any(nans):
            data = np.ma.masked_where(nans, data)
        return data



    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to get data for current timestep and populate the output data object.
        """
        # Get output:
        output = self.GetOutputData(outInfo, 0)

        if self.NeedToRead():
            self._ReadUpFront()

        # Get requested time index
        i = _helpers.GetRequestedTime(self, outInfo)

        # Build the data object
        output.SetOrigin(self.__xo, self.__yo, 0.0)
        output.SetSpacing(self.__cellsize, self.__cellsize, self.__cellsize)
        output.SetDimensions(self.__nx, self.__ny, 1)

        # Now add data values as point data
        data = self._GetRawData(idx=i).flatten(order='F')
        vtkarr = nps.numpy_to_vtk(data)
        vtkarr.SetName(self.__dataName)
        output.GetPointData().AddArray(vtkarr)

        return 1

    def RequestInformation(self, request, inInfo, outInfo):
        """Used by pipeline to set grid extents.
        """
        if self.NeedToRead():
            self._ReadUpFront()
        # Call parent to handle time stuff
        DelimitedTextReader.RequestInformation(self, request, inInfo, outInfo)
        # Now set whole output extent
        info = outInfo.GetInformationObject(0)
        # Set WHOLE_EXTENT: This is absolutely necessary
        ext = (0,self.__nx-1, 0,self.__ny-1, 0,1-1)
        info.Set(vtk.vtkStreamingDemandDrivenPipeline.WHOLE_EXTENT(), ext, 6)
        return 1

    def SetDataName(self, dataName):
        if self.__dataName != dataName:
            self.__dataName = dataName
            self.Modified(readAgain=False)

    def GetDataName(self):
        return self.__dataName
