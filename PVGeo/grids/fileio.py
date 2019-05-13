"""This module contains general grid readers and writers for programs like Surfer."""

__all__ = [
    'SurferGridReader',
    'WriteImageDataToSurfer',
    'EsriGridReader',
    'LandsatReader',
    'WriteCellCenterData',
]

__displayname__ = 'File I/O'

# NOTE: Surfer no data value: 1.70141E+38

import re
import struct
import sys
import warnings

import numpy as np
import pandas as pd
import properties
import vtk
from vtk.numpy_interface import dataset_adapter as dsa

import espatools

from .. import _helpers, interface
from ..base import ReaderBase, ReaderBaseBase, WriterBase
from ..readers import DelimitedTextReader




################################################################################


class GridInfo(properties.HasProperties):
    """Internal helper class to store Surfer grid properties and create
    ``vtkImageData`` objects from them.
    """
    ny = properties.Integer('number of columns', min=2)
    nx = properties.Integer('number of rows', min=2)
    xll = properties.Float('x-value of lower-left corner')
    yll = properties.Float('y-value of lower-left corner')
    dx = properties.Float('x-axis spacing')
    dy = properties.Float('y-axis spacing')
    dmin = properties.Float('minimum data value', required=False)
    dmax = properties.Float('maximum data value', required=False)
    data = properties.Array('grid of data values', shape=('*',))

    def mask(self):
        """Mask the no data value"""
        data = self.data
        nans = data >= 1.701410009187828e+38
        if np.any(nans):
            data = np.ma.masked_where(nans, data)
        err_msg = "{} of data ({}) doesn't match that set by file ({})."
        if not np.allclose(self.dmin, np.nanmin(data)):
            raise _helpers.PVGeoError(err_msg.format('Min', np.nanmin(data), self.dmin))
        if not np.allclose(self.dmax, np.nanmax(data)):
            raise _helpers.PVGeoError(err_msg.format('Max', np.nanmax(data), self.dmax))
        self.data = data
        return

    def toVTK(self, output=None, z=0.0, dz=1.0, data_name='Data'):
        """Convert to a ``vtkImageData`` object"""
        self.mask()
        self.validate()
        if output is None:
            output = vtk.vtkImageData()
        # Build the data object
        output.SetOrigin(self.xll, self.yll, z)
        output.SetSpacing(self.dx, self.dy, dz)
        output.SetDimensions(self.nx, self.ny, 1)
        vtkarr = interface.convert_array(self.data, name=data_name)
        output.GetPointData().AddArray(vtkarr)
        return output


