Name = 'PointsTovtkUnstructuredGrid'
Label = 'Points To vtkUnstructuredGrid'
FilterCategory = 'CSM Geophysics Filters DEV'
Help = 'Input is vtkPolyData (from Table to Points Filter)'

NumberOfInputs = 1
InputDataType = 'vtkPolyData'
OutputDataType = 'vtkUnstructuredGrid'
ExtraXml = ''

Properties = dict(

)


def RequestData():
    pdi = self.GetInput()  # vtkPolyData -> from Table to Points Filter
    grid = self.GetOutput()  # vtkUnstructuredGrid

    #print(pdi.GetPoints())

    Ids = vtk.vtkIdList()
    for i in range(pdi.GetPoints().GetNumberOfPoints()):
        Ids.InsertNextId(i)


    grid.Allocate(1,1)
    grid.InsertNextCell(12, Ids)

    grid.SetPoints(pdi.GetPoints())

    # Add all columns of the table as arrays to the PointData
    for i in range(pdi.GetPointData().GetNumberOfArrays()):
        arr = pdi.GetPointData().GetArray(i)
        grid.GetPointData().AddArray(arr)

    grid.Squeeze()

def RequestInformation():
    from paraview import util
    # ABSOLUTELY NECESSARY FOR THE FILTER TO WORK:
    #util.SetOutputWholeExtent(self, [0,nx-1,0,ny-1,0,nz-1])
