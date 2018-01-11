Name = 'TableToUniformGrid'
Label = 'Table To Uniform Grid'
FilterCategory = 'CSM Geophysics Filters'
Help = 'This filter takes a vtkTable object with columns that represent data to be translated (reshaped) into a 3D grid (2D also works, just set the third dimensions extent to 1). The grid will be a n1 by n2 by n3 vtkImageData structure and an origin (south-west bottom corner) can be set at any xyz point. Each column of the vtkTable will represent a data attribute of the vtkImageData formed (essentially a uniform mesh). The SEPlib option allows you to unfold data that was packed in the SEPlib format where the most important dimension is z and thus the z data is d1 (d1=z, d2=x, d3=y). When using SEPlib, specify n1 as the number of elements in the Z-direction, n2 as the number of elements in the X-direction, and n3 as the number of elements in the Y-direction (and so on for other parameters).'

NumberOfInputs = 1
InputDataType = 'vtkTable'
OutputDataType = 'vtkImageData'
ExtraXml = ''

Properties = dict(
    extent=[1, 1, 1],
    spacing=[1.0, 1.0, 1.0],
    origin=[0.0, 0.0, 0.0],
    SEPlib=False,
    C_ordering=True
)

PropertiesHelp = dict(
    SEPlib='Use the Stanford Exploration Project\'s axial conventions (d1=z, d2=x, d3=y). Parameters would be entered [z,x,y].'
)

def RequestData():
    from PVGPpy.vis import tableToGrid
    from vtk.util import numpy_support as nps
    import numpy as np

    pdi = self.GetInput()
    image = self.GetOutput() #vtkImageData

    temp = tableToGrid(pdi, extent, spacing, origin, SEPlib=SEPlib, C_ordering=C_ordering)

    image.ShallowCopy(temp)


def RequestInformation():
    from paraview import util
    # Setup the ImageData
    # Cartesian: d1=x, d2=y, d3=z
    nx,ny,nz = extent[0],extent[1],extent[2]
    if SEPlib:
        # SEPlib: d1=z, d2=x, d3=y
        nz,nx,ny = extent[0],extent[1],extent[2]
    # ABSOLUTELY NECESSARY FOR THE FILTER TO WORK:
    util.SetOutputWholeExtent(self, [0,nx-1, 0,ny-1, 0,nz-1])
