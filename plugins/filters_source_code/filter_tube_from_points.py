Name = 'TubeFromPoints'
Label = 'Tube From Points'
Help = 'Takes points from a vtkPolyData object and constructs a line of those points then builds a tube around that line.'

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
    Radius=1.0,
    #Input_Arr=3,
)


def RequestData():
    pdi = self.GetInput() # VTK PolyData Type
    pdo = self.GetOutput() # VTK PolyData Type

    numPoints = pdi.GetNumberOfPoints()
    pdo.Allocate()

    for i in range(0, numPoints-1):
        points = [i, i+1]
        # VTK_LINE is 3
        pdo.InsertNextCell(3, 2, points)

    # Make a tube from the PolyData line:
    tube = vtk.vtkTubeFilter()
    tube.SetInputData(pdo)
    tube.SetRadius(10)
    tube.SetNumberOfSides(20)
    tube.Update()
    pdo.ShallowCopy(tube.GetOutput())
