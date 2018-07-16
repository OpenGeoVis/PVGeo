__all__ = [
    'OMFReader',
]

import sys
import numpy as np
import vtk
sys.path.append('/Users/bane/anaconda3/envs/omf/lib/python2.7/site-packages/')
sys.path.append('/Users/bane/Documents/OpenGeoVis/Projects/omf/omf/')
import omf

from ..base import ReaderBaseBase
from .. import _helpers
from ..filters_general import PointsToPolyData



class OMFReader(ReaderBaseBase):
    """Handles reading an OMF Project
    """
    __displayname__ = 'OMF Project Reader'
    __type__ = 'reader'
    def __init__(self):
        ReaderBaseBase.__init__(self,
            nOutputPorts=1, outputType='vtkMultiBlockDataSet')
        # Properties:
        self._dataselection = vtk.vtkDataArraySelection()
        self._dataselection.AddObserver("ModifiedEvent", _helpers.createModifiedCallback(self))
        self.__names = []
        self.__data = dict()

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
        project = reader.get_project()
        self.__names = [e.name for e in project.elements]
        for n in self.__names:
            self._dataselection.AddArray(n)

        # Now iterate over the elements and add converted data to the data dict:
        for e in project.elements:
            d = e.toVTK()
            self.__data[e.name] = d
        self.NeedToRead(flag=False)
        return 1

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

        # Set number of blocks based on user choice in the selction
        output.SetNumberOfBlocks(self._dataselection.GetNumberOfArraysEnabled())
        blk = 0
        # iterate over data set to produce output based on users selection
        for name in self.__names:
            if self._dataselection.ArrayIsEnabled(name):
                output.SetBlock(blk, self.__data[name])
                output.GetMetaData(blk).Set(vtk.vtkCompositeDataSet.NAME(), name)
                blk += 1
        return 1


    #### Getters / Setters ####


    def GetDataSelection(self):
        if self.NeedToRead():
            self._ReadUpFront()
        return self._dataselection
