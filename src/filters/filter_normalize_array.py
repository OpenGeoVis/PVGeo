Name = 'NormalizeArray'
Label = 'Normalize Array'
Help = 'Help for the Test Filter'

NumberOfInputs = 1
# Works on any data type so no need to specify input/ouptut
ExtraXml = '''\
<Hints>
    <ShowInMenu category="CSM Geophysics Filters" />
</Hints>

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
    </EnumerationDomain>
    <Documentation>
        This property indicates which two axii will be swapped.
    </Documentation>
</IntVectorProperty>
'''


Properties = dict(
    multiplyer=1.0,
    new_array_name='',
    Normalization=0,
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
        arr = wpdi.RowData[name]


    # perform normalization math
    #arr = nps.vtk_to_numpy(c)

    # Feature Scale
    if Normalization == 0:
        arr = (arr - np.min(arr)) / (np.max(arr) - np.min(arr))
    # Standard Score
    elif Normalization == 1:
        arr = (arr - np.mean(arr)) / (np.std(arr))

    arr *= multiplyer

    c = nps.numpy_to_vtk(num_array=arr,deep=True)

    # If no name given for data by user, use the basename of the file
    if new_array_name == '':
        new_array_name = 'Normalized ' + name
    c.SetName(new_array_name)

    pdo.DeepCopy(pdi)

    # Point Data
    if field == 0:
        pdo.GetPointData().AddArray(c)
    # Cell Data:
    elif field == 1:
        pdo.GetCellData().AddArray(c)
    # Field Data:
    elif field == 2:
        pdo.GetFieldData().AddArray(c)
    # Row Data:
    elif field == 6:
        pdo.GetRowData().AddArray(c)
    else:
        raise Exception('Field association not defined. Try inputing Point, Cell, Field, or Row data.')
