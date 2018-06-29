# This is module to import. It provides VTKPythonAlgorithmBase, the base class
# for all python-based vtkAlgorithm subclasses in VTK and decorators used to
# 'register' the algorithm with ParaView along with information about UI.
from paraview.util.vtkAlgorithm import *
from vtk.numpy_interface import dataset_adapter as dsa
import numpy as np
import vtk

# Helpers:
from PVGeo import _helpers
# Classes to Decorate
from PVGeo.filters_general import * #AddCellConnToPoints, CombineTables
# from PVGeo.filters_general import PointsToTube, ReshapeTable, VoxelizePoints

#### GLOBAL VARIABLES ####
MENU_CAT = 'PVGeo: General Filters'


###############################################################################


# Add Cell Connectivity To Points
@smproxy.filter(name='PVGeoAddCellConnToPoints', label='Add Cell Connectivity To Points')
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkPolyData"], composite_data_supported=False)
class PVGeoAddCellConnToPoints(AddCellConnToPoints):
    def __init__(self):
        AddCellConnToPoints.__init__(self)

    #### Seters and Geters ####

    @smproperty.xml(_helpers.getDropDownXml(name='CellType', command='SetCellType',
        labels=['Poly Line', 'Line'],values=[4, 3]))
    def SetCellType(self, cellType):
        print(cellType)
        AddCellConnToPoints.SetCellType(self, cellType)

    @smproperty.xml(_helpers.getPropertyXml('SetUseNearestNbr', 'Use Neareast Nbr Approx',
        'SetUseNearestNbr', False,
        help='A boolean to control whether or not to use SciPy nearest neighbor approximation when build cell connectivity.'))
    def SetUseNearestNbr(self, flag):
        AddCellConnToPoints.SetUseNearestNbr(self, flag)



###############################################################################


# Combine Tables
@smproxy.filter(name='PVGeoCombineTables', label='Combine Tables')
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
@smproperty.input(name="Input1", port_index=1)
@smdomain.datatype(dataTypes=["vtkTable"], composite_data_supported=False)
@smproperty.input(name="Input2", port_index=0)
@smdomain.datatype(dataTypes=["vtkTable"], composite_data_supported=False)
class PVGeoCombineTables(CombineTables):
    def __init__(self):
        CombineTables.__init__(self)





###############################################################################

# PointsToTube
@smproxy.filter(name='PVGeoPointsToTube', label='Points To Tube')
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkPolyData"], composite_data_supported=False)
class PVGeoPointsToTube(PointsToTube):
    def __init__(self):
        PointsToTube.__init__(self)

    #### Seters and Geters ####

    # NOTE: Not givign the use the choice of cell type for this...
    # It is still accesible to change though...

    @smproperty.doublevector(name="Radius", default_values=10.0)
    def SetRadius(self, radius):
        PointsToTube.SetRadius(self, radius)

    @smproperty.intvector(name="Number of Sides", default_values=20)
    def SetNumberOfSides(self, num):
        PointsToTube.SetNumberOfSides(self, num)

    @smproperty.xml(_helpers.getPropertyXml('UseNearestNbr', 'Use Nearest Neighbor',
        'SetUseNearestNbr', False,
        help='A boolean to set whether to use a nearest neighbor approxiamtion when building path from input points.'))
    def SetUseNearestNbr(self, flag):
        PointsToTube.SetUseNearestNbr(self, flag)


###############################################################################


@smproxy.filter(name='PVGeoReshapeTable', label='Reshape Table')
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkTable"], composite_data_supported=False)
class PVGeoReshapeTable(ReshapeTable):
    def __init__(self):
        ReshapeTable.__init__(self)

    #### Seters and Geters ####

    @smproperty.stringvector(name="Names", default_values='Field 0')
    def SetNames(self, names):
        """Set names using a semicolon (;) seperated list"""
        # parse the names (a semicolon seperated list of names)
        ReshapeTable.SetNames(self, names)

    @smproperty.intvector(name="Number of Columns", default_values=6)
    def SetNumberOfColumns(self, ncols):
        ReshapeTable.SetNumberOfColumns(self, ncols)

    @smproperty.intvector(name="Number of Rows", default_values=126)
    def SetNumberOfRows(self, nrows):
        ReshapeTable.SetNumberOfRows(self, nrows)

    @smproperty.xml(_helpers.getDropDownXml(name='Order', command='SetOrder',
        labels=['Fortran-style: column-major order', 'C-style: Row-major order'],
        values=[0, 1]))
    def SetOrder(self, order):
        o = ['F', 'C']
        ReshapeTable.SetOrder(self, o[order])



###############################################################################


@smproxy.filter(name='PVGeoVoxelizePoints', label='Voxelize Points')
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkPolyData"], composite_data_supported=False)
class PVGeoVoxelizePoints(VoxelizePoints):
    def __init__(self):
        VoxelizePoints.__init__(self)

    #### Seters and Geters ####

    @smproperty.xml(_helpers.getPropertyXml('SetEstimateGrid', 'Estimate Grid Spacing',
        'SetEstimateGrid', True,
        help='A boolean to set whether to try to estimate the proper dx, dy, and dz spacings for a grid on a regular cartesian coordinate system.'))
    def SetEstimateGrid(self, flag):
        VoxelizePoints.SetEstimateGrid(self, flag)

    @smproperty.doublevector(name="dx", default_values=10.0)
    def SetDeltaX(self, dx):
        VoxelizePoints.SetDeltaX(self, dx)

    @smproperty.doublevector(name="dy", default_values=10.0)
    def SetDeltaY(self, dy):
        VoxelizePoints.SetDeltaY(self, dy)

    @smproperty.doublevector(name="dz", default_values=10.0)
    def SetDeltaZ(self, dz):
        VoxelizePoints.SetDeltaZ(self, dz)


