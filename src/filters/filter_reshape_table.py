Name = 'ReshapeTable'
Label = 'Reshape Table'
FilterCategory = 'CSM GP Filters'
Help = 'This filter will take a vtkTable object and reshape it. This filter essentially treats vtkTables as 2D matrices and reshapes them using numpy.reshape in a C contiguous manner. Unfortunately, data fields will be renamed arbitrarily because VTK data arrays require a name.'

NumberOfInputs = 1
InputDataType = 'vtkTable'
OutputDataType = 'vtkTable'
ExtraXml = ''


Properties = dict(
    ncols=6,
    nrows=126,
    #Fortran_Ordering=False # TODO: Fortran_Ordering
)


def RequestData():
    from PVGPpy.filt import reshapeTable

    pdi = self.GetInput() #vtkTable
    pdo = self.GetOutput() #vtkTable

    reshapeTable(pdi, nrows, ncols, pdo=pdo)
