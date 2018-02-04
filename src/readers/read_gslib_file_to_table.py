Name = 'ReadGSLIBFileToTable'
Label = 'Read GSLIB File To Table'
FilterCategory = 'CSM GP Readers'
Help = 'The GSLIB file format has headers lines followed by the data as a space delimited ASCI file (this filter is set up to allow you to choose any single character delimiter). The first header line is the title and will be printed to the console. This line may have the dimensions for a grid to be made of the data. The second line is the number (n) of columns of data. The next n lines are the variable names for the data in each column. You are allowed up to ten characters for the variable name. The data follow with a space between each field (column).'

NumberOfInputs = 0
OutputDataType = 'vtkTable'
Extensions = 'sgems dat geoeas gslib GSLIB txt SGEMS'
ReaderDescription = 'GSLIB File Format'


Properties = dict(
    Number_Ignore_Lines=0,
    Delimiter_Field=' ',
    Use_Tab_Delimiter=False
)


def RequestData():
    import os
    from PVGPpy.read import gslib
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
    pdo = self.GetOutput() # vtkTable
    tbl, h = gslib(FileNames[i], deli=Delimiter_Field, useTab=Use_Tab_Delimiter, numIgLns=Number_Ignore_Lines, pdo=pdo)
    #print(os.path.basename(FileNames[i]) + ': ' + h)

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
