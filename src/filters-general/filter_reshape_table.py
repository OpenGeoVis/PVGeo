Name = 'ReshapeTable'
Label = 'Reshape Table'
Help = 'This filter will take a vtkTable object and reshape it. This filter essentially treats vtkTables as 2D matrices and reshapes them using numpy.reshape in a C contiguous manner. Unfortunately, data fields will be renamed arbitrarily because VTK data arrays require a name.'

NumberOfInputs = 1
InputDataType = 'vtkTable'
OutputDataType = 'vtkTable'
ExtraXml = '''
<IntVectorProperty
    name="Order"
    command="SetParameter"
    number_of_elements="1"
    initial_string="test_drop_down_menu"
    default_values="0">
    <EnumerationDomain name="enum">
            <Entry value="0" text="Fortran-style: column-major order"/>
            <Entry value="1" text="C-style: Row-major order"/>
    </EnumerationDomain>
    <Documentation>
        This is the type of memory ordering to use.
    </Documentation>
</IntVectorProperty>
'''


Properties = dict(
    ncols=6,
    nrows=126,
    Array_Names="",
    Order=0
)

PropertiesHelp = dict(
    Array_Names="A semicolon (;) seperated list of names for the arrays",
)


def RequestData():
    from PVGPpy.filt import reshapeTable

    pdi = self.GetInput() #vtkTable
    pdo = self.GetOutput() #vtkTable

    mem = 'C'
    if Order == 0:
        mem = 'F'

    reshapeTable(pdi, nrows, ncols, names=Array_Names, order=mem, pdo=pdo)
