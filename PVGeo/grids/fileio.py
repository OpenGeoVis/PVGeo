"""This module contains general grid readers and writers for programs like Surfer."""

__all__ = [
    'SurferGridReader',
    'WriteImageDataToSurfer',
    'EsriGridReader'
]

# NOTE: Surfer no data value: 1.70141E+38

import vtk
import numpy as np
import pandas as pd

import sys
if sys.version_info < (3,):
    from StringIO import StringIO
else:
    from io import StringIO


# Import Helpers:
from ..base import WriterBase
from ..readers import DelimitedTextReader
from .. import _helpers
from .. import interface


#------------------------------------------------------------------------------

class SurferGridReader(DelimitedTextReader):
    """Read 2D ASCII Surfer grid files
    """
    __displayname__ = 'Surfer Grid Reader'
    __category__ = 'reader'
    def __init__(self, outputType='vtkImageData', **kwargs):
        DelimitedTextReader.__init__(self, outputType=outputType, **kwargs)
        self.SetDelimiter(' ')
        self.__nx = None
        self.__ny = None
        self.__xrng = None
        self.__yrng = None
        self.__drng = None
        self.__dataName = 'Data'


    def _ExtractHeader(self, content):
        self.__header = content[0] # this is grid type? DSAA
        try:
            dims = content[1].split()
            ny, nx = int(dims[0]), int(dims[1]) # number of data columns
            # Next three lines are min/max of XYZ
            x = content[2].split()
            xmin, xmax = float(x[0]), float(x[1])
            y = content[3].split()
            ymin, ymax = float(y[0]), float(y[1])
            d = content[4].split()
            dmin, dmax = float(d[0]), float(d[1])
            self.__nx = nx
            self.__ny = ny
            self.__xrng = (xmin, xmax)
            self.__yrng = (ymin, ymax)
            self.__drng = (dmin, dmax)
        except ValueError:
            raise _helpers.PVGeoError('This file is not in proper Surfer format.')
        return [self.__dataName], content[5::]


    def _FileContentsToDataFrame(self, contents):
        """Creates a dataframe with a sinlge array for the file data.
        """
        data = []
        for content in contents:
            arr = np.fromiter((float(s) for line in content for s in line.split()), dtype=float)
            df = pd.DataFrame(data=arr, columns=[self.GetDataName()])
            data.append(df)
        return data

    def _GetRawData(self, idx=0):
        """This will return the proper data for the given timestep.
        This method handles Surfer's NaN data values and checkes the value range
        """
        data =  self._data[idx]
        nans = data >= 1.70141e+38
        if np.any(nans):
            data = np.ma.masked_where(nans, data)
        err_msg = "{} of data ({}) doesn't match that set by file ({})."
        dmin, dmax = self.__drng
        if not np.allclose(dmin, data.min()):
            raise RuntimeError(err_msg.format('Min', data.min(), dmin))
        if not np.allclose(dmax, data.max()):
            raise RuntimeError(err_msg.format('Max', data.max(), dmax))
        return data



    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to get data for current timestep and populate the output data object.
        """
        # Get output:
        output = self.GetOutputData(outInfo, 0)

        if self.NeedToRead():
            self._ReadUpFront()

        # Get requested time index
        i = _helpers.getRequestedTime(self, outInfo)

        # Build the data object
        output.SetOrigin(self.__xrng[0], self.__yrng[0], 0.0)
        xspac = (self.__xrng[1]-self.__xrng[0])/self.__nx
        yspac = (self.__yrng[1]-self.__yrng[0])/self.__ny
        output.SetSpacing(xspac, yspac, 100.0)
        output.SetDimensions(self.__nx, self.__ny, 1)

        # Now add data values as point data
        data = self._GetRawData(idx=i).values.reshape((self.__nx, self.__ny)).flatten(order='F')
        vtkarr = interface.convertArray(data, name=self.__dataName)
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



#------------------------------------------------------------------------------

class WriteImageDataToSurfer(WriterBase):
    """Write a 2D ``vtkImageData`` object to the Surfer grid format"""
    __displayname__ = 'Write ``vtkImageData`` to Surfer Format'
    __category__ = 'writer'
    def __init__(self):
        WriterBase.__init__(self, inputType='vtkImageData', ext='grd')
        self.__inputArray = [None, None]


    def PerformWriteOut(self, inputDataObject, filename):
        img = inputDataObject

        # Check dims: make sure 2D
        # TODO: handle any orientation
        nx, ny, nz = img.GetDimensions()
        if nx == ny == 1 and nz != 1:
            raise RuntimeError('Only 2D data on the XY plane is supported at this time.')

        ox, oy, oz = img.GetOrigin()
        dx, dy, dz = img.GetSpacing()

        # Get data ranges
        xmin, xmax = ox, ox + dx*nx
        ymin, ymax = oy, oy + dy*ny

        # Note user has to select a single array to save out
        field, name = self.__inputArray[0], self.__inputArray[1]
        vtkarr = _helpers.getVTKArray(img, field, name)
        arr = interface.convertArray(vtkarr)
        dmin, dmax = arr.min(), arr.max()

        arr = arr.reshape((nx, ny), order='F')

        meta = 'DSAA\n%d %d\n%f %f\n%f %f\n%f %f' % (ny, nx, xmin, xmax,
                                                     ymin, ymax, dmin, dmax)
        # Now write out the data!
        np.savetxt(filename, arr, header=meta, comments='', fmt=self.GetFormat())


        return 1


    def SetInputArrayToProcess(self, idx, port, connection, field, name):
        """Used to the inpput array / the data value (z-value) to write for the Surfer format

        Args:
            idx (int): the index of the array to process
            port (int): input port (use 0 if unsure)
            connection (int): the connection on the port (use 0 if unsure)
            field (int): the array field (0 for points, 1 for cells, 2 for field, and 6 for row)
            name (int): the name of the array
        """
        if self.__inputArray[0] != field:
            self.__inputArray[0] = field
            self.Modified()
        if self.__inputArray[1] != name:
            self.__inputArray[1] = name
            self.Modified()
        return 1

    def Apply(self, inputDataObject, arrayName):
        self.SetInputDataObject(inputDataObject)
        arr, field = _helpers.searchForArray(inputDataObject, arrayName)
        self.SetInputArrayToProcess(0, 0, 0, field, arrayName)
        self.Update()
        return self.GetOutput()

    def Write(self, inputDataObject=None, arrayName=None):
        """Perfrom the write out."""
        if inputDataObject:
            self.SetInputDataObject(inputDataObject)
            if arrayName:
                arr, field = _helpers.searchForArray(inputDataObject, arrayName)
                self.SetInputArrayToProcess(0, 0, 0, field, arrayName)
        self.Modified()
        self.Update()

###############################################################################


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

    def _FileContentsToDataFrame(self, contents):
        """Creates a dataframe with a sinlge array for the file data.
        """
        data = []
        for content in contents:
            arr = np.fromiter((float(s) for line in content for s in line.split()), dtype=float)
            df = pd.DataFrame(data=arr, columns=[self.GetDataName()])
            data.append(df)
        return data


    def _GetRawData(self, idx=0):
        """This will return the proper data for the given timestep.
        This method handles Surfer's NaN data values and checkes the value range
        """
        data =  self._data[idx].values.astype(np.float)
        nans = np.argwhere(data == self.NODATA_VALUE)
        # if np.any(nans):
        #     data = np.ma.masked_where(nans, data)
        data[nans] = np.nan
        return data.flatten()



    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to get data for current timestep and populate the output data object.
        """
        # Get output:
        output = self.GetOutputData(outInfo, 0)

        if self.NeedToRead():
            self._ReadUpFront()

        # Get requested time index
        i = _helpers.getRequestedTime(self, outInfo)

        # Build the data object
        output.SetOrigin(self.__xo, self.__yo, 0.0)
        output.SetSpacing(self.__cellsize, self.__cellsize, self.__cellsize)
        output.SetDimensions(self.__nx, self.__ny, 1)

        # Now add data values as point data
        data = self._GetRawData(idx=i).flatten(order='F')
        vtkarr = interface.convertArray(data, name=self.__dataName)
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
