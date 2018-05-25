Name = 'AddUBCModelToMesh3D'
Label = 'Add UBC Model To Mesh 3D'
FilterCategory = 'PVGP Filters'

# A general overview of the plugin
Help = 'This filter allows you to choose a UBC model file to append as an attribute to an already created vtkRectilinearGrid of a UBC 3D Mesh.'

NumberOfInputs = 1
InputDataType = 'vtkRectilinearGrid'
OutputDataType = 'vtkRectilinearGrid'

# Any extra XML GUI components you might like: (reader extnesions, etc)
ExtraXml = ''

# These are the parameters/properties of the plugin:
Properties = dict(
    FileName_Model='absolute path',
    Data_Name=''
)

def RequestData():
    from PVGPpy.read import ubcModel3D, placeModelOnMesh
    import os

    if FileName_Model == 'absolute path':
        raise Exception('No model file selected. Aborting.')
    if Data_Name == '':
        Data_Name = os.path.basename(FileName_Model)

    pdi = self.GetInput() # vtkRectilinearGrid
    pdo = self.GetOutput() # vtkRectilinearGrid

    pdo.DeepCopy(pdi) # ShallowCopy if you want changes to propagate

    model = ubcModel3D(FileName_Model)
    placeModelOnMesh(pdo, model, dataNm=Data_Name)
