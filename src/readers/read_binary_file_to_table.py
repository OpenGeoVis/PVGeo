Name = 'ReadPackedBinaryFileToTable'
Label = 'Read Packed Binary File To Table'
FilterCategory = 'CSM GP Readers'
Help = 'This filter reads in float or double data that is packed into a binary file format. It will treat the data as one long array and make a vtkTable with one column of that data. The reader uses big endian and defaults to import as floats. Use the Table to Uniform Grid or the Reshape Table filters to give more meaning to the data. We chose to use a vtkTable object as the output of this reader because it gives us more flexibility in the filters we can apply to this data down the pipeline and keeps thing simple when using filters in this repository.'

NumberOfInputs = 0
OutputDataType = 'vtkTable'
Extensions = 'H@ bin'
ReaderDescription = 'Binary Packed Floats or Doubles'


Properties = dict(
    Data_Name='values',
    Double_Values=False,
    Time_Step=1.0
)

PropertiesHelp = dict(
    Data_Name='The string name of the data array generated from the inut file.',
    Time_Step='An advanced property for the time step in seconds.'
)


def RequestData():
    from PVGPpy.read import packedBinaries, getTimeStepFileIndex

    # This finds the index for the FileNames for the requested timestep
    i = getTimeStepFileIndex(self, FileNames, dt=Time_Step)

    # Generate Output
    pdo = self.GetOutput()
    packedBinaries(FileNames[i], dblVals=Double_Values, dataNm=Data_Name, pdo=pdo)


def RequestInformation(self):
    from PVGPpy.read import setOutputTimesteps
    # This is necessary to set time steps
    setOutputTimesteps(self, FileNames, dt=Time_Step)
