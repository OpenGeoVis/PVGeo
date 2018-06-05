Name = 'AddUBCModelToMesh'
Label = 'Add UBC Model To Mesh'
FilterCategory = 'PVGP Filters'

# A general overview of the plugin
Help = 'This filter allows you to choose a UBC model file to append as an attribute to an already created vtkRectilinearGrid of a UBC 2D or 3D Mesh.'

NumberOfInputs = 1
InputDataType = 'vtkRectilinearGrid'
OutputDataType = 'vtkRectilinearGrid'

# Handle FileName parameters manually
# NOTE: Mesh needs to be SetParameter while model needs to be AddParameter
ExtraXml = '''
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
    _2D=False,
)

def RequestData():
    from PVGPpy.read import ubcModel3D, ubcModel2D, placeModelOnMesh
    import os

    pdi = self.GetInput() # vtkRectilinearGrid
    pdo = self.GetOutput() # vtkRectilinearGrid

    pdo.DeepCopy(pdi) # ShallowCopy if you want changes to propagate

    if _2D: model = ubcModel2D(FileName_Model)
    else: model = ubcModel3D(FileName_Model)
    # Place read model on the mesh
    placeModelOnMesh(pdo, model)
