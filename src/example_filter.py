Name = 'ExamplePythonFilter'        # Name to be used for coding/macros
Label = 'Example Python Filter'     # Label for the filter menu
FilterCategory = 'CSM GP Filters'   # The filter/source menu category

# A general overview of the plugin
Help = 'This is a simple example of a Python Programmable Filter'

NumberOfInputs = 1                  # Specify as many as you would like
InputDataType = 'vtkPolyData'       # Leave blank if input doesn't matter
OutputDataType = 'vtkPolyData'      # Leave blank to preserve input data type

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
def RequestData():
    from vtk.util import numpy_support as nps
    pdi = self.GetInput() # VTK Data Type
    pdo = self.GetOutput() # VTK Data Type

    if test_bool:
        print(test_double_vector)
    else:
        print(test_string)

# Use if you need to set extents and what not
#- Information, spatial extent, ect
def RequestInformation():
    from paraview import util
    # This script is usually not necessary for filters
    # Here's an example of setting extents that might be necessary for plugin to function correctly
    #util.SetOutputWholeExtent(self, [0,nx-1, 0,ny-1, 0,nz-1])
    print('Have a great day!')
