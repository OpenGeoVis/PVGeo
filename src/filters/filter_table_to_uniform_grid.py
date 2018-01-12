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
    C_ordering=True,
    Swap_XZ=False
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
    """

    temp = tableToGrid(pdi, extent, spacing, origin, SEPlib=SEPlib, C_ordering=C_ordering)

    image.ShallowCopy(temp)"""

    def CtoF(arr, ext):
        """
        Transforms for C- to F-Contiguosness
        """
        n1,n2,n3 = extent[0],extent[1],extent[2]
        arr = np.reshape(arr, (n1,n2,n3))
        arr = np.swapaxes(arr,0,2)
        arr = np.reshape(arr, (n1*n2*n3))
        return arr

    def rearangeSEPlib(arr, ext):
        # SWAP D1 AND D3 THEN SWAP D2 AND D1
        n3,n1,n2 = ext[0],ext[1],ext[2]
        arr = np.reshape(arr, (n3,n1,n2))
        arr = np.swapaxes(arr,0,1)
        arr = np.swapaxes(arr,0,2)
        arr = np.reshape(arr, (n1*n2*n3))
        return arr


    cols = pdi.GetNumberOfColumns()
    rows = pdi.GetColumn(0).GetNumberOfTuples()

    # Output Data Type:
    #image = vtk.vtkImageData() # vtkImageData

    # Setup the ImageData
    if SEPlib:
        # SEPlib: d1=z, d2=x, d3=y
        nz,nx,ny = extent[0],extent[1],extent[2]
        sz,sx,sy = spacing[0],spacing[1],spacing[2]
        oz,ox,oy = origin[0],origin[1],origin[2]
    else:
        # Cartesian: d1=x, d2=y, d3=z
        nx,ny,nz = extent[0],extent[1],extent[2]
        sx,sy,sz = spacing[0],spacing[1],spacing[2]
        ox,oy,oz = origin[0],origin[1],origin[2]
    if Swap_XZ:
        ttt = nx
        nx = nz
        nz = ttt

    # make sure dimensions work
    if (nx*ny*nz != rows):
        raise Exception('Total number of elements must remain %d. Check reshape dimensions (n1 by n2 by n3).' % (rows))

    image.SetDimensions(nx, ny, nz)
    image.SetOrigin(ox, oy, oz)
    image.SetSpacing(sx, sy, sz)
    image.SetExtent(0,nx-1, 0,ny-1, 0,nz-1)


    # Add all columns of the table as arrays to the PointData
    for i in range(cols):
        c = pdi.GetColumn(i)
        name = c.GetName()
        arr = nps.vtk_to_numpy(c)
        if C_ordering:
            arr = CtoF(arr, (nx,ny,nz))
        if SEPlib:
            arr = rearangeSEPlib(arr, (nx,ny,nz))
        c = nps.numpy_to_vtk(num_array=arr,deep=True)
        c.SetName(name)
        #image.GetCellData().AddArray(c) # Should we add here? flipper won't flip these...
        image.GetPointData().AddArray(c)


def RequestInformation():
    from paraview import util
    # Setup the ImageData
    # Cartesian: d1=x, d2=y, d3=z
    nx,ny,nz = extent[0],extent[1],extent[2]
    if SEPlib:
        # SEPlib: d1=z, d2=x, d3=y
        nz,nx,ny = extent[0],extent[1],extent[2]
    if Swap_XZ:
        ttt = nx
        nx = nz
        nz = ttt
    # ABSOLUTELY NECESSARY FOR THE FILTER TO WORK:
    util.SetOutputWholeExtent(self, [0,nx-1, 0,ny-1, 0,nz-1])
