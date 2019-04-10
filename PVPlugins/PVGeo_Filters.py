paraview_plugin_version = '1.2.3'
# This is module to import. It provides VTKPythonAlgorithmBase, the base class
# for all python-based vtkAlgorithm subclasses in VTK and decorators used to
# 'register' the algorithm with ParaView along with information about UI.
from paraview.util.vtkAlgorithm import *
from vtk.numpy_interface import dataset_adapter as dsa

# Helpers:
from PVGeo import _helpers
# Classes to Decorate
from PVGeo.filters import *

#### GLOBAL VARIABLES ####
MENU_CAT = 'PVGeo: General Filters'


###############################################################################


# Add Cell Connectivity To Points
@smproxy.filter(name='PVGeoAddCellConnToPoints', label=AddCellConnToPoints.__displayname__)
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkPolyData"], composite_data_supported=True)
class PVGeoAddCellConnToPoints(AddCellConnToPoints):
    def __init__(self):
        AddCellConnToPoints.__init__(self)

    #### Seters and Geters ####

    @smproperty.xml(_helpers.getDropDownXml(name='CellType', command='SetCellType',
        labels=['Line', 'Poly Line'], values=[3, 4]))
    def SetCellType(self, cellType):
        AddCellConnToPoints.SetCellType(self, cellType)

    @smproperty.xml(_helpers.getPropertyXml(name='Use Neareast Nbr Approx',
        command='SetUseNearestNbr', default_values=False,
        help='A boolean to control whether or not to use SciPy nearest neighbor approximation when build cell connectivity.'))
    def SetUseNearestNbr(self, flag):
        AddCellConnToPoints.SetUseNearestNbr(self, flag)

    @smproperty.xml(_helpers.getPropertyXml(name='Use Unique Points',
        command='SetUseUniquePoints', default_values=False,
        help='Set a flag on whether to only use unique points'))
    def SetUseUniquePoints(self, flag):
        AddCellConnToPoints.SetUseUniquePoints(self, flag)



###############################################################################


# Combine Tables
@smproxy.filter(name='PVGeoCombineTables', label=CombineTables.__displayname__)
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
@smproperty.input(name="Input1", port_index=1)
@smdomain.datatype(dataTypes=["vtkTable"], composite_data_supported=False)
@smproperty.input(name="Input2", port_index=0)
@smdomain.datatype(dataTypes=["vtkTable"], composite_data_supported=False)
class PVGeoCombineTables(CombineTables):
    def __init__(self):
        CombineTables.__init__(self)


###############################################################################


# Split Table on Array
@smproxy.filter(name='PVGeoSplitTableOnArray', label=SplitTableOnArray.__displayname__)
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkTable"], composite_data_supported=False)
class PVGeoSplitTableOnArray(SplitTableOnArray):
    def __init__(self):
        SplitTableOnArray.__init__(self)

    @smproperty.xml(_helpers.getInputArrayXml(nInputPorts=1, numArrays=1))
    def SetInputArrayToProcess(self, idx, port, connection, field, name):
        return SplitTableOnArray.SetInputArrayToProcess(self, idx, port, connection, field, name)





###############################################################################

