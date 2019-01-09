__all__ = [
    'OMFReader',
]

import numpy as np
import vtk

import omf
import omfvtk

from ..base import ReaderBaseBase
from .. import _helpers
from ..interface import pointsToPolyData



class OMFReader(ReaderBaseBase):
    """Handles reading an OMF Project
    """
    __displayname__ = 'OMF Project Reader'
    __category__ = 'reader'
    extensions = 'omf'
    description = 'PVGeo: Open Mining Format Project'
    def __init__(self):
        ReaderBaseBase.__init__(self,
            nOutputPorts=1, outputType='vtkMultiBlockDataSet')
        # Properties:
        self._dataselection = vtk.vtkDataArraySelection()
        self._dataselection.AddObserver("ModifiedEvent", _helpers.createModifiedCallback(self))
        self.__names = []
        self.__data = dict()
        self.__project = None

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

    def _ReadUpFront(self):
        # Read all elements
        reader = omf.OMFReader(self.GetFileName())
        self.__project = reader.get_project()
        self.__names = [e.name for e in self.__project.elements]
        for n in self.__names:
            self._dataselection.AddArray(n)
        self.NeedToRead(flag=False)
        return 1

    def _GetRawData(self):
        """Converts OMF data to VTK data objects."""
        # Now iterate over the elements and add converted data to the data dict:
        data = dict()
        for e in self.__project.elements:
            if self._dataselection.ArrayIsEnabled(e.name):
                if not e.name in self.__data:
                    self.__data[e.name] = omfvtk.wrap(e)
                data[e.name] = self.__data[e.name]
        return data

    #### pipeline methods ####

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to get data for current timestep and populate the output data object.
        """
        # Get output:
        #output = self.GetOutputData(outInfo, 0)
        output = vtk.vtkMultiBlockDataSet.GetData(outInfo, 0)
        # Perfrom the read
        if self.NeedToRead():
            self._ReadUpFront()
        data = self._GetRawData()
        # Set number of blocks based on user choice in the selction
        output.SetNumberOfBlocks(self._dataselection.GetNumberOfArraysEnabled())
        blk = 0
        # iterate over data set to produce output based on users selection
        keys = data.keys()
        for name in keys:
            output.SetBlock(blk, data[name])
            output.GetMetaData(blk).Set(vtk.vtkCompositeDataSet.NAME(), name)
            blk += 1
        return 1


    #### Getters / Setters ####


    def GetDataSelection(self):
        if self.NeedToRead():
            self._ReadUpFront()
        return self._dataselection
