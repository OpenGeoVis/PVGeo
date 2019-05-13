paraview_plugin_version = '2.0.0'
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

    @smproperty.xml(_helpers.get_drop_down_xml(name='CellType', command='set_cell_type',
        labels=['Line', 'Poly Line'], values=[3, 4]))
    def set_cell_type(self, cell_type):
        AddCellConnToPoints.set_cell_type(self, cell_type)

    @smproperty.xml(_helpers.get_property_xml(name='Use Neareast Nbr Approx',
        command='set_use_nearest_nbr', default_values=False,
        help='A boolean to control whether or not to use SciPy nearest neighbor approximation when build cell connectivity.'))
    def set_use_nearest_nbr(self, flag):
        AddCellConnToPoints.set_use_nearest_nbr(self, flag)

    @smproperty.xml(_helpers.get_property_xml(name='Use Unique Points',
        command='set_use_unique_points', default_values=False,
        help='Set a flag on whether to only use unique points'))
    def set_use_unique_points(self, flag):
        AddCellConnToPoints.set_use_unique_points(self, flag)



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

    @smproperty.xml(_helpers.get_input_array_xml(nInputPorts=1, n_arrays=1))
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
    def set_radius(self, radius):
        PointsToTube.set_radius(self, radius)

    @smproperty.intvector(name="Number of Sides", default_values=20)
    def set_number_of_sides(self, num):
        PointsToTube.set_number_of_sides(self, num)

    @smproperty.xml(_helpers.get_property_xml(name='Use Nearest Neighbor',
        command='set_use_nearest_nbr', default_values=False,
        help='A boolean to set whether to use a nearest neighbor approxiamtion when building path from input points.'))
    def set_use_nearest_nbr(self, flag):
        PointsToTube.set_use_nearest_nbr(self, flag)

    @smproperty.xml(_helpers.get_property_xml(name='Capping',
        command='set_capping', default_values=False,
        help='A boolean to set whether to cap the ends of the tube.'))
    def set_capping(self, flag):
        PointsToTube.set_capping(self, flag)

    @smproperty.xml(_helpers.get_drop_down_xml(name='CellType', command='set_cell_type',
        labels=['Line', 'Poly Line'], values=[3, 4]))
    def set_cell_type(self, cell_type):
        PointsToTube.set_cell_type(self, cell_type)

    @smproperty.xml(_helpers.get_property_xml(name='Use Unique Points',
        command='set_use_unique_points', default_values=False,
        help='Set a flag on whether to only use unique points'))
    def set_use_unique_points(self, flag):
        PointsToTube.set_use_unique_points(self, flag)



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
    def set_names(self, names):
        """Set names using a semicolon (;) seperated list"""
        # parse the names (a semicolon seperated list of names)
        ReshapeTable.set_names(self, names)

    @smproperty.intvector(name="Number of Columns", default_values=6)
    def set_number_of_columns(self, ncols):
        ReshapeTable.set_number_of_columns(self, ncols)

    @smproperty.intvector(name="Number of Rows", default_values=126)
    def set_number_of_rows(self, nrows):
        ReshapeTable.set_number_of_rows(self, nrows)

    @smproperty.xml(_helpers.get_drop_down_xml(name='Order', command='set_order',
        labels=['Fortran-style: column-major order', 'C-style: Row-major order'],
        values=[0, 1]))
    def set_order(self, order):
        o = ['F', 'C']
        ReshapeTable.set_order(self, o[order])



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

    @smproperty.xml(_helpers.get_property_xml(name='Estimate Grid Spacing',
        command='set_estimate_grid', default_values=True,
        help='A boolean to set whether to try to estimate the proper dx, dy, and dz spacings for a grid on a regular cartesian coordinate system.', panel_visibility='advanced'))
    def set_estimate_grid(self, flag):
        VoxelizePoints.set_estimate_grid(self, flag)

    @smproperty.xml(_helpers.get_property_xml(name='Cell Size', command='set_cell_size', default_values=[10.0, 10.0, 10.0], help='The cell size (dx, dy, dz) to use as a default for all generated voxels.', panel_visibility='advanced'))
    def set_cell_size(self, dx, dy, dz):
        VoxelizePoints.set_deltas(self, dx, dy, dz)


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
        self.set_estimate_grid(False) # CRUCIAL

    def _copy_arrays(self, pdi, pdo):
        """Override to not pass spacing arrays to output"""
        exclude = [self.__dx_id[1], self.__dy_id[1], self.__dz_id[1]]
        for i in range(pdi.GetPointData().GetNumberOfArrays()):
            arr = pdi.GetPointData().GetArray(i)
            if arr.GetName() not in exclude:
                _helpers.add_array(pdo, 1, arr) # adds to CELL data
        return pdo

    def RequestData(self, request, inInfo, outInfo):
        # Handle input arrays
        pdi = self.GetInputData(inInfo, 0, 0)
        wpdi = dsa.WrapDataObject(pdi)
        dx = _helpers.get_numpy_array(wpdi, self.__dx_id[0], self.__dx_id[1])
        dy = _helpers.get_numpy_array(wpdi, self.__dy_id[0], self.__dy_id[1])
        dz = _helpers.get_numpy_array(wpdi, self.__dz_id[0], self.__dz_id[1])
        VoxelizePoints.set_deltas(self, dx, dy, dz)
        # call parent and make sure EstimateGrid is set to False
        return VoxelizePoints.RequestData(self, request, inInfo, outInfo)

    #### Seters and Geters ####

    #(int idx, int port, int connection, int fieldAssociation, const char *name)
    @smproperty.xml(_helpers.get_input_array_xml(labels=['dx','dy','dz'], nInputPorts=1, n_arrays=3))
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

    @smproperty.xml(_helpers.get_input_array_xml(nInputPorts=1, n_arrays=1))
    def SetInputArrayToProcess(self, idx, port, connection, field, name):
        return NormalizeArray.SetInputArrayToProcess(self, idx, port, connection, field, name)

    @smproperty.doublevector(name="Multiplier", default_values=1.0)
    def set_multiplier(self, val):
        NormalizeArray.set_multiplier(self, val)

    @smproperty.stringvector(name="New Array Name", default_values="Normalized")
    def set_new_array_name(self, name):
        NormalizeArray.set_new_array_name(self, name)

    @smproperty.xml(_helpers.get_drop_down_xml(name='Normalization', command='set_normalization', labels=NormalizeArray.get_normalization_names(), help='This is the type of normalization to apply to the input array.'))
    def set_normalization(self, norm):
        NormalizeArray.set_normalization(self, norm)

    @smproperty.xml(_helpers.get_property_xml(name='Absolute Value', command='set_take_absolute_value', default_values=False, help='This will take the absolute value of the array before normalization.'))
    def set_take_absolute_value(self, flag):
        NormalizeArray.set_take_absolute_value(self, flag)

    @smproperty.doublevector(name="Shifter", default_values=0.0)
    def set_shift(self, sft):
        NormalizeArray.set_shift(self, sft)


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

    @smproperty.xml(_helpers.get_input_array_xml(nInputPorts=1, n_arrays=2))
    def SetInputArrayToProcess(self, idx, port, connection, field, name):
        return ArrayMath.SetInputArrayToProcess(self, idx, port, connection, field, name)

    @smproperty.doublevector(name="Multiplier", default_values=1.0)
    def set_multiplier(self, val):
        ArrayMath.set_multiplier(self, val)

    @smproperty.stringvector(name="New Array Name", default_values="Mathed Up")
    def set_new_array_name(self, name):
        ArrayMath.set_new_array_name(self, name)

    @smproperty.xml(_helpers.get_drop_down_xml(name='Operation', command='set_operation', labels=ArrayMath.get_operation_names(), help='This is the type of operation to apply to the input arrays.'))
    def set_operation(self, op):
        ArrayMath.set_operation(self, op)


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
    def set_number_of_slices(self, num):
        ManySlicesAlongAxis.set_number_of_slices(self, num)

    @smproperty.xml(_helpers.get_drop_down_xml(name='Axis', command='set_axis',
        labels=['X Axis', 'Y Axis', 'Z Axis'],
        values=[0, 1, 2]))
    def set_axis(self, axis):
        ManySlicesAlongAxis.set_axis(self, axis)



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
    def set_number_of_slices(self, num):
        SliceThroughTime.set_number_of_slices(self, num)

    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def set_time_delta(self, dt):
        SliceThroughTime.set_time_delta(self, dt)

    @smproperty.xml(_helpers.get_drop_down_xml(name='Axis', command='set_axis',
        labels=['X Axis', 'Y Axis', 'Z Axis'],
        values=[0, 1, 2]))
    def set_axis(self, axis):
        SliceThroughTime.set_axis(self, axis)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def get_time_step_values(self):
        """This is critical for registering the timesteps"""
        return SliceThroughTime.get_time_step_values(self)


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
    def set_number_of_slices(self, num):
        ManySlicesAlongPoints.set_number_of_slices(self, num)


    @smproperty.xml(_helpers.get_property_xml(name='Use Neareast Nbr Approx',
        command='set_use_nearest_nbr', default_values=False,
        help='A boolean to control whether or not to use SciPy nearest neighbor approximation when build cell connectivity.'))
    def set_use_nearest_nbr(self, flag):
        ManySlicesAlongPoints.set_use_nearest_nbr(self, flag)


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
    def set_location(self, loc):
        SlideSliceAlongPoints.set_location(self, loc)


    @smproperty.xml(_helpers.get_property_xml(name='Use Neareast Nbr Approx',
        command='set_use_nearest_nbr', default_values=False,
        help='A boolean to control whether or not to use SciPy nearest neighbor approximation when build cell connectivity.'))
    def set_use_nearest_nbr(self, flag):
        SlideSliceAlongPoints.set_use_nearest_nbr(self, flag)

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
    def set_rotation_degrees(self, theta):
        RotatePoints.set_rotation_degrees(self, theta)

    @smproperty.doublevector(name="Origin", default_values=[0.0, 0.0], panel_visibility='advanced')
    def set_origin(self, xo, yo):
        RotatePoints.set_origin(self, xo, yo)

    @smproperty.xml(_helpers.get_property_xml(name='Use Corner',
        command='set_use_corner', default_values=True,
        help='Use the corner as the rotation origin.', panel_visibility='advanced'))
    def set_use_corner(self, flag):
        RotatePoints.set_use_corner(self, flag)


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
    def set_percent(self, percent):
        PercentThreshold.set_percent(self, percent)


    @smproperty.xml(_helpers.get_property_xml(name='Use Continuous Cell Range',
        command='set_use_continuous_cell_range', default_values=False))
    def set_use_continuous_cell_range(self, flag):
        PercentThreshold.set_use_continuous_cell_range(self, flag)

    @smproperty.xml(_helpers.get_property_xml(name='Invert',
        command='set_invert', default_values=False,
        help='Use to invert the threshold filter.'))
    def set_invert(self, flag):
        PercentThreshold.set_invert(self, flag)

    @smproperty.xml(_helpers.get_input_array_xml(nInputPorts=1, n_arrays=1))
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

    @smproperty.xml(_helpers.get_input_array_xml(nInputPorts=1, n_arrays=1))
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
    def set_decimate(self, percent):
        IterateOverPoints.set_decimate(self, percent)

    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def set_time_delta(self, dt):
        IterateOverPoints.set_time_delta(self, dt)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def get_time_step_values(self):
        """This is critical for registering the timesteps"""
        return IterateOverPoints.get_time_step_values(self)