# PointsToTube
@smproxy.filter(name='PVGeoPointsToTube', label=PointsToTube.__displayname__)
@smhint.xml('''<ShowInMenu category="%s"/>
   <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkPolyData"], composite_data_supported=True)
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

    @smproperty.xml(_helpers.getPropertyXml(name='Use Nearest Neighbor',
        command='SetUseNearestNbr', default_values=False,
        help='A boolean to set whether to use a nearest neighbor approxiamtion when building path from input points.'))
    def SetUseNearestNbr(self, flag):
        PointsToTube.SetUseNearestNbr(self, flag)

    @smproperty.xml(_helpers.getPropertyXml(name='Capping',
        command='SetCapping', default_values=False,
        help='A boolean to set whether to cap the ends of the tube.'))
    def SetCapping(self, flag):
        PointsToTube.SetCapping(self, flag)

    @smproperty.xml(_helpers.getDropDownXml(name='CellType', command='SetCellType',
        labels=['Line', 'Poly Line'], values=[3, 4]))
    def SetCellType(self, cellType):
        PointsToTube.SetCellType(self, cellType)

    @smproperty.xml(_helpers.getPropertyXml(name='Use Unique Points',
        command='SetUseUniquePoints', default_values=False,
        help='Set a flag on whether to only use unique points'))
    def SetUseUniquePoints(self, flag):
        PointsToTube.SetUseUniquePoints(self, flag)



###############################################################################


@smproxy.filter(name='PVGeoReshapeTable', label=ReshapeTable.__displayname__)
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkTable"], composite_data_supported=True)
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
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />
    <WarnOnCreate title="Axial Assumptions">
      **Voxelize Points** filter assumes the input points to be sampled on a regular XYZ coordinate system at an even spacing.
      Do you want to continue?
        </WarnOnCreate>''' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkPolyData"], composite_data_supported=False)
class PVGeoVoxelizePoints(VoxelizePoints):
    def __init__(self):
        VoxelizePoints.__init__(self)

    #### Seters and Geters ####

    @smproperty.xml(_helpers.getPropertyXml(name='Estimate Grid Spacing',
        command='SetEstimateGrid', default_values=True,
        help='A boolean to set whether to try to estimate the proper dx, dy, and dz spacings for a grid on a regular cartesian coordinate system.', panel_visibility='advanced'))
    def SetEstimateGrid(self, flag):
        VoxelizePoints.SetEstimateGrid(self, flag)

    @smproperty.xml(_helpers.getPropertyXml(name='Cell Size', command='SetCellSize', default_values=[10.0, 10.0, 10.0], help='The cell size (dx, dy, dz) to use as a default for all generated voxels.', panel_visibility='advanced'))
    def SetCellSize(self, dx, dy, dz):
        VoxelizePoints.SetDeltas(self, dx, dy, dz)


###############################################################################


@smproxy.filter(name='PVGeoVoxelizePointsFromArrays', label='Voxelize Points From Arrays')
@smhint.xml('''<ShowInMenu category="%s"/>
    RepresentationType view="RenderView" type="Surface" />
    <WarnOnCreate title="Axial Assumptions">
      **Voxelize Points From Arrays** filter assumes the input points to be sampled on a regular XYZ coordinate system.
      Do you want to continue?
    </WarnOnCreate>''' % MENU_CAT)
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

    def RequestData(self, request, inInfoVec, outInfoVec):
        # Handle input arrays
        pdi = self.GetInputData(inInfoVec, 0, 0)
        wpdi = dsa.WrapDataObject(pdi)
        dx = _helpers.getNumPyArray(wpdi, self.__dx_id[0], self.__dx_id[1])
        dy = _helpers.getNumPyArray(wpdi, self.__dy_id[0], self.__dy_id[1])
        dz = _helpers.getNumPyArray(wpdi, self.__dz_id[0], self.__dz_id[1])
        VoxelizePoints.SetDeltas(self, dx, dy, dz)
        # call parent and make sure EstimateGrid is set to False
        return VoxelizePoints.RequestData(self, request, inInfoVec, outInfoVec)

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
            raise RuntimeError('Bad input array index.')
        return 1


###############################################################################

# Normalize Arrays
@smproxy.filter(name='PVGeoNormalizeArray', label=NormalizeArray.__displayname__)
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkDataObject"], composite_data_supported=False)
class PVGeoNormalizeArray(NormalizeArray):
    def __init__(self):
        NormalizeArray.__init__(self)

    #### SETTERS AND GETTERS ####

    @smproperty.xml(_helpers.getInputArrayXml(nInputPorts=1, numArrays=1))
    def SetInputArrayToProcess(self, idx, port, connection, field, name):
        return NormalizeArray.SetInputArrayToProcess(self, idx, port, connection, field, name)

    @smproperty.doublevector(name="Multiplier", default_values=1.0)
    def SetMultiplier(self, val):
        NormalizeArray.SetMultiplier(self, val)

    @smproperty.stringvector(name="New Array Name", default_values="Normalized")
    def SetNewArrayName(self, name):
        NormalizeArray.SetNewArrayName(self, name)

    @smproperty.xml(_helpers.getDropDownXml(name='Normalization', command='SetNormalization', labels=NormalizeArray.GetNormalizationNames(), help='This is the type of normalization to apply to the input array.'))
    def SetNormalization(self, norm):
        NormalizeArray.SetNormalization(self, norm)

    @smproperty.xml(_helpers.getPropertyXml(name='Absolute Value', command='SetTakeAbsoluteValue', default_values=False, help='This will take the absolute value of the array before normalization.'))
    def SetTakeAbsoluteValue(self, flag):
        NormalizeArray.SetTakeAbsoluteValue(self, flag)

    @smproperty.doublevector(name="Shifter", default_values=0.0)
    def SetShift(self, sft):
        NormalizeArray.SetShift(self, sft)


###############################################################################

# Array Math
@smproxy.filter(name='PVGeoArrayMath', label=ArrayMath.__displayname__)
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkDataObject"], composite_data_supported=False)
class PVGeoArrayMath(ArrayMath):
    def __init__(self):
        ArrayMath.__init__(self)

    #### SETTERS AND GETTERS ####

    @smproperty.xml(_helpers.getInputArrayXml(nInputPorts=1, numArrays=2))
    def SetInputArrayToProcess(self, idx, port, connection, field, name):
        return ArrayMath.SetInputArrayToProcess(self, idx, port, connection, field, name)

    @smproperty.doublevector(name="Multiplier", default_values=1.0)
    def SetMultiplier(self, val):
        ArrayMath.SetMultiplier(self, val)

    @smproperty.stringvector(name="New Array Name", default_values="Mathed Up")
    def SetNewArrayName(self, name):
        ArrayMath.SetNewArrayName(self, name)

    @smproperty.xml(_helpers.getDropDownXml(name='Operation', command='SetOperation', labels=ArrayMath.GetOperationNames(), help='This is the type of operation to apply to the input arrays.'))
    def SetOperation(self, op):
        ArrayMath.SetOperation(self, op)


###############################################################################

@smproxy.filter(name='PVGeoManySlicesAlongAxis', label=ManySlicesAlongAxis.__displayname__)
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkDataSet"], composite_data_supported=False)
class PVGeoManySlicesAlongAxis(ManySlicesAlongAxis):
    def __init__(self):
        ManySlicesAlongAxis.__init__(self)

    @smproperty.intvector(name="Number of Slices", default_values=5)
    @smdomain.intrange(min=2, max=25)
    def SetNumberOfSlices(self, num):
        ManySlicesAlongAxis.SetNumberOfSlices(self, num)

    @smproperty.xml(_helpers.getDropDownXml(name='Axis', command='SetAxis',
        labels=['X Axis', 'Y Axis', 'Z Axis'],
        values=[0, 1, 2]))
    def SetAxis(self, axis):
        ManySlicesAlongAxis.SetAxis(self, axis)



###############################################################################

@smproxy.filter(name='PVGeoSliceThroughTime', label=SliceThroughTime.__displayname__)
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkDataSet"], composite_data_supported=False)
class PVGeoSliceThroughTime(SliceThroughTime):
    def __init__(self):
        SliceThroughTime.__init__(self)

    @smproperty.intvector(name="Number of Slices", default_values=10)
    @smdomain.intrange(min=2, max=50)
    def SetNumberOfSlices(self, num):
        SliceThroughTime.SetNumberOfSlices(self, num)

    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def SetTimeDelta(self, dt):
        SliceThroughTime.SetTimeDelta(self, dt)

    @smproperty.xml(_helpers.getDropDownXml(name='Axis', command='SetAxis',
        labels=['X Axis', 'Y Axis', 'Z Axis'],
        values=[0, 1, 2]))
    def SetAxis(self, axis):
        SliceThroughTime.SetAxis(self, axis)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def GetTimestepValues(self):
        """This is critical for registering the timesteps"""
        return SliceThroughTime.GetTimestepValues(self)


###############################################################################


@smproxy.filter(name='PVGeoManySlicesAlongPoints', label=ManySlicesAlongPoints.__displayname__)
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
@smproperty.input(name="Data Set", port_index=1)
@smdomain.datatype(dataTypes=["vtkDataSet"], composite_data_supported=False)
@smproperty.input(name="Points", port_index=0)
@smdomain.datatype(dataTypes=["vtkPolyData"], composite_data_supported=False)
class PVGeoManySlicesAlongPoints(ManySlicesAlongPoints):
    def __init__(self):
        ManySlicesAlongPoints.__init__(self)

    @smproperty.intvector(name="Number of Slices", default_values=10)
    @smdomain.intrange(min=2, max=25)
    def SetNumberOfSlices(self, num):
        ManySlicesAlongPoints.SetNumberOfSlices(self, num)


    @smproperty.xml(_helpers.getPropertyXml(name='Use Neareast Nbr Approx',
        command='SetUseNearestNbr', default_values=False,
        help='A boolean to control whether or not to use SciPy nearest neighbor approximation when build cell connectivity.'))
    def SetUseNearestNbr(self, flag):
        ManySlicesAlongPoints.SetUseNearestNbr(self, flag)


###############################################################################


@smproxy.filter(name='PVGeoSlideSliceAlongPoints', label=SlideSliceAlongPoints.__displayname__)
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
@smproperty.input(name="Data Set", port_index=1)
@smdomain.datatype(dataTypes=["vtkDataSet"], composite_data_supported=False)
@smproperty.input(name="Points", port_index=0)
@smdomain.datatype(dataTypes=["vtkPolyData"], composite_data_supported=False)
class PVGeoSlideSliceAlongPoints(SlideSliceAlongPoints):
    def __init__(self):
        SlideSliceAlongPoints.__init__(self)

    @smproperty.intvector(name="Location", default_values=50)
    @smdomain.intrange(min=0, max=99)
    def SetLocation(self, loc):
        SlideSliceAlongPoints.SetLocation(self, loc)


    @smproperty.xml(_helpers.getPropertyXml(name='Use Neareast Nbr Approx',
        command='SetUseNearestNbr', default_values=False,
        help='A boolean to control whether or not to use SciPy nearest neighbor approximation when build cell connectivity.'))
    def SetUseNearestNbr(self, flag):
        SlideSliceAlongPoints.SetUseNearestNbr(self, flag)

###############################################################################


@smproxy.filter(name='PVGeoRotatePoints', label=RotatePoints.__displayname__)
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Points" />''' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkPolyData"], composite_data_supported=True)
class PVGeoRotatePoints(RotatePoints):
    def __init__(self):
        RotatePoints.__init__(self)

    #### Seters and Geters ####

    @smproperty.doublevector(name="Rotation Angle", default_values=45.0)
    @smdomain.doublerange(min=-90.0, max=90.0)
    def SetRotationDegrees(self, theta):
        RotatePoints.SetRotationDegrees(self, theta)

    @smproperty.doublevector(name="Origin", default_values=[0.0, 0.0], panel_visibility='advanced')
    def SetOrigin(self, xo, yo):
        RotatePoints.SetOrigin(self, xo, yo)

    @smproperty.xml(_helpers.getPropertyXml(name='Use Corner',
        command='SetUseCorner', default_values=True,
        help='Use the corner as the rotation origin.', panel_visibility='advanced'))
    def SetUseCorner(self, flag):
        RotatePoints.SetUseCorner(self, flag)


