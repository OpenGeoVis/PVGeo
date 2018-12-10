__all__ = [
    'TopoReader',
    'GravObsReader',
    'GravGradReader',
    'MagObsReader',
    'GeologyMapper',
]

__displayname__ = 'General Tools'

import numpy as np
import pandas as pd
import vtk
from vtk.numpy_interface import dataset_adapter as dsa

from .. import _helpers, interface
from ..base import FilterPreserveTypeBase
from ..readers import DelimitedPointsReaderBase

################################################################################


class TopoReader(DelimitedPointsReaderBase):
    """A reader to handle .topo files in UBC format to create a topography
    surface.
    """
    __displayname__ = 'GIF Topo Reader'
    __category__ = 'reader'
    extensions = 'topo txt dat'
    description = 'PVGeo: UBC 3D Topo Files'
    def __init__(self, copy_z=True, **kwargs):
        DelimitedPointsReaderBase.__init__(self, copy_z=copy_z, **kwargs)
        self.SetHasTitles(False)#kwargs.get('hasTitles', False))
        self.SetSplitOnWhiteSpace(True)
        self.__3d = True # TODO: handle 2D topo files as well
        self.__npts = None

    # Simply override the extract titles functionality
    def _ExtractHeader(self, content):
        # No titles
        # Get number of points
        self.__npts = int(content[0].strip())
        if len(content[1].split(self._GetDeli())) != 3:
            raise _helpers.PVGeoError('Data improperly formatted')
        return ['X', 'Y', 'Z'], content[1::]



################################################################################


class GravObsReader(DelimitedPointsReaderBase):
    """Read `GIF Gravity Observations`_ file.

    .. _GIF Gravity Observations: https://giftoolscookbook.readthedocs.io/en/latest/content/fileFormats/gravfile.html
    """
    __displayname__ = 'UBC Gravity Observations'
    __category__ = 'reader'
    extensions = 'grv txt dat'
    description = 'PVGeo: GIF Gravity Observations'
    def __init__(self, **kwargs):
        DelimitedPointsReaderBase.__init__(self, **kwargs)
        self.SetHasTitles(False)
        self.SetSplitOnWhiteSpace(True)
        self.__npts = None

    # Simply override the extract titles functionality
    def _ExtractHeader(self, content):
        # No titles
        # Get number of points
        self.__npts = int(content[0].strip())
        # Now decide if it is single or multi component
        if len(content[1].split(self._GetDeli())) != 5:
            raise _helpers.PVGeoError('Data improperly formatted')
        return ['X', 'Y', 'Z', 'Grav', 'Err'], content[1::]


################################################################################


class GravGradReader(DelimitedPointsReaderBase):
    """Read `GIF Gravity Gradiometry Observations`_ file.

    .. _GIF Gravity Gradiometry Observations: https://giftoolscookbook.readthedocs.io/en/latest/content/fileFormats/ggfile.html
    """
    __displayname__ = 'GIF Gravity Gradiometry Observations'
    __category__ = 'reader'
    extensions = 'grv gg txt dat'
    description = 'PVGeo: GIF Gravity Gradiometry Observations'
    def __init__(self, **kwargs):
        DelimitedPointsReaderBase.__init__(self, **kwargs)
        self.SetHasTitles(False)
        self.SetSplitOnWhiteSpace(True)
        self.__npts = None

    # Simply override the extract titles functionality
    def _ExtractHeader(self, content):
        # Get components
        comps = content[0].split('=')[1].split(',')
        # Get number of points
        self.__npts = int(content[1].strip())
        titles = ['X', 'Y', 'Z']
        for c in comps:
            titles.append(c)
        # Now decipher if it has stddevs
        num = len(content[2].split(self._GetDeli()))
        if num != len(titles):
            if num != (len(titles) + len(comps)):
                raise _helpers.PVGeoError('Data improperly formatted')
            for c in comps:
                titles.append('Stn_%s' % c )
        return titles, content[2::]


################################################################################


