Name = 'TestDropDown'
Label = 'Test Drop Down'
FilterCategory = 'CSM Geophysics Filters'
Help = ''

NumberOfInputs = 1
# Works on any data type so no need to specify input/ouptut
ExtraXml = '''\
<StringVectorProperty
    name="SelectInputScalarsX"
    label="ArrayX"
    command="SetInputArrayToProcess"
    number_of_elements="5"
    element_types="0 0 0 0 2"
    animateable="0">
    <ArrayListDomain
        name="array_list"
        attribute_type="Scalars"
        input_domain_name="inputs_array">
        <RequiredProperties>
            <Property
                name="Input"
                function="Input" />
        </RequiredProperties>
    </ArrayListDomain>
    <FieldDataDomain
        name="field_list">
        <RequiredProperties>
            <Property
                name="Input"
                function="Input" />
        </RequiredProperties>
    </FieldDataDomain>
</StringVectorProperty>

<StringVectorProperty
    name="SelectInputScalarsY"
    label="ArrayY"
    command="SetInputArrayToProcess"
    number_of_elements="5"
    element_types="0 0 0 0 2"
    animateable="0">
    <ArrayListDomain
        name="array_list"
        attribute_type="Scalars"
        input_domain_name="inputs_array">
        <RequiredProperties>
            <Property
                name="Input"
                function="Input" />
        </RequiredProperties>
    </ArrayListDomain>
    <FieldDataDomain
        name="field_list">
        <RequiredProperties>
            <Property
                name="Input"
                function="Input" />
        </RequiredProperties>
    </FieldDataDomain>
</StringVectorProperty>

'''


Properties = dict(
)


def RequestData():
    pdi = self.GetInput()
    pdo = self.GetOutput()

    # Get input array name
    info = self.GetInputArrayInformation(0)
    name = info.Get(vtk.vtkDataObject.FIELD_NAME())
    field = info.Get(vtk.vtkDataObject.FIELD_ASSOCIATION())
    print("0: ", name)

    info = self.GetInputArrayInformation(1)
    name = info.Get(vtk.vtkDataObject.FIELD_NAME())
    field = info.Get(vtk.vtkDataObject.FIELD_ASSOCIATION())
    print("1: ", name)
