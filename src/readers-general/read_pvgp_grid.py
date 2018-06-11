Name = 'ReadPVGPGrid'             # Name to be used for coding/macros
Label = 'Read PVGP Uniform Grid'  # Label for the reader in the menu
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
    import os
    from PVGeo.grids import readPVGPGrid
    from PVGeo._helpers import getTimeStepFileIndex
    pdo = self.GetOutput()

    # This finds the index for the FileNames for the requested timestep
    i = getTimeStepFileIndex(self, FileNames, dt=Time_Step)
    path = os.path.dirname(FileNames[i])

    readPVGPGrid(FileNames[i], pdo=pdo, path=path)


def RequestInformation(self):
    from paraview import util
    from PVGeo._helpers import setOutputTimesteps
    from PVGeo.grids import readPVGPGridExtents
    # This is necessary to set time steps
    setOutputTimesteps(self, FileNames[0], dt=Time_Step)
    # NOTE: if using time series, they all must have the same extents
    ext = readPVGPGridExtents(FileNames[0])
    util.SetOutputWholeExtent(self, ext)
