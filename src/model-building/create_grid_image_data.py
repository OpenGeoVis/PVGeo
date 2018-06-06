Name = 'CreateUniformGrid'
Label = 'Create Uniform Grid'
Help = ''

NumberOfInputs = 0
OutputDataType = 'vtkImageData'
ExtraXml = ''
FileSeries = False # ABSOLUTELY NECESSARY

Properties = dict(
    extent=[10, 10, 10],
    spacing=[1.0, 1.0, 1.0],
    origin=[0.0, 0.0, 0.0]
)

def RequestData():
    image = self.GetOutput() #vtkImageData
    nx,ny,nz = extent[0],extent[1],extent[2]
    sx,sy,sz = spacing[0],spacing[1],spacing[2]
    ox,oy,oz = origin[0],origin[1],origin[2]
    # Setup the ImageData
    image.SetDimensions(nx, ny, nz)
    image.SetOrigin(ox, oy, oz)
    image.SetSpacing(sx, sy, sz)
    image.SetExtent(0,nx-1, 0,ny-1, 0,nz-1)


def RequestInformation():
    from paraview import util
    # ABSOLUTELY NECESSARY FOR THE FILTER TO WORK:
    nx,ny,nz = extent[0],extent[1],extent[2]
    util.SetOutputWholeExtent(self, [0,nx-1, 0,ny-1, 0,nz-1])
