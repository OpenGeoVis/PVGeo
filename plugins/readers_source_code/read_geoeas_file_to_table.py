Name = 'Read GEO EAS File To Table'
Label = 'Read GEO EAS File To Table'
Help = 'Help'

NumberOfInputs = 0
OutputDataType = 'vtkTable'
ExtraXml = '''\
<Hints>
    <ShowInMenu category="CSM GP Readers" />
    <ReaderFactory extensions="dat geoeas txt"
                   file_description="GEO EAS File Format" />
</Hints>'''


Properties = dict(
    FileName='absolute path',
    Number_Ignore_Lines=0,
    Delimiter_Field=' '
)


def RequestData():
    import numpy as np
    import csv
    from vtk.util import numpy_support

    pdo = self.GetOutput() # vtkTable

    titles = []
    data = []
    with open(FileName) as f:
        reader = csv.reader(f, delimiter=Delimiter_Field)
        # Skip defined lines
        for i in range(Number_Ignore_Lines):
            next(f)

        # Get file header (part of format)
        header = next(f) # TODO: do something with the header
        print('File Header: ' + header)
        # Get titles
        numCols = int(next(f))
        for i in range(numCols):
            titles.append(next(f).rstrip('\r\n'))

        # Read data
        for row in reader:
            data.append(row)

    # Put first column into table
    for i in range(len(titles)):
        col = []
        for row in data:
            col.append(row[i])
        VTK_data = numpy_support.numpy_to_vtk(num_array=col, deep=True, array_type=vtk.VTK_FLOAT)
        VTK_data.SetName(titles[i])
        pdo.AddColumn(VTK_data)