###############################################################################
@smproxy.filter(name='PVGeoExtractPoints', label=ExtractPoints.__displayname__)
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Points" />''' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkDataSet"], composite_data_supported=False)
class PVGeoExtractPoints(ExtractPoints):
    def __init__(self):
        ExtractPoints.__init__(self)


###############################################################################


@smproxy.filter(name='PVGeoPercentThreshold', label=PercentThreshold.__displayname__)
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkDataSet"], composite_data_supported=False)
class PVGeoPercentThreshold(PercentThreshold):
    def __init__(self):
        PercentThreshold.__init__(self)

    #### Seters and Geters ####

    @smproperty.doublevector(name="Percent", default_values=50.0)
    @smdomain.doublerange(min=0.0, max=100.0)
    def SetPercent(self, percent):
        PercentThreshold.SetPercent(self, percent)


    @smproperty.xml(_helpers.getPropertyXml(name='Use Continuous Cell Range',
        command='SetUseContinuousCellRange', default_values=False))
    def SetUseContinuousCellRange(self, flag):
        PercentThreshold.SetUseContinuousCellRange(self, flag)

    @smproperty.xml(_helpers.getPropertyXml(name='Invert',
        command='SetInvert', default_values=False,
        help='Use to invert the threshold filter.'))
    def SetInvert(self, flag):
        PercentThreshold.SetInvert(self, flag)

    @smproperty.xml(_helpers.getInputArrayXml(nInputPorts=1, numArrays=1))
    def SetInputArrayToProcess(self, idx, port, connection, field, name):
        return PercentThreshold.SetInputArrayToProcess(self, idx, port, connection, field, name)


