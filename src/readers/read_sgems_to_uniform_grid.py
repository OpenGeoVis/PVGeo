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
    # TODO: SEPLIB
)


def RequestData():
    from PVGPpy.read import sgemsGrid
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
    sgemsGrid(FileNames[i], deli=Delimiter_Field, useTab=Use_tab_delimiter, pdo=pdo)


def RequestInformation():
    from paraview import util
    from PVGPpy.read import sgemsExtent

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

    ext = sgemsExtent(FileNames[i], deli=Delimiter_Field, useTab=Use_tab_delimiter)
    util.SetOutputWholeExtent(self, ext)
    setOutputTimesteps(self)
