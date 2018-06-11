Name = 'ReverseImageDataAxii'
Label = 'Reverse ImageData Axii'
Help = 'This filter will flip ImageData on any of the three cartesian axii. A checkbox is provided for each axis on which you may desire to flip the data.'

NumberOfInputs = 1
InputDataType = 'vtkImageData'
OutputDataType = 'vtkImageData'
ExtraXml = ''


Properties = dict(
    reverse_x_dir=False,
    reverse_y_dir=False,
    reverse_z_dir=False,
)

PropertiesHelp = dict(
    reverse_x_dir="Reverse all data along the X-axis",
    reverse_y_dir="Reverse all data along the Y-axis",
    reverse_z_dir="Reverse all data along the Z-axis",
)

def RequestData():
    from PVGeo.grids import reverseGridAxii
    pdi = self.GetInput() # vtkImageData
    image = self.GetOutput() # vtkImageData

    # Make user selection iterable
    axes = [reverse_x_dir, reverse_y_dir, reverse_z_dir]

    reverseGridAxii(pdi, axes=axes, pdo=image)
