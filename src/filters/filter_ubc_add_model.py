Name = 'AddUBCModelToMesh'
Label = 'Add UBC Model To Mesh'
FilterCategory = 'CSM GP Filters'

# A general overview of the plugin
Help = 'This filter allows you to choose a UBC model file to append as an attribute to an already created vtkRectilinearGrid of a UBC Mesh.'

NumberOfInputs = 1
InputDataType = 'vtkRectilinearGrid'
OutputDataType = 'vtkRectilinearGrid'

# Any extra XML GUI components you might like: (reader extnesions, etc)
ExtraXml = ''

# These are the parameters/properties of the plugin:
Properties = dict(
    FileName_Model='absolute path',
    Data_Name='',
    Delimiter_Field=' ',
    Use_Tab_Delimiter=False
)



def RequestData():
    from PVGPpy.read import ubcModel, placeModelOnMesh
    import os

    if FileName_Model == 'absolute path':
        raise Exception('No model file selected. Aborting.')
    if Data_Name == '':
        Data_Name = os.path.basename(FileName_Model)

    pdi = self.GetInput() # vtkRectilinearGrid
    pdo = self.GetOutput() # vtkRectilinearGrid

    pdo.DeepCopy(pdi) # ShallowCopy if you want changes to propagate

    model = ubcModel(FileName_Model, deli=Delimiter_Field, useTab=Use_Tab_Delimiter)
    placeModelOnMesh(pdo, model, dataNm=Data_Name)
