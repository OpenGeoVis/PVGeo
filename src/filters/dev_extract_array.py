Name = 'ExtractArray'
Label = 'Extract Array'
FilterCategory = 'CSM Geophysics Filters DEV'
Help = 'Extracts an array from any input and returns that array as vtkPolyDta.'

NumberOfInputs = 1
InputDataType = ''
OutputDataType = 'vtkPolyData' #vtkPolyData
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
    name="Field_Type"
    command="SetParameter"
    number_of_elements="1"
    initial_string="test_drop_down_menu"
    default_values="0">
    <EnumerationDomain name="enum">
            <Entry value="0" text="Point Data"/>
            <Entry value="1" text="Cell Data"/>
    </EnumerationDomain>
    <Documentation>
        This property indicates which two axii will be swapped.
    </Documentation>
</IntVectorProperty>
'''


Properties = dict(
    Field_Type=0
)


def RequestData():
    from vtk.util import numpy_support as nps
    import numpy as np
    from vtk.numpy_interface import dataset_adapter as dsa
    from vtk.numpy_interface import algorithms as algs

    pdi = self.GetInput()
    pdo = self.GetOutput()

    # Get input array name
    info = self.GetInputArrayInformation(0)
    name = info.Get(vtk.vtkDataObject.FIELD_NAME())
    field = info.Get(vtk.vtkDataObject.FIELD_ASSOCIATION())

    wpdi = dsa.WrapDataObject(pdi)

    # Point Data
    if field == 0:
        arr = wpdi.PointData[name]
    # Cell Data:
    elif field == 1:
        arr = wpdi.CellData[name]
    # Field Data:
    elif field == 2:
        arr = wpdi.FieldData[name]
    # Row Data:
    elif field == 6:
        raise Exception('Row Data not supported.')
        #arr = wpdi.RowData[name]
    else:
        raise Exception('Field association not defined. Try inputing Point, Cell, Field, or Row data.')

    c = nps.numpy_to_vtk(num_array=arr,deep=True)
    c.SetName(name)

    # Point Data
    if Field_Type == 0:
        pdo.GetPointData().AddArray(c)
    # Cell Data:
    elif Field_Type == 1:
        pdo.GetCellData().AddArray(c)
