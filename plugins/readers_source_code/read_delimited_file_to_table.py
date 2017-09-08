Name = 'ReadDelimitedTextFileToTable'
Label = 'Read Delimited Text File To Table'
Help = 'This reader will take in any delimited text file and make a vtkTable from it. This is not much different than the default .txt or .csv reader in Paraview, however it gives us room to use our own extensions and a little more flexibility in the structure of the files we import.'

NumberOfInputs = 0
OutputDataType = 'vtkTable'
ExtraXml = '''\
<Hints>
    <ShowInMenu category="CSM GP Readers" />
    <ReaderFactory extensions="dat csv txt"
                   file_description="CSM GP Delimited Text File" />
</Hints>'''


Properties = dict(
    FileName='absolute_path',
    Number_Ignore_Lines=0,
    Has_Titles=True,
    Delimiter_Field=' ',
    Use_tab_delimiter=False
)

def RequestData():
    import numpy as np
    import csv
    from vtk.util import numpy_support

    pdo = self.GetOutput() # vtkTable

    if (Use_tab_delimiter):
        Delimiter_Field = '\t'

    titles = []
    data = []
    with open(FileName) as f:
        reader = csv.reader(f, delimiter=Delimiter_Field)
        # Skip header lines
        for i in range(Number_Ignore_Lines):
            reader.next()
        # Get titles
        if (Has_Titles):
            titles = reader.next()
        else:
            # Bulild arbitrary titles for length of first row
            row = reader.next()
            data.append(row)
            for i in range(len(row)):
                titles.append('Field' + str(i))
        # Read data
        for row in reader:
            data.append(row)

    # Put columns into table
    for i in range(len(titles)):
        col = []
        for row in data:
            col.append(row[i])
        VTK_data = numpy_support.numpy_to_vtk(num_array=col, deep=True, array_type=vtk.VTK_FLOAT)
        VTK_data.SetName(titles[i])
        pdo.AddColumn(VTK_data)
