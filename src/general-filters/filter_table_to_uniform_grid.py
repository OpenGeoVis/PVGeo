Name = 'TableToUniformGrid'
Label = 'Table To Uniform Grid'
FilterCategory = 'PVGP Filters'
Help = 'This filter takes a vtkTable object with columns that represent data to be translated (reshaped) into a 3D grid (2D also works, just set the third dimensions extent to 1). The grid will be a n1 by n2 by n3 vtkImageData structure and an origin (south-west bottom corner) can be set at any xyz point. Each column of the vtkTable will represent a data attribute of the vtkImageData formed (essentially a uniform mesh). The SEPlib option allows you to unfold data that was packed in the SEPlib format where the most important dimension is z and thus the z data is d1 (d1=z, d2=y, d3=x). When using SEPlib, specify n1 as the number of elements in the Z-direction, n2 as the number of elements in the X-direction, and n3 as the number of elements in the Y-direction (and so on for other parameters).'

NumberOfInputs = 1
InputDataType = 'vtkTable'
OutputDataType = 'vtkImageData'
ExtraXml = '''
<IntVectorProperty
    name="order"
    command="SetParameter"
    number_of_elements="1"
    initial_string="test_drop_down_menu"
    default_values="0">
    <EnumerationDomain name="enum">
            <Entry value="0" text="Fortran-style: column-major order"/>
            <Entry value="1" text="C-style: Row-major order"/>
    </EnumerationDomain>
    <Documentation>
        This is the type of memory ordering to use.
    </Documentation>
</IntVectorProperty>
'''



Properties = dict(
    extent=[1, 1, 1],
    spacing=[1.0, 1.0, 1.0],
    origin=[0.0, 0.0, 0.0],
    SEPlib=True,
    Transpose_XY=True,
    order=0
)

PropertiesHelp = dict(
    SEPlib='Use the Stanford Exploration Project\'s axial conventions (d1=z, d2=x, d3=y). Parameters would be entered [z,x,y].'
)

def RequestData():
    from PVGPpy.filt import tableToGrid
    from vtk.util import numpy_support as nps
    import numpy as np

    if order == 0:
        mem = 'F'
    elif order == 1:
        mem = 'C'
    else:
        mem = 'C'

    pdi = self.GetInput()
    image = self.GetOutput() #vtkImageData

    tableToGrid(pdi, extent, spacing, origin, SEPlib=SEPlib, order=mem, swapXY=Transpose_XY, pdo=image)



def RequestInformation():
    from paraview import util
    from PVGPpy.filt import refoldidx
    # Setup the ImageData
    idx = refoldidx(SEPlib=SEPlib, swapXY=Transpose_XY)
    nx,ny,nz = extent[idx[0]],extent[idx[1]],extent[idx[2]]
    # ABSOLUTELY NECESSARY FOR THE FILTER TO WORK:
    util.SetOutputWholeExtent(self, [0,nx-1, 0,ny-1, 0,nz-1])