###############################################################################


# Combine Tables
@smproxy.filter(name='PVGeoExtractArray', label=ExtractArray.__displayname__)
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkDataSet"], composite_data_supported=False)
class PVGeoExtractArray(ExtractArray):
    def __init__(self):
        ExtractArray.__init__(self)

    @smproperty.xml(_helpers.getInputArrayXml(nInputPorts=1, numArrays=1))
    def SetInputArrayToProcess(self, idx, port, connection, field, name):
        return ExtractArray.SetInputArrayToProcess(self, idx, port, connection, field, name)


###############################################################################


# Extract Cell Centers
@smproxy.filter(name='PVGeoExtractCellCenters', label=ExtractCellCenters.__displayname__)
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkDataSet"], composite_data_supported=True)
class PVGeoExtractCellCenters(ExtractCellCenters):
    def __init__(self):
        ExtractCellCenters.__init__(self)


###############################################################################


# Extract Cell Centers
@smproxy.filter(name='PVGeoAppendCellCenters', label=AppendCellCenters.__displayname__)
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkDataSet"], composite_data_supported=True)
class PVGeoAppendCellCenters(AppendCellCenters):
    def __init__(self):
        AppendCellCenters.__init__(self)


###############################################################################


# IterateOverPoints
@smproxy.filter(name='PVGeoIterateOverPoints', label=IterateOverPoints.__displayname__)
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Points" />
    <Visibility replace_input="0" />''' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkPolyData"], composite_data_supported=True)
class PVGeoIterateOverPoints(IterateOverPoints):
    def __init__(self):
        IterateOverPoints.__init__(self)


    #### Seters and Geters ####

    @smproperty.intvector(name="Decimate", default_values=75)
    @smdomain.intrange(min=1, max=99)
    def SetDecimate(self, percent):
        IterateOverPoints.SetDecimate(self, percent)

    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def SetTimeDelta(self, dt):
        IterateOverPoints.SetTimeDelta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def GetTimestepValues(self):
        """This is critical for registering the timesteps"""
        return IterateOverPoints.GetTimestepValues(self)



###############################################################################


@smproxy.filter(name='PVGeoConvertUnits', label=ConvertUnits.__displayname__)
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkDataSet"], composite_data_supported=True)
class PVGeoConvertUnits(ConvertUnits):
    def __init__(self):
        ConvertUnits.__init__(self)

    #### SETTERS AND GETTERS ####

    @smproperty.xml(_helpers.getDropDownXml(name='Conversion', command='SetConversion', labels=ConvertUnits.LookupConversions(True), help='This will set the spatial conversion.'))
    def SetConversion(self, key):
        ConvertUnits.SetConversion(self, key)

###############################################################################

try:
    # Coordinate system filters depend on pyproj
    # pyproj may not be available on Windows
    import pyproj
    @smproxy.filter(name='PVGeoLonLatToUTM', label=LonLatToUTM.__displayname__)
    @smhint.xml('''<ShowInMenu category="%s"/>
        <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
    @smproperty.input(name="Input", port_index=0)
    @smdomain.datatype(dataTypes=["vtkPolyData"], composite_data_supported=True)
    class PVGeoLonLatToUTM(LonLatToUTM):
        def __init__(self):
            LonLatToUTM.__init__(self)

        @smproperty.intvector(name="Zone", default_values=11)
        @smdomain.intrange(min=1, max=60)
        def SetZone(self, zone):
            LonLatToUTM.SetZone(self, zone)

        @smproperty.xml(_helpers.getDropDownXml(name='Ellps', command='SetEllps', labels=LonLatToUTM.GetAvailableEllps(), help='This will set the ellps.'))
        def SetEllps(self, ellps):
            LonLatToUTM.SetEllps(self, ellps)
