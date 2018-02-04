Name = 'ReadSGeMSFileToUniformGrid'
Label = 'Read SGeMS File To Uniform Grid'
FilterCategory = 'CSM GP Readers'
Help = ''

NumberOfInputs = 0
OutputDataType = 'vtkImageData'
Extensions = 'sgems SGEMS SGeMS dat txt'
ReaderDescription = 'SGeMS Grid File Format'


Properties = dict(
    Delimiter_Field=' ',
    Use_tab_delimiter=False,
    Time_Step=1.0
)

PropertiesHelp = dict(
    Use_Tab_Delimiter='A boolean to override the Delimiter_Field and use Tab delimiter.',
    Time_Step='An advanced property for the time step in seconds.'
)


def RequestData():
    from PVGPpy.read import sgemsGrid, getTimeStepFileIndex

    # This finds the index for the FileNames for the requested timestep
    i = getTimeStepFileIndex(self, FileNames, dt=Time_Step)

    # Generate Output
    pdo = self.GetOutput() # vtkTable
    sgemsGrid(FileNames[i], deli=Delimiter_Field, useTab=Use_tab_delimiter, pdo=pdo)


def RequestInformation():
    from paraview import util
    from PVGPpy.read import sgemsExtent, setOutputTimesteps
    # This is necessary to set time steps
    setOutputTimesteps(self, FileNames, dt=Time_Step)
    ext = sgemsExtent(FileNames[i], deli=Delimiter_Field, useTab=Use_tab_delimiter)
    util.SetOutputWholeExtent(self, ext)
