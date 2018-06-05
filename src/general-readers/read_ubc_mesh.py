Name = 'ReadUBCMesh'
Label = 'Read UBC Mesh 2D/3D Two-File Format'
FilterCategory = 'PVGP Readers'
Help = 'UBC Mesh 2D/3D models are defined using a 2-file format. The "mesh" file describes how the data is discretized. The "model" file lists the physical property values for all cells in a mesh. A model file is meaningless without an associated mesh file. The reader will automatically detect if the mesh is 2D or 3D and read the remainder of the data with that dimensionality assumption. If the mesh file is 2D, then then model file must also be in the 2D format (same for 3D).'

NumberOfInputs = 0
OutputDataType = 'vtkRectilinearGrid'
Extensions = 'mesh msh dat txt'
ReaderDescription = 'PVGP: UBC Mesh 2D/3D Two-File Format'
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

Properties = dict(
)


def RequestData():
    from PVGPpy.read import ubcTensorMesh
    import os
    # Get output
    pdo = self.GetOutput()
    # Read the UBC Mesh gridded data:
    ubcTensorMesh(FileName_Mesh, FileName_Model, pdo=pdo)

def RequestInformation():
    from paraview import util
    from PVGPpy.read import ubcExtent
    if FileName_Mesh == 'absolute path':
        raise Exception('No mesh file selected. Aborting.')
    # Preview the mesh file and get the mesh extents
    ext = ubcExtent(FileName_Mesh)
    # Set the mesh extents
    util.SetOutputWholeExtent(self, ext)
