Name = 'ReadDelimitedTextFileToTable'
Label = 'Read Delimited Text File To Table'
Help = 'This reader will take in any delimited text file and make a vtkTable from it. This is not much different than the default .txt or .csv reader in Paraview, however it gives us room to use our own extensions and a little more flexibility in the structure of the files we import.'

NumberOfInputs = 0
OutputDataType = 'vtkTable'
Extensions = 'dat csv txt text ascii'
ReaderDescription = 'PVGeo: Delimited Text File'


Properties = dict(
    Skiprows=0,
    Has_Titles=True,
    Delimiter_Field=' ',
    Use_Tab_Delimiter=False,
    Comments='#',
    Time_Step=1.0
)

PropertiesHelp = dict(
    Skiprows='The integer number of rows to skip at the top of the file',
    Has_Titles='A boolean for if the delimited file has header titles for the data arrays.',
    Delimiter_Field="The input file's delimiter. To use a tab delimiter please set the Use_Tab_Delimiter parameter.",
    Use_Tab_Delimiter='A boolean to override the Delimiter_Field and use a Tab delimiter.',
    Comments='The identifier for comments within the file.',
    Time_Step='An advanced property for the time step in seconds.'
)

def RequestData():
    from PVGeo.readers_general import delimitedText
    from PVGeo._helpers import getTimeStepFileIndex

    # This finds the index for the FileNames for the requested timestep
    i = getTimeStepFileIndex(self, FileNames, dt=Time_Step)

    # Generate Output
    pdo = self.GetOutput()
    delimitedText(FileNames[i], deli=Delimiter_Field, useTab=Use_Tab_Delimiter, hasTits=Has_Titles, skiprows=Skiprows, comments=Comments, pdo=pdo)

def RequestInformation(self):
    from PVGeo._helpers import setOutputTimesteps
    # This is necessary to set time steps
    setOutputTimesteps(self, FileNames, dt=Time_Step)
