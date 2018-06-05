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

# Handle FileName parameters manually
# NOTE: Mesh needs to be SetParameter while model needs to be AddParameter
ExtraXml = '''
      <StringVectorProperty
        panel_visibility="default"
        name="FileName_Mesh"
        label="FileName Mesh"
        initial_string="FileName_Mesh"
        command="SetParameter"
        animateable="1"
        clean_command="ClearParameter"
        number_of_elements="1">
        <FileListDomain name="files"/>
        <Documentation>This is the mesh file for a 2D or 3D UBC Mesh grid. This plugin only allows ONE mesh to be defined.</Documentation>
      </StringVectorProperty>

      <StringVectorProperty
        panel_visibility="default"
        name="FileName_Model"
        label="FileName Model"
        initial_string="FileName_Model"
        command="AddParameter"
        animateable="1"
        repeat_command="1"
        clean_command="ClearParameter"
        number_of_elements="1">
        <FileListDomain name="files"/>
        <Documentation>These are the model files to append to the mesh as data attributes. You can chose as many files as you would like for this.</Documentation>
      </StringVectorProperty>
'''

# These are the parameters/properties of the plugin:
Properties = dict(
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
    # Get output
    pdo = self.GetOutput()
    # Read the UBC OcTree gridded data:
    try:
        ubcOcTree(FileName_Mesh, FileName_Model, pdo=pdo)
    except NameError:
        ubcOcTree(FileName_Mesh, None, pdo=pdo)


def RequestInformation(self):
    from paraview import util
    from PVGPpy.read import ubcExtent
    # Preview the mesh file and get the mesh extents
    ext = ubcExtent(FileName_Mesh)
    # Set the mesh extents
    util.SetOutputWholeExtent(self, ext)
