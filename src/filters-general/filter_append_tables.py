# Name to be used for coding/macros:
Name = 'CombineTables'
# Label for the filter menu:
Label = 'Combine Tables'

# A general overview of the plugin
Help = 'Takes two tables and combines them if they have the same number of rows.'

NumberOfInputs = 2 # Specify as many as you would like
InputNames = ['Input Table 1', 'Input Table 2']
InputDataType = ['vtkTable', 'vtkTable']
OutputDataType = 'vtkTable' # Must be specified when many inputs specified

# How to add input arrays:
#- Number of Input array drop down choices
#NumberOfInputArrayChoices = [1,1]
#- Labels for the array drop down choices:
#InputArrayLabels = [['Array Input 1'], ['Array Input 2']]

# Any extra XML GUI components you might like:
#ExtraXml = ''

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
    import PVGeo._helpers as inputhelp
    pdo = self.GetOutput() # VTK Data Type
    # Inputs from different ports:
    pdi0 = self.GetInputDataObject(0, 0) # PORT 0
    pdi1 = self.GetInputDataObject(1, 0) # PORT 1

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

    #
