Name = 'ReadPackedBinaryFileToTable'
Label = 'Read Packed Binary File To Table'
FilterCategory = 'CSM GP Readers'
Help = 'This filter reads in float or double data that is packed into a binary file format. It will treat the data as one long array and make a vtkTable with one column of that data. The reader uses big endian and defaults to import as floats. Use the Table to Uniform Grid or the Reshape Table filters to give more meaning to the data. We chose to use a vtkTable object as the output of this reader because it gives us more flexibility in the filters we can apply to this data down the pipeline and keeps thing simple when using filters in this repository.'

NumberOfInputs = 0
OutputDataType = 'vtkTable'
Extensions = 'H@ bin'
ReaderDescription = 'Binary Packed Floats or Doubles'


Properties = dict(
    Data_Name='', # TODO: can I set the default dynamically?
    Double_Values=False
)


def RequestData():
    from PVGPpy.read import packedBinaries
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
    packedBinaries(FileNames[i], dblVals=Double_Values, dataNm=Data_Name, pdo=pdo)


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
