# Name to be used for coding/macros:
Name = 'VoxelizePointsSpacing'
# Label for the filter menu:
Label = 'Voxelize Points with Spacing Arrays'

# A general overview of the plugin
Help = 'This makes a vtkUnstructuredGrid of scattered points given voxel sizes as input arrays'

NumberOfInputs = 1 # Specify as many as you would like
InputDataType = 'vtkPolyData' # data with points
OutputDataType = 'vtkUnstructuredGrid' # full of voxels

# How to add input arrays:
#- Number of Input array drop down choices
NumberOfInputArrayChoices = 3
#- Labels for the array drop down choices:
InputArrayLabels = ['dx', 'dy', 'dz']

# Any extra XML GUI components you might like:
ExtraXml = ''

# These are the parameters/properties of the plugin:
Properties = dict(
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
    # Get input array info (selection made in drop down menu)
    dx = inputhelp.getSelectedArray(self, wpdi, 0)
    dy = inputhelp.getSelectedArray(self, wpdi, 1)
    dz = inputhelp.getSelectedArray(self, wpdi, 2)
    names = [
        inputhelp.getSelectedArrayName(self, 0),
        inputhelp.getSelectedArrayName(self, 1),
        inputhelp.getSelectedArrayName(self, 2)
    ]


    voxelizePoints(x,y,z,dx,dy,dz, grid=pdo, estimate_grid=False)
    for i in range(pdi.GetPointData().GetNumberOfArrays()):
        arr = pdi.GetPointData().GetArray(i)
        if arr.GetName() in names:
            continue
        inputhelp.addArray(pdo, 1, arr) # adds to CELL data