###############################################################################


@smproxy.filter(name='PVGeoVoxelizePointsFromArrays', label='Voxelize Points from Arrays')
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkPolyData"], composite_data_supported=False)
class PVGeoVoxelizePointsFromArrays(VoxelizePoints):
    def __init__(self):
        VoxelizePoints.__init__(self)
        self.__dx_id = [None, None]
        self.__dy_id = [None, None]
        self.__dz_id = [None, None]
        self.SetEstimateGrid(False) # CRUCIAL

    def _CopyArrays(self, pdi, pdo):
        """Override to not pass spacing arrays to output"""
        exclude = [self.__dx_id[1], self.__dy_id[1], self.__dz_id[1]]
        for i in range(pdi.GetPointData().GetNumberOfArrays()):
            arr = pdi.GetPointData().GetArray(i)
            if arr.GetName() not in exclude:
                _helpers.addArray(pdo, 1, arr) # adds to CELL data
        return pdo

    def RequestData(self, request, inInfo, outInfo):
        # Handle input arrays
        pdi = self.GetInputData(inInfo, 0, 0)
        wpdi = dsa.WrapDataObject(pdi)
        dx = _helpers.getArray(wpdi, self.__dx_id[0], self.__dx_id[1])
        dy = _helpers.getArray(wpdi, self.__dy_id[0], self.__dy_id[1])
        dz = _helpers.getArray(wpdi, self.__dz_id[0], self.__dz_id[1])
        VoxelizePoints.SetDeltaX(self, dx)
        VoxelizePoints.SetDeltaY(self, dy)
        VoxelizePoints.SetDeltaZ(self, dz)
        # call parent and make sure EstimateGrid is set to False
        return VoxelizePoints.RequestData(self, request, inInfo, outInfo)

    #### Seters and Geters ####

    #(int idx, int port, int connection, int fieldAssociation, const char *name)
    @smproperty.xml(_helpers.getInputArrayXml(labels=['dx','dy','dz'], nInputPorts=1, numArrays=3))
    def SetInputArrayToProcess(self, idx, port, connection, field, name):
        if idx == 0:
            self.__dx_id = [field, name]
        elif idx == 1:
            self.__dy_id = [field, name]
        elif idx == 2:
            self.__dz_id = [field, name]
        else:
            raise RuntimeError('Bad input array inex.')
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

@smproxy.filter(name='PVGeoManySlicesAlongAxis', label='Many Slices Along Axis')
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkDataSet"], composite_data_supported=False)
class PVGeoManySlicesAlongAxis(ManySlicesAlongAxis):
    def __init__(self):
        ManySlicesAlongAxis.__init__(self)

    @smproperty.intvector(name="Number of Slices", default_values=5)
    @smdomain.intrange(min=2, max=100)
    def SetNumberOfSlices(self, num):
        ManySlicesAlongAxis.SetNumberOfSlices(self, num)

    @smproperty.xml(_helpers.getDropDownXml(name='Axis', command='SetAxis',
        labels=['X Axis', 'Y Axis', 'Z Axis'],
        values=[0, 1, 2]))
    def SetAxis(self, axis):
        ManySlicesAlongAxis.SetAxis(self, axis)



###############################################################################

@smproxy.filter(name='PVGeoClipThroughTime', label='Clip Through Time')
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkDataSet"], composite_data_supported=False)
class PVGeoClipThroughTime(ClipThroughTime):
    def __init__(self):
        ClipThroughTime.__init__(self)

    @smproperty.intvector(name="Number of Slices", default_values=10)
    @smdomain.intrange(min=2, max=1000)
    def SetNumberOfSlices(self, num):
        ClipThroughTime.SetNumberOfSlices(self, num)

    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def SetTimeDelta(self, dt):
        ClipThroughTime.SetTimeDelta(self, dt)

    @smproperty.xml(_helpers.getDropDownXml(name='Axis', command='SetAxis',
        labels=['X Axis', 'Y Axis', 'Z Axis'],
        values=[0, 1, 2]))
    def SetAxis(self, axis):
        ClipThroughTime.SetAxis(self, axis)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def GetTimestepValues(self):
        """This is critical for registering the timesteps"""
        return ClipThroughTime.GetTimestepValues(self)


###############################################################################


@smproxy.filter(name='PVGeoManySlicesAlongPoints', label='Many Slices Along Points')
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
@smproperty.input(name="Data Set", port_index=1)
@smdomain.datatype(dataTypes=["vtkDataSet"], composite_data_supported=False)
@smproperty.input(name="Points", port_index=0)
@smdomain.datatype(dataTypes=["vtkPolyData"], composite_data_supported=False)
class PVGeoManySlicesAlongPoints(ManySlicesAlongPoints):
    def __init__(self):
        ManySlicesAlongPoints.__init__(self)

    @smproperty.intvector(name="Number of Slices", default_values=10)
    @smdomain.intrange(min=2, max=1000)
    def SetNumberOfSlices(self, num):
        ManySlicesAlongPoints.SetNumberOfSlices(self, num)


###############################################################################