###############################################################################


@smproxy.filter(name='PVGeoConvertUnits', label=ConvertUnits.__displayname__)
@smhint.xml('<ShowInMenu category="%s"/>' % MENU_CAT)
@smproperty.input(name="Input", port_index=0)
@smdomain.datatype(dataTypes=["vtkDataSet"], composite_data_supported=True)
class PVGeoConvertUnits(ConvertUnits):
    def __init__(self):
        ConvertUnits.__init__(self)

    #### SETTERS AND GETTERS ####

    @smproperty.xml(_helpers.get_drop_down_xml(name='Conversion', command='set_conversion', labels=ConvertUnits.lookup_conversions(True), help='This will set the spatial conversion.'))
    def set_conversion(self, key):
        ConvertUnits.set_conversion(self, key)

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
        def set_zone(self, zone):
            LonLatToUTM.set_zone(self, zone)

        @smproperty.xml(_helpers.get_drop_down_xml(name='Ellps', command='set_ellps', labels=LonLatToUTM.get_available_ellps(), help='This will set the ellps.'))
        def set_ellps(self, ellps):
            LonLatToUTM.set_ellps(self, ellps)
except ImportError:
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
    @smproperty.xml(_helpers.get_input_array_xml(nInputPorts=1, n_arrays=4, labels=['Red', 'Green', 'Blue', 'Transparency']))
    def SetInputArrayToProcess(self, idx, port, connection, field, name):
        return ArraysToRGBA.SetInputArrayToProcess(self, idx, port, connection, field, name)

    @smproperty.xml(_helpers.get_property_xml(name='Use Transparency',
        command='set_use_transparency', default_values=False,
        help='A boolean to control whether or not to use the Transparency array.'))
    def set_use_transparency(self, flag):
        ArraysToRGBA.set_use_transparency(self, flag)


    @smproperty.doublevector(name="Mask", default_values=-9999.0)
    def set_mask_value(self, val):
        ArraysToRGBA.set_mask_value(self, val)

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
    def get_time_step_values(self):
        """This is critical for registering the timesteps"""
        return AppendTableToCellData.get_time_step_values(self)

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
    def set_z_coords_str(self, zcellstr):
        BuildSurfaceFromPoints.set_z_coords_str(self, zcellstr)


###############################################################################
