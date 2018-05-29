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
FileSeries = False

# Any extra XML GUI components you might like:
ExtraXml = ''

# These are the parameters/properties of the plugin:
Properties = dict(
    FileName_Mesh='absolute path',
    FileName_Model='absolute path',
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
    from PVGPpy.read import ubcOcTree
    import os
    # Make sure we have a file combo
    if FileName_Mesh == 'absolute path':
        raise Exception('No mesh file selected. Aborting.')
    if FileName_Model == 'absolute path':
        raise Exception('No model file selected. Aborting.')

    # Get output
    pdo = self.GetOutput()
    # If no name given for data by user, use the basename of the file
    if Data_Name == '':
        Data_Name = os.path.basename(FileName_Model)
    # Read the UBC OcTree gridded data:
    ubcOcTree(FileName_Mesh, FileName_Model, dataNm=Data_Name, pdo=pdo)


def RequestInformation(self):
    from paraview import util
    from PVGPpy.read import ubcExtent
    # Preview the mesh file and get the mesh extents
    ext = ubcExtent(FileName_Mesh)
    # Set the mesh extents
    util.SetOutputWholeExtent(self, ext)
