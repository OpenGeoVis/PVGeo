Name = 'CreateEmptyGrid'
Label = 'Create Empty Grid'
FilterCategory = 'CSM Geophysics Sources'
Help = ''

NumberOfInputs = 0
OutputDataType = 'vtkImageData'
ExtraXml = ''

Properties = dict(
    nx=1,
    ny=1,
    nz=1,
    x_spacing=1.0,
    y_spacing=1.0,
    z_spacing=1.0,
    x_origin=0.0,
    y_origin=0.0,
    z_origin=0.0,
)

def RequestData():
    image = self.GetOutput() #vtkImageData

    # Setup the ImageData
    image.SetDimensions(nx, ny, nz)
    image.SetOrigin(x_origin, y_origin, z_origin)
    image.SetSpacing(x_spacing, y_spacing, z_spacing)
    image.SetExtent(0,nx-1, 0,ny-1, 0,nz-1)


def RequestInformation():
    from paraview import util
    # ABSOLUTELY NECESSARY FOR THE FILTER TO WORK:
    util.SetOutputWholeExtent(self, [0,nx-1, 0,ny-1, 0,nz-1])