except:
    pass


###############################################################################


@smproxy.filter(name='PVGeoArraysToRGBA', label=ArraysToRGBA.__displayname__)
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkDataSet"], composite_data_supported=False)
class PVGeoArraysToRGBA(ArraysToRGBA):
    def __init__(self):
        ArraysToRGBA.__init__(self)

    #### Seters and Geters ####
    @smproperty.xml(_helpers.getInputArrayXml(nInputPorts=1, numArrays=4, labels=['Red', 'Green', 'Blue', 'Transparency']))
    def SetInputArrayToProcess(self, idx, port, connection, field, name):
        return ArraysToRGBA.SetInputArrayToProcess(self, idx, port, connection, field, name)

    @smproperty.xml(_helpers.getPropertyXml(name='Use Transparency',
        command='SetUseTransparency', default_values=False,
        help='A boolean to control whether or not to use the Transparency array.'))
    def SetUseTransparency(self, flag):
        ArraysToRGBA.SetUseTransparency(self, flag)


    @smproperty.doublevector(name="Mask", default_values=-9999.0)
    def SetMaskValue(self, val):
        ArraysToRGBA.SetMaskValue(self, val)

###############################################################################


# Append Table to Cell Data
@smproxy.filter(name='PVGeoAppendTableToCellData', label=AppendTableToCellData.__displayname__)
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
@smproperty.input(name="Table", port_index=1)
@smdomain.datatype(dataTypes=["vtkTable"], composite_data_supported=False)
@smproperty.input(name="DataSet", port_index=0)
@smdomain.datatype(dataTypes=["vtkDataSet"], composite_data_supported=False)
class PVGeoAppendTableToCellData(AppendTableToCellData):
    def __init__(self):
        AppendTableToCellData.__init__(self)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def GetTimestepValues(self):
        """This is critical for registering the timesteps"""
        return AppendTableToCellData.GetTimestepValues(self)

###############################################################################

# BuildSurfaceFromPoints
@smproxy.filter(name='PVGeoBuildSurfaceFromPoints', label=BuildSurfaceFromPoints.__displayname__)
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkPolyData"], composite_data_supported=True)
class PVGeoBuildSurfaceFromPoints(BuildSurfaceFromPoints):
    def __init__(self):
        BuildSurfaceFromPoints.__init__(self)

    @smproperty.stringvector(name="Z Coords", default_values='0. 50.0')
    def SetZCoordsStr(self, zcellstr):
        BuildSurfaceFromPoints.SetZCoordsStr(self, zcellstr)


###############################################################################
