__all__ = [
    'SGeMSGridReader',
]

import numpy as np
from vtk.util import numpy_support as nps
import vtk

from .gslib import GSLibReader
from .. import _helpers


class SGeMSGridReader(GSLibReader):
    """@desc: Generates `vtkImageData` from the uniform grid defined in the inout file in the SGeMS grid format. This format is simply the GSLIB format where the header line defines the dimensions of the uniform grid.
    """
    def __init__(self):
        GSLibReader.__init__(self, outputType='vtkImageData')
        self.__extent = None

    def _ReadExtent(self):
        """
        @desc:
        Reads the input file for the SGeMS format to get output extents. Computationally inexpensive method to discover whole output extent.

        @return:
        tuple : This returns a tuple of the whole extent for the uniform grid to be made of the input file (0,n1-1, 0,n2-1, 0,n3-1). This output should be directly passed to `util.SetOutputWholeExtent()` when used in programmable filters or source generation on the pipeline.

        """
        # Read first file... extent cannot vary with time
        # TODO: make more efficient to only reader header of file
        fileLines = self._GetFileContents(idx=0)
        h = fileLines[0+self.GetSkipRows()].split(self._GetDeli())
        try:
            n1,n2,n3 = int(h[0]), int(h[1]), int(h[2])
        except ValueError:
            raise _helpers.PVGeoError('File not in proper SGeMS Grid fromat.')
        return (0,n1-1, 0,n2-1, 0,n3-1)

    def _ExtractHeader(self, content):
        titles, content = GSLibReader._ExtractHeader(self, content)
        h = self.GetFileHeader().split(self._GetDeli())
        try:
            if self.__extent is None:
                self.__extent = (int(h[0]), int(h[1]), int(h[2]))
            elif self.__extent != (int(h[0]), int(h[1]), int(h[2])):
                raise _helpers.PVGeoError('Grid dimensions change in file time series.')
        except ValueError:
            raise _helpers.PVGeoError('File not in proper SGeMS Grid fromat.')
        return titles, content

    def RequestData(self, request, inInfo, outInfo):
        # Get output:
        output = vtk.vtkImageData.GetData(outInfo)
        # Get requested time index
        i = _helpers.GetRequestedTime(self, outInfo)
        if self.NeedToRead():
            self._ReadUpFront()
        # Generate the data object
        n1, n2, n3 = self.__extent
        output.SetDimensions(n1, n2, n3)
        output.SetExtent(0,n1-1, 0,n2-1, 0,n3-1)
        # Use table generater and convert because its easy:
        table = vtk.vtkTable()
        _helpers.placeArrInTable(self._GetRawData(idx=i), self.GetTitles(), table)
        # now get arrays from table and add to point data of pdo
        for i in range(table.GetNumberOfColumns()):
            output.GetPointData().AddArray(table.GetColumn(i))
            #TODO: maybe we ought to add the data as cell data
        del(table)
        return 1


    def RequestInformation(self, request, inInfo, outInfo):
        # Call parent to handle time stuff
        GSLibReader.RequestInformation(self, request, inInfo, outInfo)
        # Now set whole output extent
        ext = self._ReadExtent()
        info = outInfo.GetInformationObject(0)
        # Set WHOLE_EXTENT: This is absolutely necessary
        info.Set(vtk.vtkStreamingDemandDrivenPipeline.WHOLE_EXTENT(), ext, 6)
        return 1
