__all__ = [
    'SGeMSGridReader',
]

import numpy as np
from vtk.util import numpy_support as nps
import vtk

from .gslib import GSLibReader
from .. import _helpers


class SGeMSGridReader(GSLibReader):
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
    def __init__(self):
        GSLibReader.__init__(self, outputType='vtkImageData')
        self.__extent = None

    def _ReadExtent(self):
        """
        @desc:
        Reads the input file for the SGeMS format to get output extents. Computationally inexpensive method to discover whole output extent.

        @params:
        FileName : str : req : The file name / absolute path for the input file in SGeMS grid format.
        deli : str : opt : The input files delimiter. To use a tab delimiter please set the `useTab`.
        useTab : boolean : opt : A boolean that describes whether to use a tab delimiter.
        comments : char : opt : The identifier for comments within the file.

        @return:
        tuple : This returns a tuple of the whole extent for the uniform grid to be made of the input file (0,n1-1, 0,n2-1, 0,n3-1). This output should be directly passed to `util.SetOutputWholeExtent()` when used in programmable filters or source generation on the pipeline.

        """
        # Read first file... extent cannot vary with time
        # TODO: make more efficient to only reader header of file
        fileLines = self._GetFileLines(idx=0)
        h = fileLines[0+self.GetSkipRows()].split(self._GetDeli())
        n1,n2,n3 = int(h[0]), int(h[1]), int(h[2])
        return (0,n1-1, 0,n2-1, 0,n3-1)

    def _ExtractHeader(self, fileLines):
        titles, fileLines = GSLibReader._ExtractHeader(self, fileLines)
        h = self.GetFileHeader().split(self._GetDeli())
        self.__extent = int(h[0]), int(h[1]), int(h[2])
        return titles, fileLines

    def RequestData(self, request, inInfo, outInfo):
        # Get output:
        output = vtk.vtkImageData.GetData(outInfo)
        # Get requested time index
        i = _helpers.GetRequestedTime(self, outInfo)
        # Perform Read
        fileLines = self._GetFileLines(idx=i)
        titles, fileLines = self._ExtractHeader(fileLines)
        data = self._GetNumPyData(fileLines)
        # Generate the data object
        n1, n2, n3 = self.__extent
        output.SetDimensions(n1, n2, n3)
        output.SetExtent(0,n1-1, 0,n2-1, 0,n3-1)
        # Use table generater and convert because its easy:
        table = vtk.vtkTable()
        _helpers._placeArrInTable(data, titles, table)
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
