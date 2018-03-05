Name = 'PVGPGridReader'        # Name to be used for coding/macros
Label = 'PVGPGridReader'     # Label for the reader in the menu
FilterCategory = 'CSM GP Readers'   # The source menu category

Extensions = 'pvgp'
ReaderDescription = 'PVGP Unifrom Grid Format'

# A general overview of the plugin
Help = ''

NumberOfInputs = 0                          # Specify zero for readers
# No input data type
OutputDataType = 'vtkImageData'      # NEED to specify

# Any extra XML GUI components you might like:
ExtraXml = ''

# These are the parameters/properties of the plugin:
Properties = dict(
    Time_Step=1.0
)

# This is the description for each of the properties variable:
#- Include if you'd like. Totally optional.
#- The variable name (key) must be identical to the property described.
#PropertiesHelp = dict()

# from paraview import vtk is done automatically in the reader
def RequestData(self):
    """Create a VTK output given the list of FileNames and the current timestep.
    This script can access self and FileNames and should return an output of type
    OutputDataType defined above"""
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
    ext = readPVGPGridExtents(FileNames[0])
    util.SetOutputWholeExtent(self, ext)
