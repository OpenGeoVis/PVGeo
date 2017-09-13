Name = 'PointsToPolyLine'
Label = 'Points To PolyLine'
Help = 'Takes points from a vtkPolyData object and constructs a vtkPolyLine of those points. Useful for the native Slice Along PolyLine filter.'

NumberOfInputs = 1
InputDataType = 'vtkPolyData'
OutputDataType = 'vtkPolyData'
ExtraXml = '''\
<Hints>
    <ShowInMenu category="CSM Geophysics Filters" />
</Hints>
'''


Properties = dict(
)


def RequestData():
    pdi = self.GetInput() # VTK PolyData Type
    pdo = self.GetOutput() # VTK PolyData Type

    pdo.DeepCopy(pdi)

    numPoints = pdi.GetNumberOfPoints()

    for i in range(0, numPoints-1):
        points = [i, i+1]
        # VTK_POLY_LINE is 4
        # Type map is specified in vtkCellType.h
        pdo.InsertNextCell(4, 2, points)
