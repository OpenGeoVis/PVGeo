Name = 'TableToUniformGrid'
Label = 'Table To Uniform Grid'
Help = 'This filter takes a vtkTable object with columns that represent data to be translated (reshaped) into a 3D grid (2D also works, just set the third dimensions extent to 1). The grid will be a n1 by n2 by n3 structure and an origin can be set at any xyz point. Each column of the vtkTable will represent a data attribute of the vtkImageData formed (essentially a uniform mesh). The SEPlib option allows you to unfold data that was packed in the SEPlib format where the most important dimension is z and thus the z data is d1 (d1=z, d2=x, d3=y).'

NumberOfInputs = 1
InputDataType = 'vtkTable'
OutputDataType = 'vtkImageData'
ExtraXml = '''\
<Hints>
    <ShowInMenu category="CSM Geophysics Filters" />
</Hints>
'''

Properties = dict(
    n1=1,
    n2=1,
    n3=1,
    s1_spacing=1.0,
    s2_spacing=1.0,
    s3_spacing=1.0,
    o1_origin=0.0,
    o2_origin=0.0,
    o3_origin=0.0,
    SEPlib=False
)

def RequestData():
    from vtk.util import numpy_support as nps
    import numpy as np
    pdi = self.GetInput()
    image = self.GetOutput() #vtkImageData

    cols = pdi.GetNumberOfColumns()
    rows = pdi.GetColumn(0).GetNumberOfTuples()

    # make sure dimensions work

    if (n1*n2*n3 != rows):
        raise Exception('Total number of elements must remain %d. Check reshape dimensions (n1 by n2 by n3).' % (rows))

    def RearangeSEPlib(arr):
        # SWAP D1 AND D3 THEN SWAP D2 AND D1
        import numpy as np
        arr = np.reshape(arr, (n2,n3,n1))
        arr = np.swapaxes(arr,0,1)
        arr = np.swapaxes(arr,0,2)
        arr = np.reshape(arr, (n1*n2*n3))
        return arr


    # Setup the ImageData
    if SEPlib:
        # SEPlib: d1=z, d2=x, d3=y
        # TODO: rearange input array
        image.SetDimensions(n2, n3, n1)
        image.SetOrigin(o2_origin, o3_origin, o1_origin)
        image.SetSpacing(s2_spacing, s3_spacing, s1_spacing)
        image.SetExtent(0,n2-1, 0,n3-1, 0,n1-1)
    else:
        # Cartesian: d1=x, d2=y, d3=z
        image.SetDimensions(n1, n2, n3)
        image.SetOrigin(o1_origin, o2_origin, o3_origin)
        image.SetSpacing(s1_spacing, s2_spacing, s3_spacing)
        image.SetExtent(0,n1-1, 0,n2-1, 0,n3-1)


    # Add all columns of the table as arrays to the PointData
    for i in range(cols):
        c = pdi.GetColumn(i)
        if SEPlib:
            name = c.GetName()
            arr = nps.vtk_to_numpy(c)
            arr = RearangeSEPlib(arr)
            c = nps.numpy_to_vtk(num_array=arr,deep=True)
            c.SetName(name)
        #image.GetCellData().AddArray(c) # Should we add here? flipper won't flip these...
        image.GetPointData().AddArray(c)


def RequestInformation():
    from paraview import util
    # ABSOLUTELY NECESSARY FOR THE FILTER TO WORK:
    if SEPlib:
        util.SetOutputWholeExtent(self, [0,n2-1, 0,n3-1, 0,n1-1])
    else:
        util.SetOutputWholeExtent(self, [0,n1-1, 0,n2-1, 0,n3-1])
