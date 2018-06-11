Name = 'ReadSGeMSFileToUniformGrid'
Label = 'Read SGeMS File To Uniform Grid'
Help = 'NOTE: if reading a time series, they must all have the same extent!'

NumberOfInputs = 0
OutputDataType = 'vtkImageData'
Extensions = 'sgems SGEMS SGeMS dat txt'
ReaderDescription = 'PVGP: SGeMS Grid File Format'


Properties = dict(
    Skiprows=0,
    Delimiter_Field=' ',
    Use_tab_delimiter=False,
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
    from PVGeo.gslib import sgemsGrid
    from PVGeo._helpers import getTimeStepFileIndex
    from paraview import util

    # This finds the index for the FileNames for the requested timestep
    i = getTimeStepFileIndex(self, FileNames, dt=Time_Step)

    # Generate Output
    pdo = self.GetOutput() # vtkTable
    sgemsGrid(FileNames[i], deli=Delimiter_Field, useTab=Use_tab_delimiter, skiprows=Skiprows, comments=Comments, pdo=pdo)


def RequestInformation():
    from paraview import util
    from PVGeo.gslib import sgemsExtent
    from PVGeo._helpers import setOutputTimesteps, getTimeStepFileIndex
    # This is necessary to set time steps
    setOutputTimesteps(self, FileNames, dt=Time_Step)
    # Only grab extent for first file... requires all to have same extent
    ext = sgemsExtent(FileNames[0], deli=Delimiter_Field, useTab=Use_tab_delimiter)
    util.SetOutputWholeExtent(self, ext)
