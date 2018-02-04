Name = 'CorrelateArrays'
Label = 'Correlate Arrays'
FilterCategory = 'CSM GP Filters'
Help = ''

NumberOfInputs = 1
# Works on any data type so no need to specify input/ouptut
ExtraXml = '''\
<StringVectorProperty
    name="SelectInputScalars1"
    label="Array 1"
    command="SetInputArrayToProcess"
    default_values="0 NULL"
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
    name="SelectInputScalars2"
    label="Array 2"
    command="SetInputArrayToProcess"
    default_values="1 NULL"
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
    Multiplyer=1.0,
    New_Array_Name='',
)

PropertiesHelp = dict(
    Multiplyer="This is a static shifter/scale factor across the array after normalization.",
    New_Array_Name="Give the new normalized array a meaningful name.",
)


def RequestData():
    from PVGPpy.filt import correlateArrays

    pdi = self.GetInput()
    pdo = self.GetOutput()

    info1 = self.GetInputArrayInformation(0)
    info2 = self.GetInputArrayInformation(1)

    correlateArrays(pdi, info1, info2, multiplyer=Multiplyer, newName=New_Array_Name, pdo=pdo)
