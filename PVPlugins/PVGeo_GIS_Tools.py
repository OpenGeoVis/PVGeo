paraview_plugin_version = '1.1.12'
# This is module to import. It provides VTKPythonAlgorithmBase, the base class
# for all python-based vtkAlgorithm subclasses in VTK and decorators used to
# 'register' the algorithm with ParaView along with information about UI.
from paraview.util.vtkAlgorithm import *

# Helpers:
from PVGeo import _helpers
# Classes to Decorate
from PVGeo.gis import *


#### GLOBAL VARIABLES ####
MENU_CAT = 'PVGeo: GIS Tools'

###############################################################################

@smproxy.reader(name="PVGeoEsriGridReader",
       label="PVGeo: Esri ASCII Grid Reader",
       extensions="asc",
       file_description="Surfer Grid")
class PVGeoSurferGridReader(EsriGridReader):
    def __init__(self):
        EsriGridReader.__init__(self)

    #### Seters and Geters ####

    @smproperty.xml(_helpers.getFileReaderXml("sgems dat geoeas gslib GSLIB txt SGEMS", readerDescription='GSLib Table'))
    def AddFileName(self, fname):
        EsriGridReader.AddFileName(self, fname)

    @smproperty.stringvector(name='DataName', default_values='Data')
    def SetDataName(self, dataName):
        EsriGridReader.SetDataName(self, dataName)


###############################################################################
