Name = 'CreateOddRectilinearGrid'
Label = 'Create Odd Rectilinear Grid'
Help = 'This creates a vtkRectilinearGrid.'

NumberOfInputs = 0
OutputDataType = 'vtkRectilinearGrid'
ExtraXml = ''
FileSeries = False # ABSOLUTELY NECESSARY

Properties = dict(
    Num_Cells=[10, 10, 10],
    X_Range=[0.0, 1.0],
    Y_Range=[0.0, 1.0],
    Z_Range=[0.0, 1.0]
)

def RequestData():
    import numpy as np
    from vtk.util import numpy_support as nps

    pdo = self.GetOutput() #vtkRectilinearGrid
    nx,ny,nz = Num_Cells[0]+1,Num_Cells[1]+1,Num_Cells[2]+1

    xcoords = np.linspace(X_Range[0], X_Range[1], num=nx)
    ycoords = np.linspace(Y_Range[0], Y_Range[1], num=ny)
    zcoords = np.linspace(Z_Range[0], Z_Range[1], num=nz)

    data = np.random.rand(nx*ny*nz)

    # CONVERT TO VTK #
    xcoords = nps.numpy_to_vtk(num_array=xcoords,deep=True)
    ycoords = nps.numpy_to_vtk(num_array=ycoords,deep=True)
    zcoords = nps.numpy_to_vtk(num_array=zcoords,deep=True)
    data = nps.numpy_to_vtk(num_array=data,deep=True)

    pdo.SetDimensions(nx+1,ny+1,nz+1) # note this subtracts 1
    pdo.SetXCoordinates(xcoords)
    pdo.SetYCoordinates(ycoords)
    pdo.SetZCoordinates(zcoords)

    data.SetName('Random Data')
    # THIS IS CELL DATA! Add the model data to CELL data:
    pdo.GetCellData().AddArray(data)


def RequestInformation():
    from paraview import util
    # ABSOLUTELY NECESSARY FOR THE FILTER TO WORK:
    nx,ny,nz = Num_Cells[0]+1,Num_Cells[1]+1,Num_Cells[2]+1
    util.SetOutputWholeExtent(self, [0,nx-1, 0,ny-1, 0,nz-1])
