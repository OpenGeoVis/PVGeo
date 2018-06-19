__all__ = [
    'vtkPackedBinariesReader',
    'vtkDelimitedTextReader',
    'vtkXYZTextReader',
]

# Outside Modules
import numpy as np
import vtk
from vtk.util import numpy_support as nps
import warnings
# Get plugin generator imports
try:
    # This is module to import. It provides VTKPythonAlgorithmBase, the base class
    # for all python-based vtkAlgorithm subclasses in VTK and decorators used to
    # 'register' the algorithm with ParaView along with information about UI.
    from paraview.util.vtkAlgorithm import *
except ImportError:
    from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase
    from PVGeo._detail import *

# PVGeo Imports
import PVGeo
from PVGeo import vtkPVGeoReaderBase
from PVGeo import _helpers
from PVGeo.readers_general import packedBinaries, madagascar
from PVGeo.readers_general import delimitedText, xyzRead

@smproxy.reader(name="vtkPackedBinariesReader",
       label="PackedBinariesReader",
       extensions="bin H@ rsf",
       file_description="PackedBinariesReader")
class vtkPackedBinariesReader(vtkPVGeoReaderBase):
    def __init__(self):
        vtkPVGeoReaderBase.__init__(self,
            nOutputPorts=1, outputType='vtkTable')
        # Other Parameters
        self.__dataName = "Data"
        self.__endian = ''
        self.__dtype = 'f'
        self.__madagascar = False


    def RequestData(self, request, inInfo, outInfo):
        # Get output:
        output = vtk.vtkTable.GetData(outInfo)
        # Get requested time index
        i = self._get_update_time(outInfo.GetInformationObject(0))

        if self.__madagascar:
            madagascar(self.GetFileNames()[i], dataNm=self.GetDataName(), endian=self.GetEndian(), dtype=self.GetDType(), pdo=output)
        else:
            packedBinaries(self.GetFileNames()[i], dataNm=self.__dataName, endian=self.__endian, dtype=self.__dtype, pdo=output)

        return 1

    #### Seters and Geters ####
    @smproperty.xml(_helpers.getFileReaderXml("dat gslib sgems SGEMS", readerDescription='SGeMS Uniform Grid'))
    def AddFileName(self, fname):
        vtkPVGeoReaderBase.AddFileName(self, fname)

    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="adcanced")
    def SetTimeDelta(self, timeStep):
        vtkPVGeoReaderBase.SetTimeDelta(self, timeStep)

    @smproperty.xml(_helpers.getDropDownXml('Endian','SetEndian',
        ['Native', 'Little-Endian', 'Big-Endian'],
        help='This is the type memory endianness.'))
    def SetEndian(self, endian):
        pos = ['', '<', '>']
        if isinstance(endian, int):
            endian = pos[endian]
        if endian != self.__endian:
            self.__endian = endian
            self.Modified()

    def GetEndian(self):
        return self.__endian

    @smproperty.xml(_helpers.getDropDownXml('DataType','SetDType',
        ['Float64', 'Float32', 'Integer4'],
        help='This is data type to read.'))
    def SetDType(self, dtype):
        pos = ['d', 'f', 'i']
        if isinstance(dtype, int):
            dtype = pos[dtype]
        if dtype != self.__dtype:
            self.__dtype = dtype
            self.Modified()

    def GetDType(self):
        return self.__dtype

    @smproperty.stringvector(name='DataName', default_values='Data')
    def SetDataName(self, dataName):
        if dataName != self.__dataName:
            self.__dataName = dataName
            self.Modified()

    def GetDataName(self):
        return self.__dataName

    @smproperty.xml(_helpers.getPropertyXml('Madagascar', 'Madagascar SSRSF', 'SetMadagascar', False, help='A boolean to tell the reader to treat the file as a Madagascar SSRSF file.'))
    def SetMadagascar(self, flag):
        if flag != self.__madagascar:
            self.__madagascar = flag
            self.Modified()


#########


@smproxy.reader(name="vtkDelimitedTextReader",
       label="vtkDelimitedTextReader",
       extensions="",
       file_description="PackedBinariesReader")
class vtkDelimitedTextReader(vtkPVGeoReaderBase):
    def __init__(self):
        vtkPVGeoReaderBase.__init__(self,
            nOutputPorts=1, outputType='vtkTable')

        # Other Parameters:
        self.__delimiter = " "
        self.__useTab = False
        self.__skipRows = 0
        self.__comments = "#"
        self.__hasTitles = True


    def RequestData(self, request, inInfo, outInfo):
        # Get output:
        output = vtk.vtkTable.GetData(outInfo)
        # Get requested time index
        i = self._get_update_time(outInfo.GetInformationObject(0))
        # Read file and generate output
        delimitedText(self.GetFileNames()[i], deli=self.__delimiter,
            useTab=self.__useTab, hasTits=self.__hasTitles,
            skiprows=self.__skipRows, comments=self.__comments, pdo=output)
        return 1


    #### Seters and Geters ####
    @smproperty.xml(_helpers.getFileReaderXml("dat gslib sgems SGEMS", readerDescription='SGeMS Uniform Grid'))
    def AddFileName(self, fname):
        vtkPVGeoReaderBase.AddFileName(self, fname)

    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="adcanced")
    def SetTimeDelta(self, timeStep):
        vtkPVGeoReaderBase.SetTimeDelta(self, timeStep)

    @smproperty.stringvector(name="Delimiter", default_values=" ")
    def SetDelimiter(self, deli):
        if deli != self.__delimiter:
            self.__delimiter = deli
            self.Modified()

    @smproperty.xml(_helpers.getPropertyXml('UseTab', 'Use Tab Delimiter', 'SetUseTab', False, help='A boolean to override the Delimiter_Field and use a Tab delimiter.'))
    def SetUseTab(self, flag):
        if flag != self.__useTab:
            self.__useTab = flag
            self.Modified()

    @smproperty.intvector(name="SkipRows", default_values=0)
    def SetSkipRows(self, skip):
        if skip != self.__skipRows:
            self.__skipRows = skip
            self.Modified()

    @smproperty.stringvector(name="Comments", default_values="#")
    def SetComments(self, identifier):
        if identifier != self.__comments:
            self.__comments = identifier
            self.Modified()


###

class vtkXYZTextReader(vtkPVGeoReaderBase):
    def __init__(self):
        vtkPVGeoReaderBase.__init__(self,
            nOutputPorts=1, outputType='vtkTable')

        # Other Parameters:
        self.__delimiter = " "
        self.__useTab = False
        self.__skipRows = 0
        self.__comments = "#"

    def RequestData(self, request, inInfo, outInfo):
        # Get output:
        output = vtk.vtkTable.GetData(outInfo)
        # Get requested time index
        i = self._get_update_time(outInfo.GetInformationObject(0))
        # Read file and generate output
        xyzRead(self.GetFileNames(i), deli=self.__delimiter,
            useTab=self.__useTab, skiprows=self.__skipRows,
            comments=self.__comments, pdo=output)

    #### Seters and Geters ####
    @smproperty.xml(_helpers.getFileReaderXml("dat gslib sgems SGEMS", readerDescription='SGeMS Uniform Grid'))
    def AddFileName(self, fname):
        vtkPVGeoReaderBase.AddFileName(self, fname)

    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="adcanced")
    def SetTimeDelta(self, timeStep):
        vtkPVGeoReaderBase.SetTimeDelta(self, timeStep)
