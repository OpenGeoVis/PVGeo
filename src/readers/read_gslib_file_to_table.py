Name = 'ReadGSLIBFileToTable'
Label = 'Read GSLIB File To Table'
FilterCategory = 'CSM GP Readers'
Help = 'The GSLIB file format has headers lines followed by the data as a space delimited ASCI file (this filter is set up to allow you to choose any single character delimiter). The first header line is the title and will be printed to the console. This line may have the dimensions for a grid to be made of the data. The second line is the number (n) of columns of data. The next n lines are the variable names for the data in each column. You are allowed up to ten characters for the variable name. The data follow with a space between each field (column).'

NumberOfInputs = 0
OutputDataType = 'vtkTable'
Extensions = 'sgems dat geoeas gslib GSLIB txt SGEMS'
ReaderDescription = 'GSLIB File Format'


Properties = dict(
    FileName='absolute path',
    Number_Ignore_Lines=0,
    Delimiter_Field=' ',
    Use_tab_delimiter=False
)


def RequestData():
    import numpy as np
    import csv
    import os
    from vtk.util import numpy_support

    pdo = self.GetOutput() # vtkTable

    if (Use_tab_delimiter):
        Delimiter_Field = '\t'

    titles = []
    data = []
    with open(FileName) as f:
        reader = csv.reader(f, delimiter=Delimiter_Field)
        # Skip defined lines
        for i in range(Number_Ignore_Lines):
            next(f)

        # Get file header (part of format)
        header = next(f) # TODO: do something with the header
        print(os.path.basename(FileName) + ': ' + header)
        # Get titles
        numCols = int(next(f))
        for i in range(numCols):
            titles.append(next(f).rstrip('\r\n'))

        # Read data
        for row in reader:
            data.append(row)

    # Put first column into table
    for i in range(numCols):
        col = []
        for row in data:
            col.append(row[i])
        VTK_data = numpy_support.numpy_to_vtk(num_array=col, deep=True, array_type=vtk.VTK_FLOAT)
        VTK_data.SetName(titles[i])
        pdo.AddColumn(VTK_data)
