Name = 'ReadDelimitedTextFileToTable'
Label = 'Read Delimited Text File To Table'
Help = 'This reader will take in any delimited text file and make a vtkTable from it. This is not much different than the default .txt or .csv reader in Paraview, however it gives us room to use our own extensions and a little more flexibility in the structure of the files we import.'

NumberOfInputs = 0
OutputDataType = 'vtkTable'
Extensions = 'dat csv txt'
ReaderDescription = 'PVGP: Delimited Text File'


Properties = dict(
    Number_Ignore_Lines=0,
    Has_Titles=True,
    Delimiter_Field=' ',
    Use_Tab_Delimiter=False,
    Time_Step=1.0
)

PropertiesHelp = dict(
    Use_Tab_Delimiter='A boolean to override the Delimiter_Field and use Tab delimiter.',
    Time_Step='An advanced property for the time step in seconds.'
)

def RequestData():
    from PVGPpy.read import delimitedText, getTimeStepFileIndex

    # This finds the index for the FileNames for the requested timestep
    i = getTimeStepFileIndex(self, FileNames, dt=Time_Step)

    # Generate Output
    pdo = self.GetOutput()
    delimitedText(FileNames[i], deli=Delimiter_Field, useTab=Use_Tab_Delimiter, hasTits=Has_Titles, numIgLns=Number_Ignore_Lines, pdo=pdo)

def RequestInformation(self):
    from PVGPpy.read import setOutputTimesteps
    # This is necessary to set time steps
    setOutputTimesteps(self, FileNames, dt=Time_Step)
