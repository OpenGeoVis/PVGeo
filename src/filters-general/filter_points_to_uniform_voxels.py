# Name to be used for coding/macros:
Name = 'PointsToUniformVoxels'
# Label for the filter menu:
Label = 'Points To Uniform Voxels'

# A general overview of the plugin
Help = 'This makes a vtkUnstructuredGrid of scattered points given voxel sizes'

NumberOfInputs = 1 # Specify as many as you would like
InputDataType = 'vtkPolyData' # data with points
OutputDataType = 'vtkUnstructuredGrid' # full of voxels

# Any extra XML GUI components you might like:
ExtraXml = ''

# These are the parameters/properties of the plugin:
Properties = dict(
    dx=1.0,
    dy=1.0,
    dz=1.0,
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
    from PVGeo.filters_general import points2grid, addCellData
    pdi = self.GetInput() # poly data with points
    pdo = self.GetOutput() # vtkUnstructuredGrid
    wpdi = dsa.WrapDataObject(pdi)

    pts = wpdi.Points
    x,y,z = pts[:,0], pts[:,1], pts[:,2]
    points2grid(x,y,z,dx,dy,dz, grid=pdo)
    for i in range(pdi.GetPointData().GetNumberOfArrays()):
        arr = pdi.GetPointData().GetArray(i)
        inputhelp.addArray(pdo, 1, arr) # adds to CELL data
