"""
Example python filter demonstrating some of the features available for
python programmable filters.
"""
# Name to be used for coding/macros:
Name = 'ExampleMult'
# Label for the filter menu:
Label = 'ExampleMult'
# The filter/source menu category:
FilterCategory = 'PVGP Filters'

# A general overview of the plugin
Help = 'This is a simple example of a Python Programmable Filter'

NumberOfInputs = 3 # Specify as many as you would like
InputDataType = '' # Leave blank if input doesn't matter
OutputDataType = 'vtkPolyData' # Leave blank to preserve input data type

# How to add input arrays:
#- Number of Input array drop down choices
#NumberOfInputArrayChoices = 0
#- Labels for the array drop down choices:
#InputArrayLabels = ['Array']
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
    import PVGPpy.helpers as inputhelp
    pdi = self.GetInput() # VTK Data Type
    pdo = self.GetOutput() # VTK Data Type
    # Get input array info (selection made in drop down menu)
    name = inputhelp.getSelectedArrayName(self, 0)
    field = inputhelp.getSelectedArrayField(self, 0)

    print(name, field)
    print(inputs)
