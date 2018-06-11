"""
Example python filter demonstrating some of the features available for
python programmable filters.
"""
# Name to be used for coding/macros:
Name = 'ExampleFilterMultInput'
# Label for the filter menu:
Label = 'Example Filter Multiple Inputs'
# The filter/source menu category:
FilterCategory = 'PVGP Filters'

# A general overview of the plugin
Help = 'This is a simple example of a Python Programmable Filter with mutiple inputs.'

NumberOfInputs = 2 # Specify as many as you would like
InputNames = ['Input foo 1', 'Input foo 2']
InputDataType = ['vtkDataObject', 'vtkDataObject']
OutputDataType = 'vtkPolyData' # Must be specified when many inputs specified

# How to add input arrays:
#- Number of Input array drop down choices
NumberOfInputArrayChoices = [1,1]
#- Labels for the array drop down choices:
InputArrayLabels = [['Array Input 1'], ['Array Input 2']]

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
    import PVGeo._helpers as inputhelp
    pdo = self.GetOutput() # VTK Data Type
    # Inputs from different ports:
    pdi0 = self.GetInputDataObject(0, 0) # PORT 0
    pdi1 = self.GetInputDataObject(1, 0) # PORT 1

    # DO STUFF WITH INOUTS AND OUTPUTS
    print(type(pdi0))
    print(type(pdi1))

    name0 = inputhelp.getSelectedArrayName(self, 0)
    name1 = inputhelp.getSelectedArrayName(self, 1)

    print(name0,name1)
