Name = 'CreateEarthSource'
Label = 'Create Earth Source'
FilterCategory = 'PVGP Sources'
Help = ''

NumberOfInputs = 0
OutputDataType = 'vtkPolyData'
ExtraXml = ''

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
