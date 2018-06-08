"""
Example python filter demonstrating some of the features available for
python programmable filters.
"""
# Name to be used for coding/macros:
Name = 'ExampleFilterMultInput'
# Label for the filter menu:
Label = 'Example FIlter Multiple Inputs'
# The filter/source menu category:
FilterCategory = 'PVGP Filters'

# A general overview of the plugin
Help = 'This is a simple example of a Python Programmable Filter with mutiple inputs.'

NumberOfInputs = 2 # Specify as many as you would like
InputNames = ['Input foo 1', 'Input foo 2']
InputDataType = ['vtkDataObject', 'vtkDataObject']
OutputDataType = 'vtkPolyData' # Must be specified when many inputs specified

# NOTE: Input arrays are not supported for filters with multiple inputs.

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
    # NOTE: `inputs` is a global variable containing the inputs in order.
    pdo = self.GetOutput() # VTK Data Type

    print(inputs[0])
    print(inputs[1])
