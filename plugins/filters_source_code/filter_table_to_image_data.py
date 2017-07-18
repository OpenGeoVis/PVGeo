Name = 'Table To ImageData'
Label = 'Table To ImageData'
Help = 'This filter takes a vtkTable object with columns that represent data to be translated (reshaped) into a 3D grid (2D also works, just set the third dimensions extent to 1). The grid will be a nx by ny by nz structure and an origin can be set at any xyz point. Note that there is an option to choose an array from the input table; this sets which data to treat as the default scalar values. The chosen array should be irrelevant but the feature is left in case some filters down the pipeline do not like having some data not set as a scalar.'

NumberOfInputs = 1
InputDataType = 'vtkTable'
OutputDataType = 'vtkImageData'
ExtraXml = '''\
<Hints>
    <ShowInMenu category="CSM GP Filters" />
</Hints>
<StringVectorProperty name="SelectInputScalars"
                            label="Array"
                            command="SetInputArrayToProcess"
                            number_of_elements="5"
                            element_types="0 0 0 0 2"
                            animateable="0">
        <ArrayListDomain name="array_list"
                         attribute_type="Scalars"
                         input_domain_name="inputs_array">
          <RequiredProperties>
            <Property name="Input"
                      function="Input" />
          </RequiredProperties>
        </ArrayListDomain>
        <FieldDataDomain name="field_list">
          <RequiredProperties>
            <Property name="Input"
                      function="Input" />
          </RequiredProperties>
        </FieldDataDomain>
      </StringVectorProperty>
'''

Properties = dict(
    nx = 1,
    ny = 1,
    nz = 1,
    spacing = 1,
    x_origin = 0,
    y_origin = 0,
    z_origin = 0
    )

def RequestData():
    pdi = self.GetInput()
    image = self.GetOutput() #vtkImageData
    cols = pdi.GetNumberOfColumns()

    # Setup the ImageData
    image.SetDimensions(nx,ny,nz)
    image.SetOrigin(x_origin,y_origin,z_origin)
    image.SetSpacing(spacing,spacing,spacing)
    image.AllocateScalars(vtk.VTK_DOUBLE, cols)
    image.SetExtent(0,nx-1,0,ny-1,0,nz-1)

    # Add all columns of the table as arrays to the PointData
    for i in range(cols):
        c = pdi.GetColumn(i)
        #image.GetCellData().AddArray(c)
        image.GetPointData().AddArray(c) # NOTE: Workaround that could be sketchy. I'm Leaving the ability to set which array is the scalars in case there is trouble down the pipeline.

    # Set scalars from the chosen array in the drop down menu from input table
    name = self.GetInputArrayInformation(0).Get(vtk.vtkDataObject.FIELD_NAME())
    image.GetPointData().SetScalars(pdi.GetColumnByName(name))


def RequestInformation():
    from paraview import util
    # ABSOLUTELY NECESSARY FOR THE FILTER TO WORK:
    util.SetOutputWholeExtent(self, [0,nx-1,0,ny-1,0,nz-1])
