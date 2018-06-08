Name = 'ReadGSLIBFileToTable'
Label = 'Read GSLIB File To Table'
Help = 'The GSLIB file format has headers lines followed by the data as a space delimited ASCI file (this filter is set up to allow you to choose any single character delimiter). The first header line is the title and will be printed to the console. This line may have the dimensions for a grid to be made of the data. The second line is the number (n) of columns of data. The next n lines are the variable names for the data in each column. You are allowed up to ten characters for the variable name. The data follow with a space between each field (column).'

NumberOfInputs = 0
OutputDataType = 'vtkTable'
Extensions = 'sgems dat geoeas gslib GSLIB txt SGEMS'
ReaderDescription = 'PVGP: GSLIB File Format'


Properties = dict(
    Skiprows=0,
    Delimiter_Field=' ',
    Use_Tab_Delimiter=False,
    Comments='#',
    Time_Step=1.0
)

PropertiesHelp = dict(
    Skiprows='The integer number of rows to skip at the top of the file',
    Delimiter_Field="The input file's delimiter. To use a tab delimiter please set the Use_Tab_Delimiter parameter.",
    Use_Tab_Delimiter='A boolean to override the Delimiter_Field and use Tab delimiter.',
    Comments='The identifier for comments within the file.',
    Time_Step='An advanced property for the time step in seconds.'
)


def RequestData():
    import os
    from PVGPpy.read import gslib, getTimeStepFileIndex

    # This finds the index for the FileNames for the requested timestep
    i = getTimeStepFileIndex(self, FileNames, dt=Time_Step)

    # Generate Output, use: print(os.path.basename(FileNames[i]) + ': ' + h)
    pdo = self.GetOutput() # vtkTable
    tbl, h = gslib(FileNames[i], deli=Delimiter_Field, useTab=Use_Tab_Delimiter, skiprows=Skiprows, comments=Comments, pdo=pdo)

def RequestInformation(self):
    from PVGPpy.read import setOutputTimesteps
    # This is necessary to set time steps
    setOutputTimesteps(self, FileNames, dt=Time_Step)
