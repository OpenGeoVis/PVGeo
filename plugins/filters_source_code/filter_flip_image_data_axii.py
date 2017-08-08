Name = 'FlipImageDataAxii'
Label = 'Flip ImageData Axii'
Help = 'This filter will flip ImageData in any of the three cartesian coordinates.'

NumberOfInputs = 1
InputDataType = 'vtkImageData'
OutputDataType = 'vtkImageData'
ExtraXml = '''\
<Hints>
    <ShowInMenu category="CSM Geophysics Filters" />
</Hints>'''


Properties = dict(
    reverse_x_dir=False,
    reverse_y_dir=False,
    reverse_z_dir=False,
)


def RequestData():
    pdi = self.GetInput() # vtkImageData
    image = self.GetOutput() # vtkImageData

    # Make user selection iterable
    dirs = [reverse_x_dir, reverse_y_dir, reverse_z_dir]

    # Copy over input to output to be flipped around
    # Deep copy keeps us from messing with the input data
    image.DeepCopy(pdi)

    # Iterate over all array in the PointData
    for j in range(image.GetPointData().GetNumberOfArrays()):
        # Swap Scalars with all Arrays in PointData so that all data gets filtered
        scal = image.GetPointData().GetScalars()
        arr = pdi.GetPointData().GetArray(j)
        image.GetPointData().SetScalars(arr)
        image.GetPointData().AddArray(scal)
        for i in range(3):
            # Rotate ImageData on each axis if needed
            # Go through each axis and rotate if needed
            # Note: ShallowCopy is necessary!!
            if dirs[i]:
                flipper = vtk.vtkImageFlip()
                flipper.SetInputData(image)
                flipper.SetFilteredAxis(i)
                flipper.Update()
                flipper.UpdateWholeExtent()
                image.ShallowCopy(flipper.GetOutput())
