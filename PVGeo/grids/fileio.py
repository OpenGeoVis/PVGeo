"""This module contains general grid readers and writers for programs like Surfer."""

__all__ = [
    'SurferGridReader',
    'WriteImageDataToSurfer',
    'EsriGridReader',
    'LandsatReader',
]

# NOTE: Surfer no data value: 1.70141E+38

import vtk
import numpy as np
import pandas as pd

# import sys
# sys.path.append('/Users/bane/Documents/OpenGeoVis/Software/espatools')
import espatools

import sys
if sys.version_info < (3,):
    from StringIO import StringIO
else:
    from io import StringIO


# Import Helpers:
from ..base import WriterBase, ReaderBaseBase
from ..readers import DelimitedTextReader
from .. import _helpers
from .. import interface


################################################################################

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



################################################################################

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



################################################################################


class LandsatReader(ReaderBaseBase):
    """A reader that will handle ESPA XML files for Landsat Imagery. This reader
    uses the ``espatools`` package to read Landsat rasters (band sets) and creates
    vtkImageData with each band as point data
    """
    __displayname__ = 'Landsat XML Reader'
    __category__ = 'reader'
    def __init__(self, **kwargs):
        ReaderBaseBase.__init__(self, outputType='vtkImageData', **kwargs)
        self.__reader = espatools.RasterSetReader()
        self.__raster = None
        # Properties:
        self._dataselection = vtk.vtkDataArraySelection()
        self._dataselection.AddObserver("ModifiedEvent", _helpers.createModifiedCallback(self))


    def Modified(self, readAgain=False):
        """Ensure default is overridden to be false so array selector can call.
        """
        ReaderBaseBase.Modified(self, readAgain=readAgain)


    def GetFileName(self):
        """Super class has file names as a list but we will only handle a single
        project file. This provides a conveinant way of making sure we only
        access that single file.
        A user could still access the list of file names using ``GetFileNames()``.
        """
        return ReaderBaseBase.GetFileNames(self, idx=0)


    #### Methods for performing the read ####

    def _GetFileContents(self, idx=None):
        """Reads XML meta data, no data read."""
        self.__reader.SetFileName(self.GetFileName())
        self.__raster = self.__reader.Read(meta_only=True)
        for n in self.__raster.bands.keys():
            self._dataselection.AddArray(n)
        self.NeedToRead(flag=False) # Only meta data has been read
        return

    def _ReadUpFront(self):
        return self._GetFileContents()

    def _GetRawData(self, idx=0):
        """Perfroms the read for the selected bands"""
        allowed = []
        for name in self.__raster.bands.keys():
            if self._dataselection.ArrayIsEnabled(name):
                allowed.append(name)
        self.__raster = self.__reader.Read(meta_only=False, allowed=allowed)
        return self.__raster

    def _BuildImageData(self, output):
        """Properly builds the output ``vtkImageData`` object"""
        if self.__raster is None:
            raise _helpers.PVGeoError('Raster invalid.')
        raster = self.__raster
        output.SetDimensions(raster.nsamps, raster.nlines, 1)
        output.SetSpacing(raster.pixel_size.x, raster.pixel_size.y, 1)
        corner = raster.global_metadata.projection_information.corner_point[0]
        output.SetOrigin(corner.x, corner.y, 0)
        return output


    #### Pipeline Methods ####

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output"""
        # Get output:
        output = vtk.vtkImageData.GetData(outInfo, 0)
        # Perform Read if needed
        if self.__raster is None:
            self._ReadUpFront()
        self._GetRawData()
        self._BuildImageData(output)
        # Now add the data based on what the user has selected
        for name, band in self.__raster.bands.items():
            output.GetPointData().AddArray(interface.convertArray(band.data.flatten(), name=name))
        try:
            colors = self.__raster.GetRGB().reshape((-1,3))
            output.GetPointData().SetScalars(interface.convertArray(colors, name='Colors'))
            output.GetPointData().SetActiveScalars("Colors")
        except RuntimeError:
            pass
        return 1

    def RequestInformation(self, request, inInfo, outInfo):
        """Used by pipeline to set grid extents."""
        # Call parent to handle time stuff
        ReaderBaseBase.RequestInformation(self, request, inInfo, outInfo)
        if self.__raster is None:
            self._ReadUpFront()
        # Now set whole output extent
        b = self.__raster.bands.get(list(self.__raster.bands.keys())[0])
        nx, ny, nz = b.nsamps, b.nlines, 1
        ext = (0,nx-1, 0,ny-1, 0,nz-1)
        info = outInfo.GetInformationObject(0)
        # Set WHOLE_EXTENT: This is absolutely necessary
        info.Set(vtk.vtkStreamingDemandDrivenPipeline.WHOLE_EXTENT(), ext, 6)
        return 1



    #### Seters and Geters for the GUI ####

    def GetDataSelection(self):
        """Used by ParaView GUI"""
        if self.NeedToRead():
            self._ReadUpFront()
        return self._dataselection
