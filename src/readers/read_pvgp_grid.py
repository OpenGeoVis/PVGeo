Name = 'PVGPGridReader'             # Name to be used for coding/macros
Label = 'PVGP Uniform Grid Reader'  # Label for the reader in the menu
FilterCategory = 'CSM GP Readers'   # The source menu category
Extensions = 'pvgp PVGP'
ReaderDescription = 'PVGP Unifrom Grid Reader. Opens a header file which points to data arrays to fill a uniform grid.'
# A general overview of the plugin
Help = ''
NumberOfInputs = 0
OutputDataType = 'vtkImageData'
ExtraXml = ''

# These are the parameters/properties of the plugin:
Properties = dict(
    Time_Step=1.0
)

def RequestData(self):
    from PVGPpy.read import getTimeStepFileIndex, readPVGPGrid
    pdo = self.GetOutput()

    # This finds the index for the FileNames for the requested timestep
    i = getTimeStepFileIndex(self, FileNames, dt=Time_Step)

    readPVGPGrid(FileNames[i], pdo=pdo)


def RequestInformation(self):
    from paraview import util
    from PVGPpy.read import setOutputTimesteps, readPVGPGridExtents
    # This is necessary to set time steps
    setOutputTimesteps(self, FileNames[0], dt=Time_Step)
    # NOTE: if using time series, they all must have the same extents
    ext = readPVGPGridExtents(FileNames[0])
    util.SetOutputWholeExtent(self, ext)