class SurferGridReader(ReaderBase):
    """Read 2D ASCII/Binary Surfer grid files. The IO code was adopted from
    `Seequent's steno3d_surfer`_

    .. _Seequent's steno3d_surfer: https://github.com/seequent/steno3d-surfer/blob/master/steno3d_surfer/parser.py

    Note:
        MIT License

        Copyright (c) 2018 Seequent

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        SOFTWARE.
    """
    __displayname__ = 'Surfer Grid Reader'
    __category__ = 'reader'
    extensions = 'grd GRD'
    description = 'PVGeo: Surfer Grid'
    def __init__(self, outputType='vtkImageData', **kwargs):
        ReaderBase.__init__(self, outputType=outputType, **kwargs)
        self.__grids = None
        self.__data_name = kwargs.get('data_name', 'Data')

    @staticmethod
    def _surfer7bin(filename):
        """See class notes.
        """
        with open(filename, 'rb') as f:
            if unpack('4s', f.read(4))[0] != b'DSRB':
                raise _helpers.PVGeoError(
                '''Invalid file identifier for Surfer 7 binary .grd
                    file. First 4 characters must be DSRB.'''
                )
            f.read(8)  #Size & Version

            section = unpack('4s', f.read(4))[0]
            if section != b'GRID':
                raise _helpers.PVGeoError(
                    '''Unsupported Surfer 7 file structure. GRID keyword
                    must follow immediately after header but {}
                    encountered.'''.format(section)
                )
            size = unpack('<i', f.read(4))[0]
            if size != 72:
                raise _helpers.PVGeoError(
                    '''Surfer 7 GRID section is unrecognized size. Expected
                    72 but encountered {}'''.format(size)
                )
            nrow = unpack('<i', f.read(4))[0]
            ncol = unpack('<i', f.read(4))[0]
            x0 = unpack('<d', f.read(8))[0]
            y0 = unpack('<d', f.read(8))[0]
            deltax = unpack('<d', f.read(8))[0]
            deltay = unpack('<d', f.read(8))[0]
            zmin = unpack('<d', f.read(8))[0]
            zmax = unpack('<d', f.read(8))[0]
            rot = unpack('<d', f.read(8))[0]
            if rot != 0:
                warnings.warn('Unsupported feature: Rotation != 0')
            blankval = unpack('<d', f.read(8))[0]

            section = unpack('4s', f.read(4))[0]
            if section != b'DATA':
                raise _helpers.PVGeoError(
                    '''Unsupported Surfer 7 file structure. DATA keyword
                    must follow immediately after GRID section but {}
                    encountered.'''.format(section)
                )
            datalen = unpack('<i', f.read(4))[0]
            if datalen != ncol*nrow*8:
                raise _helpers.PVGeoError(
                    '''Surfer 7 DATA size does not match expected size from
                    columns and rows. Expected {} but encountered
                    {}'''.format(ncol*nrow*8, datalen)
                )
            data = np.zeros(ncol*nrow)
            for i in range(ncol*nrow):
                data[i] = unpack('<d', f.read(8))[0]
            data = np.where(data >= blankval, np.nan, data)

            try:
                section = unpack('4s', f.read(4))[0]
                if section == b'FLTI':
                    warnings.warn('Unsupported feature: Fault Info')
                else:
                    warnings.warn('Unrecognized keyword: {}'.format(section))
                warnings.warn('Remainder of file ignored')
            except:
                pass

        grd = GridInfo(
            nx=ncol,
            ny=nrow,
            xll=x0,
            yll=y0,
            dx=deltax,
            dy=deltay,
            dmin=zmin,
            dmax=zmax,
            data=data
        )
        return grd

    @staticmethod
    def _surfer6bin(filename):
        """See class notes.
        """
        with open(filename, 'rb') as f:
            if unpack('4s', f.read(4))[0] != b'DSBB':
                raise _helpers.PVGeoError(
                    '''Invalid file identifier for Surfer 6 binary .grd
                    file. First 4 characters must be DSBB.'''
                )
            nx = unpack('<h', f.read(2))[0]
            ny = unpack('<h', f.read(2))[0]
            xlo = unpack('<d', f.read(8))[0]
            xhi = unpack('<d', f.read(8))[0]
            ylo = unpack('<d', f.read(8))[0]
            yhi = unpack('<d', f.read(8))[0]
            dmin = unpack('<d', f.read(8))[0]
            dmax = unpack('<d', f.read(8))[0]
            data = np.ones(nx * ny)
            for i in range(nx * ny):
                zdata = unpack('<f', f.read(4))[0]
                if zdata >= 1.701410009187828e+38:
                    data[i] = np.nan
                else:
                    data[i] = zdata

        grd = GridInfo(
            nx=nx,
            ny=ny,
            xll=xlo,
            yll=ylo,
            dx=(xhi-xlo)/(nx-1),
            dy=(yhi-ylo)/(ny-1),
            dmin=dmin,
            dmax=dmax,
            data=data
        )
        return grd

    @staticmethod
    def _surfer6ascii(filename):
        """See class notes.
        """
        with open(filename, 'r') as f:
            if f.readline().strip() != 'DSAA':
                raise _helpers.PVGeoError('''Invalid file identifier for Surfer 6 ASCII .grd file. First line must be DSAA''')
            [ncol, nrow] = [int(n) for n in f.readline().split()]
            [xmin, xmax] = [float(n) for n in f.readline().split()]
            [ymin, ymax] = [float(n) for n in f.readline().split()]
            [dmin, dmax] = [float(n) for n in f.readline().split()]
            # Read in the rest of the file as a 1D array
            data = np.fromiter((np.float(s) for line in f for s in line.split()), dtype=float)

        grd = GridInfo(
            nx=ncol,
            ny=nrow,
            xll=xmin,
            yll=ymin,
            dx=(xmax-xmin)/(ncol-1),
            dy=(ymax-ymin)/(nrow-1),
            dmin=dmin,
            dmax=dmax,
            data=data
        )
        return grd


    def _read_grids(self, idx=None):
        """This parses the first file to determine grid file type then reads
        all files set."""
        if idx is not None:
            filenames = [self.get_file_names(idx=idx)]
        else:
            filenames = self.get_file_names()
        contents = []
        f = open(filenames[0], 'rb')
        key = struct.unpack('4s', f.read(4))[0]
        f.close()
        if key == b'DSRB':
            reader = self._surfer7bin
        elif key == b'DSBB':
            reader = self._surfer6bin
        elif key == b'DSAA':
            reader = self._surfer6ascii
        else:
            raise _helpers.PVGeoError('''Invalid file identifier for Surfer .grd file.
            First 4 characters must be DSRB, DSBB, or DSAA. This file contains: %s''' % key)

        for f in filenames:
            try:
                contents.append(reader(f))
            except (IOError, OSError) as fe:
                raise _helpers.PVGeoError(str(fe))
        if idx is not None: return contents[0]
        return contents


    def _read_up_front(self):
        """Should not need to be overridden.
        """
        # Perform Read
        self.__grids = self._read_grids()
        self.need_to_read(flag=False)
        return 1


    ########################

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to get data for current timestep and populate the
        output data object.
        """
        # Get output:
        output = self.GetOutputData(outInfo, 0)
        if self.need_to_read():
            self._read_up_front()
        # Get requested time index
        i = _helpers.get_requested_time(self, outInfo)
        # Build the output
        grid = self.__grids[i]
        grid.toVTK(output=output, data_name=self.__data_name)
        return 1

    def RequestInformation(self, request, inInfo, outInfo):
        """Used by pipeline to set grid extents.
        """
        if self.need_to_read():
            self._read_up_front()
        # Call parent to handle time stuff
        ReaderBase.RequestInformation(self, request, inInfo, outInfo)
        # Now set whole output extent
        info = outInfo.GetInformationObject(0)
        grid = self.__grids[0] # Get first grid to set output extents
        # Set WHOLE_EXTENT: This is absolutely necessary
        ext = (0,grid.nx-1, 0,grid.ny-1, 0,1-1)
        info.Set(vtk.vtkStreamingDemandDrivenPipeline.WHOLE_EXTENT(), ext, 6)
        return 1

    def set_data_name(self, data_name):
        """Set the name of the data array"""
        if self.__data_name != data_name:
            self.__data_name = data_name
            self.Modified(read_again=False)

    def get_data_name(self):
        """Get the name of the data array"""
        return self.__data_name


################################################################################


class WriteImageDataToSurfer(WriterBase):
    """Write a 2D ``vtkImageData`` object to the Surfer grid format"""
    __displayname__ = 'Write ``vtkImageData`` to Surfer Format'
    __category__ = 'writer'
    def __init__(self):
        WriterBase.__init__(self, inputType='vtkImageData', ext='grd')
        self.__input_array = [None, None]


    def perform_write_out(self, input_data_object, filename, object_name):
        """Writes an input ``vtkImageData`` object to a file"""
        img = input_data_object

        # Check dims: make sure 2D
        # TODO: handle any orientation
        nx, ny, nz = img.GetDimensions()
        if nx == ny == 1 and nz != 1:
            raise RuntimeError('Only 2D data on the XY plane is supported at this time.')

        ox, oy, oz = img.GetOrigin()
        dx, dy, dz = img.GetSpacing()

        # Get data ranges
        xmin, xmax, ymin, ymax, zmin, zmax = img.GetBounds()

        # Note user has to select a single array to save out
        field, name = self.__input_array[0], self.__input_array[1]
        vtkarr = _helpers.get_vtk_array(img, field, name)
        arr = interface.convert_array(vtkarr)
        dmin, dmax = arr.min(), arr.max()

        # arr = arr.reshape((nx, ny), order='F')

        meta = 'DSAA\n%d %d\n%f %f\n%f %f\n%f %f' % (nx, ny, xmin, xmax,
                                                     ymin, ymax, dmin, dmax)
        # Now write out the data!
        np.savetxt(filename, arr, header=meta, comments='', fmt=self.get_format())


        return 1


    def SetInputArrayToProcess(self, idx, port, connection, field, name):
        """Used to the inpput array / the data value (z-value) to write for the
        Surfer format.

        Args:
            idx (int): the index of the array to process
            port (int): input port (use 0 if unsure)
            connection (int): the connection on the port (use 0 if unsure)
            field (int): the array field (0 for points, 1 for cells, 2 for
                field, and 6 for row)
            name (int): the name of the array
        """
        if self.__input_array[0] != field:
            self.__input_array[0] = field
            self.Modified()
        if self.__input_array[1] != name:
            self.__input_array[1] = name
            self.Modified()
        return 1

    def apply(self, input_data_object, array_name):
        """Run the algorithm on an input data object, specifying one data array
        to save out.
        """
        self.SetInputDataObject(input_data_object)
        arr, field = _helpers.search_for_array(input_data_object, array_name)
        self.SetInputArrayToProcess(0, 0, 0, field, array_name)
        self.Update()
        return interface.wrap_pyvista(self.GetOutput())

    def Write(self, input_data_object=None, array_name=None):
        """Perfrom the write out."""
        if input_data_object:
            self.SetInputDataObject(input_data_object)
            if array_name:
                arr, field = _helpers.search_for_array(input_data_object, array_name)
                self.SetInputArrayToProcess(0, 0, 0, field, array_name)
        self.Modified()
        self.Update()


    def write(self, input_data_object=None, array_name=None):
        """Perfrom the write out."""
        return self.Write(input_data_object=input_data_object, array_name=array_name)

###############################################################################


class EsriGridReader(DelimitedTextReader):
    """See details: https://en.wikipedia.org/wiki/Esri_grid
    """
    __displayname__ = 'Esri Grid Reader'
    __type__ = 'reader'
    description = 'PVGeo: Esri Grid'
    extensions = 'asc dem txt'
    def __init__(self, outputType='vtkImageData', **kwargs):
        DelimitedTextReader.__init__(self, outputType=outputType, **kwargs)
        # These are attributes the derived from file contents:
        self.set_delimiter(' ')
        self.__nx = None
        self.__ny = None
        self.__xo = None
        self.__yo = None
        self.__cellsize = None
        self.__data_name = kwargs.get('data_name', 'Data')
        self.NODATA_VALUE = -9999

    def _extract_header(self, content):
        """Internal helper to parse header information in ESRI Grid files"""
        try:
            self.__nx = int(content[0].split()[1])
            self.__ny = int(content[1].split()[1])
            self.__xo = float(content[2].split()[1])
            self.__yo = float(content[3].split()[1])
            self.__cellsize = float(content[4].split()[1])
            self.NODATA_VALUE = float(content[5].split()[1])
        except ValueError:
            raise _helpers.PVGeoError('This file is not in proper Esri ASCII Grid format.')
        return [self.__data_name], content[6::]

    def _file_contents_to_data_frame(self, contents):
        """Creates a dataframe with a sinlge array for the file data.
        """
        data = []
        for content in contents:
            arr = np.fromiter((float(s) for line in content for s in line.split()), dtype=float)
            df = pd.DataFrame(data=arr, columns=[self.get_data_name()])
            data.append(df)
        return data


    def _get_raw_data(self, idx=0):
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
        """Used by pipeline to get data for current timestep and populate the
        output data object.
        """
        # Get output:
        output = self.GetOutputData(outInfo, 0)

        if self.need_to_read():
            self._read_up_front()

        # Get requested time index
        i = _helpers.get_requested_time(self, outInfo)

        # Build the data object
        output.SetOrigin(self.__xo, self.__yo, 0.0)
        output.SetSpacing(self.__cellsize, self.__cellsize, self.__cellsize)
        output.SetDimensions(self.__nx, self.__ny, 1)

        # Now add data values as point data
        data = self._get_raw_data(idx=i).flatten(order='F')
        vtkarr = interface.convert_array(data, name=self.__data_name)
        output.GetPointData().AddArray(vtkarr)

        return 1

    def RequestInformation(self, request, inInfo, outInfo):
        """Used by pipeline to set grid extents.
        """
        if self.need_to_read():
            self._read_up_front()
        # Call parent to handle time stuff
        DelimitedTextReader.RequestInformation(self, request, inInfo, outInfo)
        # Now set whole output extent
        info = outInfo.GetInformationObject(0)
        # Set WHOLE_EXTENT: This is absolutely necessary
        ext = (0,self.__nx-1, 0,self.__ny-1, 0,1-1)
        info.Set(vtk.vtkStreamingDemandDrivenPipeline.WHOLE_EXTENT(), ext, 6)
        return 1

    def set_data_name(self, data_name):
        """Set the name of the data array"""
        if self.__data_name != data_name:
            self.__data_name = data_name
            self.Modified(read_again=False)

    def get_data_name(self):
        """Get the name of the data array"""
        return self.__data_name



################################################################################


class LandsatReader(ReaderBaseBase):
    """A reader that will handle ESPA XML files for Landsat Imagery. This reader
    uses the ``espatools`` package to read Landsat rasters (band sets) and
    creates vtkImageData with each band as point data
    """
    __displayname__ = 'Landsat XML Reader'
    __category__ = 'reader'
    extensions = "xml"
    description = 'PVGeo: Landsat ESPA XML Metadata'
    def __init__(self, **kwargs):
        ReaderBaseBase.__init__(self, outputType='vtkImageData', **kwargs)
        self.__reader = espatools.RasterSetReader(yflip=True)
        self.__raster = None
        self.__cast = True
        self.__scheme = 'infrared'
        # Properties:
        self._dataselection = vtk.vtkDataArraySelection()
        self._dataselection.AddObserver("ModifiedEvent", _helpers.create_modified_callback(self))


    def Modified(self, read_again=False):
        """Ensure default is overridden to be false so array selector can call.
        """
        return ReaderBaseBase.Modified(self, read_again=read_again)

    def modified(self, read_again=False):
        return self.Modified(read_again=read_again)


    def get_file_name(self):
        """Super class has file names as a list but we will only handle a single
        project file. This provides a conveinant way of making sure we only
        access that single file.
        A user could still access the list of file names using ``get_file_names()``.
        """
        return ReaderBaseBase.get_file_names(self, idx=0)


    #### Methods for performing the read ####

    def _get_file_contents(self, idx=None):
        """Reads XML meta data, no data read."""
        self.__reader.SetFileName(self.get_file_name())
        self.__raster = self.__reader.Read(meta_only=True)
        for n in self.__raster.bands.keys():
            self._dataselection.AddArray(n)
        self.need_to_read(flag=False) # Only meta data has been read
        return

    def _read_up_front(self):
        """Internal helper to read all data at start"""
        return self._get_file_contents()

    def _get_raw_data(self, idx=0):
        """Perfroms the read for the selected bands"""
        allowed = []
        for i in range(self._dataselection.GetNumberOfArrays()):
            name = self._dataselection.GetArrayName(i)
            if self._dataselection.ArrayIsEnabled(name):
                allowed.append(name)
        self.__raster = self.__reader.Read(meta_only=False, allowed=allowed, cast=self.__cast)
        return self.__raster

    def _build_image_data(self, output):
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
            self._read_up_front()
        self._get_raw_data()
        self._build_image_data(output)
        # Now add the data based on what the user has selected
        for name, band in self.__raster.bands.items():
            data = band.data
            output.GetPointData().AddArray(interface.convert_array(data.flatten(), name=name))
        if self.__scheme is not None:
            colors = self.__raster.GetRGB(scheme=self.__scheme).reshape((-1,3))
            output.GetPointData().SetScalars(interface.convert_array(colors, name=self.__scheme))
            output.GetPointData().SetActiveScalars(self.__scheme)
        return 1

    def RequestInformation(self, request, inInfo, outInfo):
        """Used by pipeline to set grid extents."""
        # Call parent to handle time stuff
        ReaderBaseBase.RequestInformation(self, request, inInfo, outInfo)
        if self.__raster is None:
            self._read_up_front()
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
        if self.need_to_read():
            try:
                self._read_up_front()
            except:
                pass
        return self._dataselection


    def set_cast_data_type(self, flag):
        """A flag to cast all data arrays as floats/doubles.
        This will fill invalid values with nans instead of a fill value"""
        if self.__cast != flag:
            self.__cast = flag
            self.Modified()


    def set_color_scheme(self, scheme):
        """Get an RGB scheme from the raster set. If no scheme is desired, pass
        any string that is not a defined scheme as the scheme argument."""
        if isinstance(scheme, int):
            scheme = self.get_color_scheme_names()[scheme]
        if scheme in list(espatools.RasterSet.RGB_SCHEMES.keys()) and self.__scheme != scheme:
            self.__scheme = scheme
            self.Modified()
        elif self.__scheme is not None:
            self.__scheme = None
            self.Modified()


    @staticmethod
    def get_color_scheme_names():
        """Get a list of the available color schemes"""
        schemes = list(espatools.RasterSet.RGB_SCHEMES.keys())
        schemes.insert(0, 'No Selection')
        return schemes


################################################################################


class WriteCellCenterData(WriterBase):
    """This writer will save a file of the XYZ points for an input dataset's
    cell centers and its cell data. Use in tandom with ParaView's native CSV
    writer which saves the PointData.
    """
    __displayname__ = 'Write Cell Centers To CSV'
    __category__ = 'writer'
    def __init__(self):
        WriterBase.__init__(self, inputType='vtkDataSet')
        self.__delimiter = ','


    def perform_write_out(self, input_data_object, filename, object_name):
        """Writes the cell centers of the input data object to a file"""
        # Find cell centers
        filt = vtk.vtkCellCenters()
        filt.SetInputDataObject(input_data_object)
        filt.Update()
        centers = dsa.WrapDataObject(filt.GetOutput(0)).Points
        # Get CellData
        wpdi = dsa.WrapDataObject(input_data_object)
        celldata = wpdi.CellData
        keys = celldata.keys()
        # Save out using numpy
        arr = np.zeros((len(centers), 3 + len(keys)))
        arr[:,0:3] = centers
        for i, name in enumerate(keys):
            arr[:,i+3] = celldata[name]
        # Now write out the data
        # Clean data titles to make sure they do not contain the delimiter
        repl = '_' if self.__delimiter != '_' else '-'
        for i, name in enumerate(keys):
            keys[i] = name.replace(self.__delimiter, repl)
        header = '! %s\n%s' % (object_name, ('%s' % self.__delimiter).join(['X', 'Y', 'Z'] + keys))
        np.savetxt(filename, arr,
                   header=header,
                   delimiter=self.__delimiter,
                   fmt=self.get_format(),
                   comments='')
        # Success for pipeline
        return 1

    def set_delimiter(self, deli):
        """The string delimiter to use"""
        if self.__delimiter != deli:
            self.__delimiter = deli
            self.Modified()


###############################################################################
