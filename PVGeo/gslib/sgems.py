__all__ = [
    'SGeMSGridReader',
    'WriteImageDataToSGeMS',
]

__displayname__ = 'SGeMS File I/O'

import os
import re

import numpy as np
import pandas as pd
import vtk

from .. import _helpers, interface
from ..base import WriterBase
from .gslib import GSLibReader


class SGeMSGridReader(GSLibReader):
    """Generates ``vtkImageData`` from the uniform grid defined in the inout
    file in the SGeMS grid format. This format is simply the GSLIB format where
    the header line defines the dimensions of the uniform grid.
    """
    __displayname__ = 'SGeMS Grid Reader'
    __category__ = 'reader'
    extensions = GSLibReader.extensions + 'gslibgrid mtxset'
    description = 'PVGeo: SGeMS Uniform Grid'
    def __init__(self, origin=(0.0, 0.0, 0.0), spacing=(1.0, 1.0, 1.0), **kwargs):
        GSLibReader.__init__(self, outputType='vtkImageData', **kwargs)
        self.__extent = None
        self.__origin = origin
        self.__spacing = spacing
        self.__mask = kwargs.get("mask", -9966699.)

    def __parse_extent(self, header):
        regex = re.compile('\S\s\((\d+)x(\d+)x(\d+)\)')
        dims = regex.findall(header)
        if len(dims) < 1:
            regex = re.compile('(\d+) (\d+) (\d+)')
            dims = regex.findall(header)
        if len(dims) < 1:
            raise _helpers.PVGeoError('File not in proper SGeMS Grid fromat.')
        dims = dims[0]
        return int(dims[0]), int(dims[1]), int(dims[2])

    def _read_extent(self):
        """Reads the input file for the SGeMS format to get output extents.
        Computationally inexpensive method to discover whole output extent.

        Return:
            tuple :
                This returns a tuple of the whole extent for the uniform
                grid to be made of the input file (0,n1-1, 0,n2-1, 0,n3-1).
                This output should be directly passed to set the whole output
                extent.

        """
        # Read first file... extent cannot vary with time
        # TODO: make more efficient to only reader header of file
        fileLines = self._get_file_contents(idx=0)
        h = fileLines[0+self.get_skip_rows()]
        n1,n2,n3 = self.__parse_extent(h)
        return (0,n1, 0,n2, 0,n3)

    def _extract_header(self, content):
        """Internal helper to parse header info for the SGeMS file format"""
        titles, content = GSLibReader._extract_header(self, content)
        h = self.get_file_header()
        try:
            if self.__extent is None:
                self.__extent = self.__parse_extent(h)
            elif self.__extent != (self.__parse_extent(h)):
                raise _helpers.PVGeoError('Grid dimensions change in file time series.')
        except ValueError:
            raise _helpers.PVGeoError('File not in proper SGeMS Grid fromat.')
        return titles, content

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to get output data object for given time step.
        Constructs the ``vtkImageData``
        """
        # Get output:
        output = vtk.vtkImageData.GetData(outInfo)
        # Get requested time index
        i = _helpers.get_requested_time(self, outInfo)
        if self.need_to_read():
            self._read_up_front()
        # Generate the data object
        n1, n2, n3 = self.__extent
        dx, dy, dz = self.__spacing
        ox, oy, oz = self.__origin
        output.SetDimensions(n1+1, n2+1, n3+1)
        output.SetSpacing(dx, dy, dz)
        output.SetOrigin(ox, oy, oz)
        # Use table generator and convert because its easy:
        table = vtk.vtkTable()
        df = self._get_raw_data(idx=i)
        # Replace all masked values with NaN
        df.replace(self.__mask, np.nan, inplace=True)
        interface.data_frame_to_table(df, table)
        # now get arrays from table and add to point data of pdo
        for i in range(table.GetNumberOfColumns()):
            output.GetCellData().AddArray(table.GetColumn(i))
        del(table)
        return 1


    def RequestInformation(self, request, inInfo, outInfo):
        """Used by pipeline to set grid extents.
        """
        # Call parent to handle time stuff
        GSLibReader.RequestInformation(self, request, inInfo, outInfo)
        # Now set whole output extent
        ext = self._read_extent()
        info = outInfo.GetInformationObject(0)
        # Set WHOLE_EXTENT: This is absolutely necessary
        info.Set(vtk.vtkStreamingDemandDrivenPipeline.WHOLE_EXTENT(), ext, 6)
        return 1


    def set_spacing(self, dx, dy, dz):
        """Set the spacing for each axial direction"""
        spac = (dx, dy, dz)
        if self.__spacing != spac:
            self.__spacing = spac
            self.Modified(read_again=False)

    def set_origin(self, ox, oy, oz):
        """Set the origin corner of the grid"""
        origin = (ox, oy, oz)
        if self.__origin != origin:
            self.__origin = origin
            self.Modified(read_again=False)





class WriteImageDataToSGeMS(WriterBase):
    """Writes a ``vtkImageData`` object to the SGeMS uniform grid format.
    This writer can only handle point data. Note that this will only handle
    CellData as that is convention with SGeMS.
    """
    __displayname__ = 'Write ``vtkImageData`` To SGeMS Grid Format'
    __category__ = 'writer'
    def __init__(self, inputType='vtkImageData'):
        WriterBase.__init__(self, inputType=inputType, ext='SGeMS')


    def perform_write_out(self, input_data_object, filename, object_name):
        """Write out the input ``vtkImage`` data to the SGeMS file format"""
        # Get the input data object
        grd = input_data_object

        # Get grid dimensions and minus one becuase this defines nodes
        nx, ny, nz = grd.GetDimensions()
        nx -= 1
        ny -= 1
        nz -= 1

        numArrs = grd.GetCellData().GetNumberOfArrays()
        arrs = []

        titles = []
        # Get data arrays
        for i in range(numArrs):
            vtkarr = grd.GetCellData().GetArray(i)
            arrs.append(interface.convert_array(vtkarr))
            titles.append(vtkarr.GetName())

        datanames = '\n'.join(titles)

        df = pd.DataFrame(np.array(arrs).T)

        with open(filename, 'w') as f:
            f.write('%d %d %d\n' % (nx, ny, nz))
            f.write('%d\n' % len(titles))
            f.write(datanames)
            f.write('\n')
            df.to_csv(f, sep=' ', header=None, index=False, float_format=self.get_format())

        return 1
