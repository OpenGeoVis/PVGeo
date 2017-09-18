Name = 'PointsToTube'
Label = 'Points To Tube'
Help = 'Takes points from a vtkPolyData object and constructs a line of those points then builds a polygonal tube around that line with some specified radius and number of sides.'

NumberOfInputs = 1
InputDataType = 'vtkPolyData'
OutputDataType = 'vtkPolyData'
ExtraXml = '''\
<Hints>
    <ShowInMenu category="CSM Geophysics Filters" />
</Hints>
'''


Properties = dict(
    Number_of_Sides=20,
    Radius=10.0,
)


def RequestData():
    pdi = self.GetInput() # VTK PolyData Type
    pdo = self.GetOutput() # VTK PolyData Type

    pdo.DeepCopy(pdi)
    numPoints = pdi.GetNumberOfPoints()

    # VTK_POLY_LINE is 4
    # Type map is specified in vtkCellType.h
    Cell_Type = 4
    ptsi = [i for i in range(numPoints)]
    pdo.InsertNextCell(Cell_Type, numPoints, ptsi)

    # Make a tube from the PolyData line:
    tube = vtk.vtkTubeFilter()
    tube.SetInputData(pdo)
    tube.SetRadius(Radius)
    tube.SetNumberOfSides(Number_of_Sides)
    tube.Update()
    pdo.ShallowCopy(tube.GetOutput())
