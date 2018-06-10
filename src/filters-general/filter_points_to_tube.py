Name = 'PointsToTube'
Label = 'Points To Tube'
Help = 'Takes points from a vtkPolyData object and constructs a line of those points then builds a polygonal tube around that line with some specified radius and number of sides.'

NumberOfInputs = 1
InputDataType = 'vtkPolyData'
OutputDataType = 'vtkPolyData'
ExtraXml = ''


Properties = dict(
    Number_of_Sides=20,
    Radius=10.0,
    Use_nearest_nbr=True,
)


def RequestData():
    from PVGPpy.filters_general import pointsToTube
    pdi = self.GetInput() # VTK PolyData Type
    pdo = self.GetOutput() # VTK PolyData Type

    pointsToTube(pdi, radius=Radius, numSides=Number_of_Sides, nrNbr=Use_nearest_nbr, pdo=pdo)
