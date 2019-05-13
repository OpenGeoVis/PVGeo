__all__ = [
    'DelimitedTextReader',
    'DelimitedPointsReaderBase',
    'XYZTextReader'
]

__displayname__ = 'Delimited File I/O'

import sys

import numpy as np
import pandas as pd

from .. import _helpers, interface
from ..base import ReaderBase

if sys.version_info < (3,):
    from StringIO import StringIO
else:
    from io import StringIO



class DelimitedTextReader(ReaderBase):
    """This reader will take in any delimited text file and make a ``vtkTable``
    from it. This is not much different than the default .txt or .csv reader in
    ParaView, however it gives us room to use our own extensions and a little
    more flexibility in the structure of the files we import.
    """
    __displayname__ = 'Delimited Text Reader'
    __category__ = 'reader'
    extensions = 'dat csv txt text ascii xyz tsv ntab'
    description = 'PVGeo: Delimited Text Files'
    def __init__(self, nOutputPorts=1, outputType='vtkTable', **kwargs):
        ReaderBase.__init__(self,
            nOutputPorts=nOutputPorts, outputType=outputType, **kwargs)

        # Parameters to control the file read:
        #- if these are set/changed, we must reperform the read
        self.__delimiter = kwargs.get('delimiter', ' ')
        self.__use_tab = kwargs.get('use_tab', False)
        self.__skipRows = kwargs.get('skiprows', 0)
        self.__comments = kwargs.get('comments', '!')
        self.__has_titles = kwargs.get('has_titles', True)
        # Data objects to hold the read data for access by the pipeline methods
        self._data = []
        self._titles = []

    def _get_delimiter(self):
        """For itenral use only!
        """
        if self.__use_tab:
            return None
        return self.__delimiter

    def get_split_on_white_space(self):
        """Returns the status of how the delimiter interprets whitespace"""
        return self.__use_tab

    #### Methods for performing the read ####

    def _get_file_contents(self, idx=None):
        """This grabs the lines of the input data file as a string array. This
        allows us to load the file contents, parse the header then use numpy or
        pandas to parse the data."""
        if idx is not None:
            filenames = [self.get_file_names(idx=idx)]
        else:
            filenames = self.get_file_names()
        contents = []
        for f in filenames:
            try:
                contents.append(np.genfromtxt(f, dtype=str, delimiter='\n', comments=self.__comments)[self.__skipRows::])
            except (IOError, OSError) as fe:
                raise _helpers.PVGeoError(str(fe))
        if idx is not None: return contents[0]
        return contents

    def _extract_header(self, content):
        """Override this. Removes header from single file's content.
        """
        if len(np.shape(content)) > 2:
            raise _helpers.PVGeoError("`_extract_header()` can only handle a sigle file's content")
        idx = 0
        if self.__has_titles:
            titles = content[idx].split(self._get_delimiter())
            idx += 1
        else:
            cols = len(content[idx].split(self._get_delimiter()))
            titles = []
            for i in range(cols):
                titles.append('Field %d' % i)
        return titles, content[idx::]

    def _extract_headers(self, contents):
        """Should NOT be overriden. This is a convienance methods to iteratively
        get all file contents. Your should override ``_extract_header``.
        """
        ts = []
        for i, c in enumerate(contents):
            titles, newcontent = self._extract_header(c)
            contents[i] = newcontent
            ts.append(titles)
        # Check that the titles are the same across files:
        ts = np.unique(np.asarray(ts), axis=0)
        if len(ts) > 1:
            raise _helpers.PVGeoError('Data array titles varied across file timesteps. This data is invalid as a timeseries.')
        return ts[0], contents


    def _file_contents_to_data_frame(self, contents):
        """Should NOT need to be overriden. After ``_extract_headers`` handles
        removing the file header from the file contents, this method will parse
        the remainder of the contents into a pandas DataFrame with column names
        generated from the titles resulting from in ``_extract_headers``.
        """
        data = []
        for content in contents:
            if self.get_split_on_white_space():
                df = pd.read_csv(StringIO("\n".join(content)), names=self.get_titles(), delim_whitespace=self.get_split_on_white_space())
            else:
                df = pd.read_csv(StringIO("\n".join(content)), names=self.get_titles(), sep=self._get_delimiter())
            data.append(df)
        return data

    def _read_up_front(self):
        """Should not need to be overridden.
        """
        # Perform Read
        contents = self._get_file_contents()
        self._titles, contents = self._extract_headers(contents)
        self._data = self._file_contents_to_data_frame(contents)
        self.need_to_read(flag=False)
        return 1

    #### Methods for accessing the data read in #####

    def _get_raw_data(self, idx=0):
        """This will return the proper data for the given timestep as a dataframe
        """
        return self._data[idx]


    #### Algorithm Methods ####

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to get data for current timestep and populate the
        output data object.
        """
        # Get output:
        output = self.GetOutputData(outInfo, 0)
        # Get requested time index
        i = _helpers.get_requested_time(self, outInfo)
        if self.need_to_read():
            self._read_up_front()
        # Generate the data object
        interface.data_frame_to_table(self._get_raw_data(idx=i), output)
        return 1


    #### Seters and Geters ####


    def set_delimiter(self, deli):
        """The input file's delimiter. To use a tab delimiter please use
        ``set_split_on_white_space()``

        Args:
            deli (str): a string delimiter/seperator
        """
        if deli != self.__delimiter:
            self.__delimiter = deli
            self.Modified()

    def set_split_on_white_space(self, flag):
        """Set a boolean flag to override the ``set_delimiter()`` and use any
        white space as a delimiter.
        """
        if flag != self.__use_tab:
            self.__use_tab = flag
            self.Modified()


    def set_skip_rows(self, skip):
        """Set the integer number of rows to skip at the top of the file.
        """
        if skip != self.__skipRows:
            self.__skipRows = skip
            self.Modified()

    def get_skip_rows(self):
        """Get the integer number of rows to skip at the top of the file.
        """
        return self.__skipRows

    def set_comments(self, identifier):
        """The character identifier for comments within the file.
        """
        if identifier != self.__comments:
            self.__comments = identifier
            self.Modified()

    def set_has_titles(self, flag):
        """Set the boolean for if the delimited file has header titles for the
        data arrays.
        """
        if self.__has_titles != flag:
            self.__has_titles = flag
            self.Modified()

    def has_titles(self):
        """Get the boolean for if the delimited file has header titles for the
        data arrays.
        """
        return self.__has_titles

    def get_titles(self):
        return self._titles


################################################################################


class DelimitedPointsReaderBase(DelimitedTextReader):
    """A base class for delimited text readers that produce ``vtkPolyData``
    points.
    """
    __displayname__ = 'Delimited Points Reader Base'
    __category__ = 'base'
    # extensions are inherrited from DelimitedTextReader
    description = 'PVGeo: Delimited Points' # Should be overriden
    def __init__(self, **kwargs):
        DelimitedTextReader.__init__(self, outputType='vtkPolyData', **kwargs)
        self.__copy_z = kwargs.get('copy_z', False)

    def set_copy_z(self, flag):
        """Set whether or not to copy the Z-component of the points to the
        Point Data"""
        if self.__copy_z != flag:
            self.__copy_z = flag
            self.Modified()

    def get_copy_z(self):
        """Get the status of whether or not to copy the Z-component of the
        points to the Point Data
        """
        return self.__copy_z

    #### Algorithm Methods ####

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to get data for current timestep and populate the
        output data object.
        """
        # Get output:
        output = self.GetOutputData(outInfo, 0)
        # Get requested time index
        i = _helpers.get_requested_time(self, outInfo)
        if self.need_to_read():
            self._read_up_front()
        # Generate the PolyData output
        data = self._get_raw_data(idx=i)
        output.DeepCopy(interface.points_to_poly_data(data, copy_z=self.get_copy_z()))
        return 1


################################################################################


class XYZTextReader(DelimitedTextReader):
    """A makeshift reader for XYZ files where titles have comma delimiter and
    data has space delimiter.
    """
    __displayname__ = 'XYZ Text Reader'
    __category__ = 'reader'
    # extensions are inherrited from DelimitedTextReader
    description = 'PVGeo: XYZ Delimited Text Files where header has comma delimiter.'
    def __init__(self, **kwargs):
        DelimitedTextReader.__init__(self, **kwargs)
        self.set_comments(kwargs.get('comments', '#'))

    # Simply override the extract titles functionality
    def _extract_header(self, content):
        """Internal helper to parse header details for XYZ files"""
        titles = content[0][2::].split(', ') # first two characers of header is '! '
        return titles, content[1::]
