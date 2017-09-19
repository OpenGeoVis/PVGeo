Name = 'GenerateGridFromPoints'
Label = 'Generate Grid From Points'
Help = ''

NumberOfInputs = 1
InputDataType = 'vtkPolyData'
OutputDataType = 'vtkImageData'
ExtraXml = '''\
<Hints>
    <ShowInMenu category="CSM Geophysics Filters DEV" />
</Hints>
'''

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
    pdi = self.GetInput()
    pdo = self.GetOutput()
    scal = pdi.GetPointData().GetArray('p')
    pdi.GetPointData().SetScalars(scal)


    shepard1 = vtk.vtkShepardMethod()
    shepard1.SetInputData(pdi)
    shepard1.SetModelBounds(797006.000000,805506.000000,9196651.000000,9206651.000000,-1184.000000,1900.000000)
    #shepard1.SetSampleDimensions(42,58,20)
    #shepard1.SetNullValue(0)
    #shepard1.SetMaximumDistance(1)
    #shepard1.SetPowerParameter(1)

    shepard1.Update()
    pdo = shepard1.GetOutput()
    #print(type(shepard1.GetOutput()))


def RequestInformation():
    from paraview import util
    # ABSOLUTELY NECESSARY FOR THE FILTER TO WORK:
    util.SetOutputWholeExtent(self, [0,nx-1, 0,ny-1, 0,nz-1])
