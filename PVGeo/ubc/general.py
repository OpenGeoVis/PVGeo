__all__ = [
    'TopoReader',
    'GravObsReader',
    'MagObsReader',
]

import numpy as np
import vtk

# Import Helpers:
from ..readers import DelimitedPointsReaderBase
from .. import _helpers


################################################################################


class TopoReader(DelimitedPointsReaderBase):
    """A reader to handle .topo files in UBC format to create a topography surface
    """
    __displayname__ = 'UBC Topo Reader'
    __category__ = 'reader'
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
    """Read _`GIF Gravity Observations` file.

    .. _GIF Gravity Observations: https://giftoolscookbook.readthedocs.io/en/latest/content/fileFormats/gravfile.html
    """
    __displayname__ = 'UBC Gravity Observations'
    __category__ = 'reader'
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


class MagObsReader(DelimitedPointsReaderBase):
    """Read _`GIF Magnetic Observations` file.

    .. _GIF Magnetic Observations: https://giftoolscookbook.readthedocs.io/en/latest/content/fileFormats/magfile.html
    """
    __displayname__ = 'UBC Magnetic Observations'
    __category__ = 'reader'
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
        """Used by pipeline to get data for current timestep and populate the output data object.
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