class MagObsReader(DelimitedPointsReaderBase):
    """Read `GIF Magnetic Observations`_ file.

    .. _GIF Magnetic Observations: https://giftoolscookbook.readthedocs.io/en/latest/content/fileFormats/magfile.html
    """
    __displayname__ = 'UBC Magnetic Observations'
    __category__ = 'reader'
    extensions = 'mag loc txt dat pre'
    description = 'PVGeo: GIF Magnetic Observations'
    def __init__(self, **kwargs):
        DelimitedPointsReaderBase.__init__(self, **kwargs)
        self.SetHasTitles(False)
        self.SetSplitOnWhiteSpace(True)
        self.__npts = None
        self.__incl = None
        self.__decl = None
        self.__geomag = None
        self.__ainc = None
        self.__adec = None
        self.__dir = None


    # Simply override the extract titles functionality
    def _ExtractHeader(self, content):
        # No titles
        self.__incl, self.__decl, self.__geomag = (float(val) for val in content[0].split(self._GetDeli()))
        self.__ainc, self.__adec, self.__dir = (float(val) for val in content[1].split(self._GetDeli()))
        # Get number of points
        self.__npts = int(content[2].strip())
        # Now decide if it is single or multi component
        row = content[3].split(self._GetDeli())
        num = len(row)
        if num == 3: # just locations
            self.SetCopyZ(True)
            return ['X', 'Y', 'Z'], content[3::]
        elif num == 4: # single component
            return ['X', 'Y', 'Z', 'Mag'], content[3::]
        elif num == 5: # single component
            return ['X', 'Y', 'Z', 'Mag', 'Err'], content[3::]
        elif num == 7: # multi component
            return ['X', 'Y', 'Z', 'ainc_1', 'ainc_2', 'Mag', 'Err'], content[3::]
        else:
            raise _helpers.PVGeoError('Data improperly formatted.')

    @staticmethod
    def ConvertVector(incl, decl, mag=1):
        x = mag * np.cos(np.deg2rad(incl)) * np.cos(np.deg2rad(decl))
        y = mag * np.cos(np.deg2rad(incl)) * np.sin(np.deg2rad(decl))
        z = mag * np.sin(np.deg2rad(incl))
        return (x, y, z)

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to get data for current timestep and populate the
        output data object.
        """
        # Set points using parent
        DelimitedPointsReaderBase.RequestData(self, request, inInfo, outInfo)
        # Add field data to ouptput
        output = self.GetOutputData(outInfo, 0)

        # Add inducing magnetic field
        x, y, z = self.ConvertVector(self.__incl, self.__decl, mag=self.__geomag)
        ind = vtk.vtkDoubleArray()
        ind.SetName('Inducing Magnetic Field')
        ind.SetNumberOfComponents(3)
        ind.InsertNextTuple3(x, y, z)
        output.GetFieldData().AddArray(ind)

        # Add Inclination and declination of the anomaly projection
        x, y, z = self.ConvertVector(self.__ainc, self.__adec)
        anom = vtk.vtkDoubleArray()
        anom.SetName('Anomaly Projection')
        anom.SetNumberOfComponents(3)
        anom.InsertNextTuple3(x, y, z)
        output.GetFieldData().AddArray(anom)

        return 1



################################################################################



class GeologyMapper(FilterPreserveTypeBase):
    """A filter to load a GIF geology definity file and map its values to a given
    data array in an input data object.
    """
    __displayname__ = 'UBC Geology Mapper'
    __category__ = 'filter'
    description = 'PVGeo: UBC Geology Mapper'
    def __init__(self, filename=None, delimiter=',', **kwargs):
        FilterPreserveTypeBase.__init__(self, **kwargs)
        self.__filename = filename
        self.__deli = delimiter
        self.__inputArray = [None, None]

    @staticmethod
    def _ReadDefinitions(filename, delimiter):
        """Reades the geology definition file as a pandas DataFrame"""
        return pd.read_csv(filename, sep=delimiter)

    @staticmethod
    def _MapValues(geol, arr):
        """Map the values defined by ``geol`` dataframe to the values in ``arr``.
        The first column (name should be ``Index``) will be used for the mapping.
        """
        # TODO: check that geol table contains all indexs found in arr
        # Return the mapped table
        geol.set_index(geol.keys()[0])
        return geol[geol.keys()[1::]].iloc[arr]

    def RequestData(self, request, inInfo, outInfo):
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        pdo = self.GetOutputData(outInfo, 0)
        # Get input array
        field, name = self.__inputArray[0], self.__inputArray[1]
        #self.__range = NormalizeArray.GetArrayRange(pdi, field, name)
        wpdi = dsa.WrapDataObject(pdi)
        arr = _helpers.getNumPyArray(wpdi, field, name)

        #### Perfrom task ####
        geol = self._ReadDefinitions(self.__filename, self.__deli)
        data = self._MapValues(geol, arr)

        pdo.DeepCopy(pdi)
        interface.addArraysFromDataFrame(pdo, field, data)

        return 1


    #### Seters and Geters ####


    def SetInputArrayToProcess(self, idx, port, connection, field, name):
        """Used to set the input array(s)

        Args:
            idx (int): the index of the array to process
            port (int): input port (use 0 if unsure)
            connection (int): the connection on the port (use 0 if unsure)
            field (int): the array field (0 for points, 1 for cells, 2 for
                field, and 6 for row)
            name (int): the name of the array
        """
        if self.__inputArray[0] != field:
            self.__inputArray[0] = field
            self.Modified()
        if self.__inputArray[1] != name:
            self.__inputArray[1] = name
            self.Modified()
        return 1


    def SetFileName(self, filename):
        if self.__filename != filename:
            self.__filename = filename
            self.Modified()

    def SetDelimiter(self, deli):
        if self.__deli != deli:
            self.__deli = deli
            self.Modified()
