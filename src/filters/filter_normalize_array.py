Name = 'NormalizeArray'
Label = 'Normalize Array'
FilterCategory = 'CSM Geophysics Filters'
Help = 'This filter allow the user to select an array from the input data set to be normalized. The filter will append another array to that data set for the output. The user can specify how they want to rename the array, can choose a multiplier, and can choose from two types of common normalizations: Feature Scaling and Standard Score.'

NumberOfInputs = 1
# Works on any data type so no need to specify input/ouptut
ExtraXml = '''\
<StringVectorProperty
    name="SelectInputScalars"
    label="Array"
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

<IntVectorProperty
    name="Normalization"
    command="SetParameter"
    number_of_elements="1"
    initial_string="test_drop_down_menu"
    default_values="0">
    <EnumerationDomain name="enum">
            <Entry value="0" text="Feature Scaling"/>
            <Entry value="1" text="Standard Score"/>
            <Entry value="2" text="Natural Log"/>
            <Entry value="3" text="Log Base 10"/>
    </EnumerationDomain>
    <Documentation>
        This is the type of normalization to apply to the input array.
    </Documentation>
</IntVectorProperty>
'''


Properties = dict(
    Multiplyer=1.0,
    New_Array_Name='',
    Normalization=0,
)

PropertiesHelp = dict(
    multiplyer="This is a static shifter/scale factor across the array after normalization.",
    new_array_name="Give the new normalized array a meaningful name.",
)


def RequestData():
    from PVGPpy.filt import normalizeArray

    pdi = self.GetInput()
    pdo = self.GetOutput()

    info = self.GetInputArrayInformation(0)

    normalizeArray(pdi, info, Normalization, multiplyer=Multiplyer, newName=New_Array_Name, pdo=pdo)
