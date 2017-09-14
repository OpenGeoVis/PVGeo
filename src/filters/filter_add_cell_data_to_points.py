Name = 'AddCellDataToPoints'
Label = 'AddCellDataToPoints'
Help = ''

NumberOfInputs = 1
InputDataType = 'vtkPolyData'
OutputDataType = 'vtkPolyData'
ExtraXml = '''\
<Hints>
    <ShowInMenu category="CSM Geophysics Filters" />
</Hints>

<IntVectorProperty
    name="Cell_Type"
    command="SetParameter"
    number_of_elements="1"
    initial_string="test_drop_down_menu"
    default_values="0">
    <EnumerationDomain name="enum">
          <Entry value="3" text="Line"/>
          <Entry value="4" text="Poly Line"/>
    </EnumerationDomain>
    <Documentation>
        This property indicates which two axii will be swapped.
    </Documentation>
</IntVectorProperty>
'''


Properties = dict(
    Cell_Type=4
)


def RequestData():
    pdi = self.GetInput() # VTK PolyData Type
    pdo = self.GetOutput() # VTK PolyData Type

    pdo.DeepCopy(pdi)

    numPoints = pdi.GetNumberOfPoints()

    # Type map is specified in vtkCellType.h
    for i in range(0, numPoints-1):
        if Cell_Type == 3 or Cell_Type == 4:
            points = [i, i+1]
            pdo.InsertNextCell(Cell_Type, 2, points)
        if Cell_Type == 11 or Cell_Type == 12:
            #<Entry value="11" text="Voxell"/>
            #<Entry value="12" text="Hexahedron"/>
            points = [i, i+1, i+2, i+3]
            pdo.InsertNextCell(Cell_Type, 4, points)
