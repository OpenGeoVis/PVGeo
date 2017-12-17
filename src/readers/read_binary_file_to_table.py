Name = 'ReadPackedBinaryFileToTable'
Label = 'Read Packed Binary File To Table'
FilterCategory = 'CSM GP Readers'
Help = 'This filter reads in float or double data that is packed into a binary file format. It will treat the data as one long array and make a vtkTable with one column of that data. The reader uses big endian and defaults to import as floats. Use the Table to Uniform Grid or the Reshape Table filters to give more meaning to the data. We chose to use a vtkTable object as the output of this reader because it gives us more flexibility in the filters we can apply to this data down the pipeline and keeps thing simple when using filters in this repository.'

NumberOfInputs = 0
OutputDataType = 'vtkTable'
Extensions = 'H@ bin'
ReaderDescription = 'Binary Packed Floats or Doubles'


Properties = dict(
    FileName='absolute path',
    data_name='', # TODO: can I set the default dynamically?
    double_values=False
)


def RequestData():
    from PVGPpy.read import readPackedBinaries
    pdo = self.GetOutput()
    tbl = readPackedBinaries(FileName, dblVals=double_values, dataNm=data_name)
    pdo.ShallowCopy(tbl)
