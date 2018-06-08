"""
Example python filter demonstrating some of the features available for
python programmable filters.
"""
# Name to be used for coding/macros:
Name = 'ExamplePythonFilter'
# Label for the filter menu:
Label = 'Example Python Filter'
# The filter/source menu category:
FilterCategory = 'PVGP Filters'

# A general overview of the plugin
Help = 'This is a simple example of a Python Programmable Filter'

NumberOfInputs = 1 # Specify as many as you would like
InputDataType = 'vtkDataObject' # Leave blank if input doesn't matter
OutputDataType = 'vtkDataObject' # Leave blank to preserve input data type

# How to add input arrays:
#- Number of Input array drop down choices
NumberOfInputArrayChoices = 2
#- Labels for the array drop down choices:
InputArrayLabels = ['Array Input 1', 'Array Input 2']


# Any extra XML GUI components you might like:
ExtraXml = ''

# These are the parameters/properties of the plugin:
Properties = dict(
    test_bool=True,
    test_int=123,
    test_int_vector=[1, 2, 3],
    test_double=1.23,
    test_double_vector=[1.1, 2.2, 3.3],
    test_string='string value',
)

# This is the description for each of the properties variable:
#- Include if you'd like. Totally optional.
#- The variable name (key) must be identical to the property described.
PropertiesHelp = dict(
    test_bool='This is a description about the test_bool property!'
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

    if test_bool:
        print(name,field)
    else:
        print(test_string)



# Use if you need to set extents and what not
#- Information, spatial extent, ect
def RequestInformation(self):
    from paraview import util
    # This script is usually not necessary for filters
    # Here's an example of setting extents that might be necessary for plugin to function correctly:
    #util.SetOutputWholeExtent(self, [0,nx-1, 0,ny-1, 0,nz-1])
    print('Have a great day!')
