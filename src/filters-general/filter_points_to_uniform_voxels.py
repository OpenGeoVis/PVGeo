# Name to be used for coding/macros:
Name = 'VoxelizePointsUniformly'
# Label for the filter menu:
Label = 'Voxelize Points Uniformly'

# A general overview of the plugin
Help = 'This makes a vtkUnstructuredGrid of scattered points by estimating a uniform voxel size. The user can also give the filter a voxel size to use.'

NumberOfInputs = 1 # Specify as many as you would like
InputDataType = 'vtkPolyData' # data with points
OutputDataType = 'vtkUnstructuredGrid' # full of voxels

# Any extra XML GUI components you might like:
ExtraXml = ''

# These are the parameters/properties of the plugin:
Properties = dict(
    dx=10.0,
    dy=10.0,
    dz=10.0,
    Estimate_Grid=True,
)

# This is the description for each of the properties variable:
#- Include if you'd like. Totally optional.
#- The variable name (key) must be identical to the property described.
PropertiesHelp = dict(
)

# Where your main processing occurs
#- Data processing
def RequestData(self):
    from vtk.util import numpy_support as nps
    from vtk.numpy_interface import dataset_adapter as dsa
    import PVGeo._helpers as inputhelp
    from PVGeo.filters_general import voxelizePoints, addCellData
    pdi = self.GetInput() # poly data with points
    pdo = self.GetOutput() # vtkUnstructuredGrid
    wpdi = dsa.WrapDataObject(pdi)

    pts = wpdi.Points
    x,y,z = pts[:,0], pts[:,1], pts[:,2]
    voxelizePoints(x,y,z,dx,dy,dz, grid=pdo, estimate_grid=Estimate_Grid)
    for i in range(pdi.GetPointData().GetNumberOfArrays()):
        arr = pdi.GetPointData().GetArray(i)
        inputhelp.addArray(pdo, 1, arr) # adds to CELL data
