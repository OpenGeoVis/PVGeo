Name = 'SwapAxiiImageData'
Label = 'Swap Axii Image Data'
FilterCategory = 'CSM Geophysics Filters DEV'
Help = ''

NumberOfInputs = 1
InputDataType = 'vtkImageData'
OutputDataType = 'vtkImageData'
ExtraXml = '''\
<IntVectorProperty
    name="Swap"
    command="SetParameter"
    number_of_elements="1"
    initial_string="test_drop_down_menu"
    default_values="0">
    <EnumerationDomain name="enum">
          <Entry value="0" text="Swap X and Y axii"/>
          <Entry value="1" text="Swap X and Z axii"/>
          <Entry value="2" text="Swap Y and Z axii"/>
    </EnumerationDomain>
    <Documentation>
        This property indicates which two axii will be swapped.
    </Documentation>
</IntVectorProperty>
'''

Properties = dict(
    Swap=0,
)

def RequestData():
    from vtk.util import numpy_support as nps
    import numpy as np
    from vtk.numpy_interface import dataset_adapter as dsa
    pdi = self.GetInput() #vtkImageData
    pdo = self.GetOutput() #vtkImageData

    #pdo.DeepCopy(pdi)

    # Input Dimensions:
    [ix,iy,iz] = pdi.GetDimensions()
    [iox, ioy, ioz] = pdi.GetOrigin()
    [isx, isy, isz] = pdi.GetSpacing()

    # Default Sawp (X and Y):
    d1, d2 = 0, 1
    # Default Switch of extents:
    nx, ny, nz = iy, ix, iz
    # Default switch of origin:
    oox, ooy, ooz = ioy, iox, ioz
    # Default switch of spacing:
    osx, osy, osz = isy, isx, isz

    # Determine Swap order
    if Swap == 0:
        # Swap X and Y
        d1, d2 = 1, 0
        nx, ny, nz = iy, ix, iz
        oox, ooy, ooz = ioy, iox, ioz
        osx, osy, osz = isy, isx, isz
    elif Swap == 1:
        # Swap X and Z
        d1, d2 = 1, 2
        nx, ny, nz = iz, iy, ix
        oox, ooy, ooz = ioz, ioy, iox
        osx, osy, osz = isz, isy, isx
    elif Swap == 2:
        # Swap Y and Z
        d1, d2 = 0, 2
        nx, ny, nz = ix, iz, iy
        oox, ooy, ooz = iox, ioz, ioy
        osx, osy, osz = isx, isz, isy
    else:
        raise Exception('Unknown axii swap.')

    pdo.SetDimensions(nx, ny, nz)
    pdo.SetOrigin(oox, ooy, ooz)
    pdo.SetSpacing(osx, osy, osz)
    pdo.SetExtent(0,nx-1, 0,ny-1, 0,nz-1)

    wpdi = dsa.WrapDataObject(pdi)
    narr = pdi.GetPointData().GetNumberOfArrays()

    # TODO: the swap/reshape is not working
    for i in range(narr):
        arr = wpdi.PointData[i]
        arr = np.reshape(arr, (iy,ix,iz))
        arr = np.swapaxes(arr,d1,d2)
        arr = np.reshape(arr, (ix*iy*iz))
        c = nps.numpy_to_vtk(num_array=arr,deep=True)
        c.SetName(pdi.GetPointData().GetArray(i).GetName())
        pdo.GetPointData().AddArray(c)

def RequestInformation():
    from paraview import util
    pdi = self.GetInput() #vtkImageData
    [ix,iy,iz] = pdi.GetDimensions()
    # Determine Swap order
    if Swap == 0:
        nx, ny, nz = iy, ix, iz
    elif Swap == 1:
        nx, ny, nz = iz, iy, ix
    elif Swap == 2:
        nx, ny, nz = ix, iz, iy
    else:
        raise Exception('Unknown axii swap.')
    # ABSOLUTELY NECESSARY FOR THE IMAGEDATA FILTERS TO WORK:
    util.SetOutputWholeExtent(self, [0,nx-1, 0,ny-1, 0,nz-1])
