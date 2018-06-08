Name = 'CreateOddRectilinearGrid'
Label = 'Create Odd Rectilinear Grid'
Help = 'This creates a vtkRectilinearGrid.'

NumberOfInputs = 0
OutputDataType = 'vtkRectilinearGrid'
ExtraXml = ''
FileSeries = False # ABSOLUTELY NECESSARY

Properties = dict(
    Origin=[-350.0, -400.0, 0.0],
    X_Cells='200 100 50 20*50.0 50 100 200',
    Y_Cells='200 100 50 21*50.0 50 100 200',
    Z_Cells='20*25.0 50 100 200'
)

PropertiesHelp = dict(
    Origin='The XYZ origin of the Southwest-top of the grid.',
    X_Cells='A space delimited list of cell sizes along the X axis. You can use cell repeaters like 20*50.0 for twenty cells of width 50.0.',
    Y_Cells='A space delimited list of cell sizes along the Y axis. You can use cell repeaters like 20*50.0 for twenty cells of width 50.0.',
    Z_Cells='A space delimited list of cell sizes along the Z axis. You can use cell repeaters like 20*50.0 for twenty cells of width 50.0. These are orderd in the negative Z direction such that the first cell is at the highest in altitude.'
)

def RequestData():
    import numpy as np
    from vtk.util import numpy_support as nps
    from PVGPpy.model_building import oddModel

    pdo = self.GetOutput() #vtkRectilinearGrid
    oddModel(Origin, X_Cells, Y_Cells, Z_Cells, data=None, dataNm='Data', pdo=pdo)


def RequestInformation():
    from paraview import util
    from PVGPpy.model_building import oddModelExtent
    # ABSOLUTELY NECESSARY FOR THE SOURCE TO WORK:
    ext = oddModelExtent(X_Cells, Y_Cells, Z_Cells)
    util.SetOutputWholeExtent(self, ext)
