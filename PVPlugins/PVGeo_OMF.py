# This is module to import. It provides VTKPythonAlgorithmBase, the base class
# for all python-based vtkAlgorithm subclasses in VTK and decorators used to
# 'register' the algorithm with ParaView along with information about UI.
from paraview.util.vtkAlgorithm import *

import sys
sys.path.append('/Users/bane/anaconda3/envs/omf/lib/python2.7/site-packages/')
sys.path.append('/Users/bane/Documents/OpenGeoVis/Projects/omf/omf/')

# Helpers:
from PVGeo import _helpers
# Classes to Decorate
from PVGeo.omf import OMFReader





###############################################################################


OMF_EXTS = 'omf'
OMF_DESC = 'Open Mining Format Project'

@smproxy.reader(name="PVGeoOMFReader",
       label="PVGeo: Open Mining Format Project Reader",
       extensions=OMF_EXTS,
       file_description=OMF_DESC)
class PVGeoOMFReader(OMFReader):
    def __init__(self):
        OMFReader.__init__(self)

    #### Seters and Geters ####

    # TODO: check this to make sure not time varying
    @smproperty.xml(_helpers.getFileReaderXml(OMF_EXTS, readerDescription=OMF_DESC))
    def AddFileName(self, fname):
        OMFReader.AddFileName(self, fname)


    # Array selection API is typical with readers in VTK
    # This is intended to allow ability for users to choose which arrays to
    # load. To expose that in ParaView, simply use the
    # smproperty.dataarrayselection().
    # This method **must** return a `vtkDataArraySelection` instance.
    @smproperty.dataarrayselection(name="Project Data")
    def GetDataSelection(self):
        return OMFReader.GetDataSelection(self)


###############################################################################
