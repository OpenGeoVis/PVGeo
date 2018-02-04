Name = 'ReadUBCMesh'
Label = 'Read UBC Mesh Two-File Format'
FilterCategory = 'CSM GP Readers'
Help = 'UBC Mesh 3D models are defined using a 2-file format. The "mesh" file describes how the data is descritized. The "model" file lists the physical property values for all cells in a mesh. A model file is meaningless without an associated mesh file. Default file delimiter is a space character.'

NumberOfInputs = 0
OutputDataType = 'vtkRectilinearGrid'
Extensions = 'mesh msh dat'
ReaderDescription = 'UBC Mesh Two-File Format'

# TODO: implement FileNames to work with time series
Properties = dict(
    FileName_Mesh='absolute path',
    FileName_Model='absolute path',
    Data_Name='',
    Delimiter_Field=' ',
    Use_Tab_Delimiter=False
)


def RequestData():
    from PVGPpy.read import ubcGridData
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
    # Read the UBC Mesh gridded data:
    ubcGridData(FileName_Mesh, FileName_Model, deli=Delimiter_Field, useTab=Use_Tab_Delimiter, dataNm=Data_Name, pdo=pdo)

def RequestInformation():
    from paraview import util
    from PVGPpy.read import ubcMeshExtnet
    if FileName_Mesh == 'absolute path':
        raise Exception('No mesh file selected. Aborting.')
    # Preview the mesh file and get the mesh extents
    ext = ubcMeshExtnet(FileName_Mesh, deli=Delimiter_Field, useTab=Use_Tab_Delimiter)
    # Set the mesh extents
    util.SetOutputWholeExtent(self, ext)
