"""
@author: Bane Sullivan
"""
Name = 'ReadOcTreeMesh' # Name to be used for coding/macros
Label = 'Read OcTree Mesh' # Label for the reader in the menu
FilterCategory = 'PVGP Readers' # The source menu category
Extensions = 'mesh msh dat txt'
ReaderDescription = 'PVGP: UBC OcTree Mesh File Format.'
# A general overview of the plugin
Help = 'TODO'

NumberOfInputs = 0
OutputDataType = 'vtkUnstructuredGrid'

# Any extra XML GUI components you might like:
ExtraXml = ''

# These are the parameters/properties of the plugin:
Properties = dict(
    Data_Name='',
    Time_Step=1.0
)

# This is the description for each of the properties variable:
#- Include if you'd like. Totally optional.
#- The variable name (key) must be identical to the property described.
PropertiesHelp = dict(
)

# from paraview import vtk is done automatically in the reader
def RequestData(self):
    from PVGPpy.read import getTimeStepFileIndex
    from PVGPpy.read import ubcOcTree
    import os
    # This finds the index for the FileNames for the requested timestep
    i = getTimeStepFileIndex(self, FileNames, dt=Time_Step)

    # Get output
    pdo = self.GetOutput()
    # If no name given for data by user, use the basename of the file
    if Data_Name == '':
        Data_Name = os.path.basename(FileNames[0]) # use first file in series so representation/cmap does not change.
    # Read the UBC OcTree gridded data:
    ubcOcTree(FileNames[i], dataNm=Data_Name, pdo=pdo)


def RequestInformation(self):
    from paraview import util
    from PVGPpy.read import setOutputTimesteps, getTimeStepFileIndex
    from PVGPpy.read import ubcExtent
    # This is necessary to set time steps
    setOutputTimesteps(self, FileNames, dt=Time_Step)
    i = getTimeStepFileIndex(self, FileNames, dt=Time_Step)
    # Preview the mesh file and get the mesh extents
    ext = ubcExtent(FileNames[i])
    # Set the mesh extents
    util.SetOutputWholeExtent(self, ext)
