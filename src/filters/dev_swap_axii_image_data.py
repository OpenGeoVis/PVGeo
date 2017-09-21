Name = 'SwapAxiiImageData'
Label = 'Swap Axii Image Data'
FilterCategory = 'CSM Geophysics Filters DEV'
Help = ''

NumberOfInputs = 1
InputDataType = 'vtkImageData'
OutputDataType = 'vtkImageData'
ExtraXml = '''\
<IntVectorProperty
    name="Axii"
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
    Axii=0,
)

def RequestData():
    pdi = self.GetInput()
    pdo = self.GetOutput() #vtkImageData

    [nx,ny,nz] = pdi.GetDimensions()

    print(Axii)

    # Grab Data values
    # Put into 3D structure
    # Swap axis in that structure
    # unfold
    # convert to VTK arrays
    # set name accordingly
    # add array to pdo


def RequestInformation():
    from paraview import util
    # ABSOLUTELY NECESSARY FOR THE FILTER TO WORK:
    pdi = self.GetInput()
    [nx,ny,nz] = pdi.GetDimensions()
    util.SetOutputWholeExtent(self, [0,nx-1, 0,ny-1, 0,nz-1])
