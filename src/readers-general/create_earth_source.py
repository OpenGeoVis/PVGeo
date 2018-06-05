Name = 'CreateEarthSource'
Label = 'Create Earth Source'
Help = ''

NumberOfInputs = 0
OutputDataType = 'vtkPolyData'
ExtraXml = ''
FileSeries = False # ABSOLUTELY NECESSARY

Properties = dict(
    Radius=6371.0,
)

def RequestData():
    pdo = self.GetOutput()
    earth = vtk.vtkEarthSource()
    earth.SetRadius(Radius)
    earth.OutlineOn()
    earth.Update()

    pdo.DeepCopy(earth.GetOutput())
