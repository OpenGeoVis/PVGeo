Name = 'ReadDelimitedTextFileToTable'
Label = 'Read Delimited Text File To Table'
FilterCategory = 'CSM GP Readers'
Help = 'This reader will take in any delimited text file and make a vtkTable from it. This is not much different than the default .txt or .csv reader in Paraview, however it gives us room to use our own extensions and a little more flexibility in the structure of the files we import.'

NumberOfInputs = 0
OutputDataType = 'vtkTable'
Extensions = 'dat csv txt'
ReaderDescription = 'CSM GP Delimited Text File'


Properties = dict(
    Number_Ignore_Lines=0,
    Has_Titles=True,
    Delimiter_Field=' ',
    Use_Tab_Delimiter=False
)

def RequestData():
    from PVGPpy.read import delimitedText
    import numpy as np

    def GetUpdateTimestep(algorithm):
        """Returns the requested time value, or None if not present"""
        executive = algorithm.GetExecutive()
        outInfo = executive.GetOutputInformation(0)
        if outInfo.Has(executive.UPDATE_TIME_STEP()):
            return outInfo.Get(executive.UPDATE_TIME_STEP())
        else:
            return None
    # Get the current timestep
    req_time = GetUpdateTimestep(self)
    # Read the closest file
    #np.asarray([get_time(file) for file in FileNames])
    xtime = np.arange(len(FileNames), dtype=float)
    i = np.argwhere(xtime == req_time)

    # Generate Output
    pdo = self.GetOutput()
    delimitedText(FileNames[i], deli=Delimiter_Field, useTab=Use_Tab_Delimiter, hasTits=Has_Titles, numIgLns=Number_Ignore_Lines, pdo=pdo)

def RequestInformation(self):
    def setOutputTimesteps(algorithm):
        executive = algorithm.GetExecutive()
        outInfo = executive.GetOutputInformation(0)
        # Calculate list of timesteps here
        #np.asarray([get_time(file) for file in FileNames])
        xtime = range(len(FileNames))
        outInfo.Remove(executive.TIME_STEPS())
        for i in range(len(FileNames)):
            outInfo.Append(executive.TIME_STEPS(), xtime[i])
        # Remove and set time range info
        outInfo.Remove(executive.TIME_RANGE())
        outInfo.Append(executive.TIME_RANGE(), xtime[0])
        outInfo.Append(executive.TIME_RANGE(), xtime[-1])

    setOutputTimesteps(self)
