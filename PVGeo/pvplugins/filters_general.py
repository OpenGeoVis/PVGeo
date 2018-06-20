# __all__ = [
#
# ]

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
from PVGeo import _helpers

#### GLOBAL VARIABLES ####
MENUT_CAT = 'PVGeo: General Filters'


###############################################################################


# Add Cell Connectivity To Points
@smproxy.filter(name='vtkAddCellConnToPoints', label='Add Cell Connectivity To Points')
@smhint.xml('<ShowInMenu category="%s"/>' % MENUT_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkPolyData"], composite_data_supported=False)
class vtkAddCellConnToPoints(VTKPythonAlgorithmBase):
    def __init__(self):
        VTKPythonAlgorithmBase.__init__(self,
            nInputPorts=1, inputType='vtkPolyData',
            nOutputPorts=1, outputType='vtkPolyData')
        # Parameters
        self.__cellType = 4
        self.__usenbr = False


    def RequestData(self, request, inInfo, outInfo):
        from PVGeo.filters_general import connectCells
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        pdo = self.GetOutputData(outInfo, 0)
        # Perfrom task
        connectCells(pdi, cellType=self.__cellType, nrNbr=self.__usenbr, pdo=pdo, logTime=False)
        return 1


    #### Seters and Geters ####

    @smproperty.xml(_helpers.getDropDownXml(name='CellType', command='SetCellType', labels=['Poly Line', 'Line'],values=[4, 3]))
    def SetCellType(self, cellType):
        if cellType != self.__cellType:
            self.__cellType = cellType
            self.Modified()

    @smproperty.xml(_helpers.getPropertyXml('UseNearestNbr', 'Use Neareast Nbr Approx', 'UseNearestNbr', False, help='A boolean to control whether or not to use SciPy nearest neighbor approximation when build cell connectivity.'))
    def UseNearestNbr(self, flag):
        if flag != self.__usenbr:
            self.__usenbr = flag
            self.Modified()



###############################################################################


# Combine Tables
@smproxy.filter(name='vtkCombineTables', label='Combine Tables')
@smhint.xml('<ShowInMenu category="%s"/>' % MENUT_CAT)
@smproperty.input(name="Input1", port_index=1)
@smdomain.datatype(dataTypes=["vtkTable"], composite_data_supported=False)
@smproperty.input(name="Input2", port_index=0)
@smdomain.datatype(dataTypes=["vtkTable"], composite_data_supported=False)
class vtkCombineTables(VTKPythonAlgorithmBase):
    def __init__(self):
        VTKPythonAlgorithmBase.__init__(self,
            nInputPorts=2,
            nOutputPorts=1, outputType='vtkTable')
        # Parameters... none

    # CRITICAL for multiple input ports
    def FillInputPortInformation(self, port, info):
        # all are tables so no need to check port
        info.Set(self.INPUT_REQUIRED_DATA_TYPE(), "vtkTable")
        return 1


    def RequestData(self, request, inInfo, outInfo):
        # Inputs from different ports:
        pdi0 = self.GetInputData(inInfo, 0, 0)
        pdi1 = self.GetInputData(inInfo, 1, 0)
        pdo = self.GetOutputData(outInfo, 0)

        pdo.DeepCopy(pdi0)

        # Get number of columns
        ncols1 = pdi1.GetNumberOfColumns()
        # Get number of rows
        nrows = pdi0.GetNumberOfRows()
        nrows1 = pdi1.GetNumberOfRows()
        assert(nrows == nrows1)

        for i in range(pdi1.GetRowData().GetNumberOfArrays()):
            arr = pdi1.GetRowData().GetArray(i)
            pdo.GetRowData().AddArray(arr)
        return 1



###############################################################################
# TODO: how do we preserve input/output types?
# Correlate Arrays
# @smproxy.filter(name='vtkCorrelateArrays', label='Correlate Arrays')
# @smhint.xml('<ShowInMenu category="%s"/>' % MENUT_CAT)
# @smproperty.input(name="Input", port_index=0)
# @smdomain.datatype(dataTypes=["vtkDataObject"], composite_data_supported=False)
# class vtkCorrelateArrays(VTKPythonAlgorithmBase):
#     """Use `np.correlate()` on `mode=\'same\'` on two selected arrays from one input."""
#     def __init__(self):
#         VTKPythonAlgorithmBase.__init__(self,
#             nInputPorts=1, nOutputPorts=1, inputType='vtkDataObject', outputType='vtkDataObject')
#         # Parameters... none
#         self.__multiplier = 1.0
#         self.__newName = 'Correlated'
#
#     # # THIS IS CRUCIAL to preserve data type through filter
#     def RequestDataObject(self, request, inInfoVec, outInfoVec):
#         """Overwritten by subclass to manage data object creation.
#         There is not need to overwrite this class if the output can
#         be created based on the OutputType data member."""
#         #print(inInfoVec[0])
#         #typ = inInfoVec[0].Get(vtkDataObject.DATA_OBJECT()).Get(vtkDataObject.DATA_OBJECT())
#         #print(typ)
#         outInfoVec[0].Set(vtkDataObject.DATA_TYPE_NAME(), "vtkTable")
#         return 1
#
#     def RequestData(self, request, inInfo, outInfo):
#         from PVGeo.filters_general import correlateArrays
#         import PVGeo._helpers as inputhelp
#         # Get input/output of Proxy
#         pdi = self.GetInputData(inInfo, 0, 0)
#         pdo = self.GetOutputData(outInfo, 0)
#         # Grab input arrays to process from drop down menus
#         # Simply grab the name and field association
#         # TODO: use new array helpers
#         # name0 = inputhelp.getSelectedArrayName(self, 0)
#         # field0 = inputhelp.getSelectedArrayField(self, 0)
#         # name1 = inputhelp.getSelectedArrayName(self, 1)
#         # field1 = inputhelp.getSelectedArrayField(self, 1)
#         # # Pass array names and associations on to process
#         # correlateArrays(pdi, (name0,field0), (name1,field1), multiplier=self.__multiplier, newName=self.__newName, pdo=pdo)
#         print('does this work???')
#         print(pdi)
#         print(pdo)
#         pdo.DeepCopy(pdi)
#         return 1
#
#
#     # Array selection API is typical with filters in VTK
#     # This is intended to allow ability for users to choose which arrays to
#     # process. To expose that in ParaView, simply use the
#     # @smproperty.xml(_helpers.getInputArrayXml(nInputPorts=1, numArrays=2))
#     # def SetInputArrayToProcess(self, idx, info):
#     #     return vtkPVGeoFilterBase.SetInputArrayToProcess(idx, info)
#
#     #### SETTERS AND GETTERS ####
#
#     @smproperty.doublevector(name="Multiplier", default_values=1.0)
#     def SetMultiplier(self, val):
#         if self.__multiplier != val:
#             self.__multiplier = val
#             self.Modified()
#
#
#     def GetMultiplier(self):
#         return self.__multiplier
#
#
#     @smproperty.stringvector(name="NewArrayName", default="Correlated")
#     def SetNewArrayName(self, name):
#         if self.__newName != name:
#             self.__newName = name
#             self.Modified()
#
#
#     def GetNewArrayName(self):
#         return self.__newName





###############################################################################


###############################################################################




###############################################################################
