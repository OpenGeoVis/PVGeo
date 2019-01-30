paraview_plugin_version = '1.1.6'
# This is module to import. It provides VTKPythonAlgorithmBase, the base class
# for all python-based vtkAlgorithm subclasses in VTK and decorators used to
# 'register' the algorithm with ParaView along with information about UI.
from paraview.util.vtkAlgorithm import *

# Helpers:
from PVGeo import _helpers, AlgorithmBase
# Classes to Decorate
from PVGeo.gmggroup import *


###############################################################################


@smproxy.reader(name="PVGeoOMFReader",
       label="PVGeo: Open Mining Format Project Reader",
       extensions=OMFReader.extensions,
       file_description=OMFReader.description)
class PVGeoOMFReader(OMFReader):
    def __init__(self):
        OMFReader.__init__(self)

    #### Seters and Geters ####

    # TODO: check this to make sure not time varying
    @smproperty.xml(_helpers.get_file_reader_xml(OMFReader.extensions, reader_description=OMFReader.description))
    def AddFileName(self, filename):
        OMFReader.AddFileName(self, filename)


    # Array selection API is typical with readers in VTK
    # This is intended to allow ability for users to choose which arrays to
    # load. To expose that in ParaView, simply use the
    # smproperty.dataarrayselection().
    # This method **must** return a `vtkDataArraySelection` instance.
    @smproperty.dataarrayselection(name="Project Data")
    def GetDataSelection(self):
        return OMFReader.GetDataSelection(self)


###############################################################################


# @smproxy.filter(name="PVGeoOMFExtractor", label="OMF Block Extractor")
# @smhint.xml('<ShowInMenu category="%s"/>' % 'PVGeo: OMF')
# @smproperty.input(name="MultiBlockInput", port_index=0)
# @smdomain.datatype(dataTypes=["vtkMultiBlockDataSet"], composite_data_supported=True)
# class PVGeoOMFExtractor(AlgorithmBase):
#     def __init__(self):
#         AlgorithmBase.__init__(self, nInputPorts=1, inputType='vtkMultiBlockDataSet',
#             nOutputPorts=1, outputType='vtkPolyData')
#         self.__block = 0
#
#
#     #### Pipeline Methods ####
#
#     # THIS IS CRUCIAL to preserve data type through filter
#     def RequestDataObject(self, request, inInfo, outInfo):
#         input = self.GetInputData(inInfo, 0, 0)
#         obj = input.GetBlock(self.__block)
#         self.OutputType = obj.GetClassName()
#         self.FillOutputPortInformation(0, outInfo.GetInformationObject(0))
#         outInfo.GetInformationObject(0).Set(vtk.vtkDataObject.DATA_OBJECT(), obj)
#         return 1
#
#
#     def RequestData(self, request, inInfo, outInfo):
#         # Now extract the multiblock data set
#         self.RequestDataObject(request, inInfo, outInfo)
#         input = self.GetInputData(inInfo, 0, 0)
#         output = self.GetOutputData(outInfo, 0)
#         obj = input.GetBlock(self.__block)
#         output.ShallowCopy(obj)
#         print(outInfo)
#         return 1
#
#     @smproperty.xml('''
#     <IntVectorProperty
#         command="SetBlock"
#         name="BlockIndices"
#         label="Block Indices"
#         animateable="1"
#         repeat_command="0" >
#         <CompositeTreeDomain
#             mode="all"
#             name="tree">
#             <RequiredProperties>
#                 <Property function="Input"
#                           name="MultiBlockInput" />
#             </RequiredProperties>
#         </CompositeTreeDomain>
#         <Documentation></Documentation>
#     </IntVectorProperty>''')
#     def SetBlock(self, block):
#         if self.__block != block:
#             self.__block = block
#             self.Modified()
