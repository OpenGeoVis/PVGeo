Name = 'ReadUBCMesh'
Label = 'Read UBC Mesh Two-File Format'
FilterCategory = 'CSM GP Readers'
Help = ''

NumberOfInputs = 0
OutputDataType = 'vtkRectilinearGrid'
ExtraXml = '''\
<Hints>
    <ReaderFactory extensions="mesh msh dat"
                   file_description="UBC Mesh Two-File Format" />
</Hints>'''


Properties = dict(
    FileName_Mesh='absolute path',
    FileName_Data='absolute path',
    Delimiter_Field=' ',
    Use_tab_delimiter=False
)


def RequestData():
    import numpy as np
    import csv
    import os
    from vtk.util import numpy_support

    if FileName_Mesh == 'absolute path':
        raise Exception('No mesh file selected. Aborting.')
    if FileName_Data == 'absolute path':
        raise Exception('No data file selected. Aborting.')

    pdo = self.GetOutput() # vtkTable

    if (Use_tab_delimiter):
        Delimiter_Field = '\t'

    # Read in the data


def RequestInformation():
    from paraview import util
    import csv

    if FileName_Mesh == 'absolute path':
        raise Exception('No mesh file selected. Aborting.')
    # Read in the mesh
    with open(FileName_Mesh) as f:
        reader = csv.reader(f, delimiter=Delimiter_Field)
        f.close()
