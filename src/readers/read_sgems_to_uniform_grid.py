Name = 'ReadSGeMSFileToUniformGrid'
Label = 'Read SGeMS File To Uniform Grid'
FilterCategory = 'CSM GP Readers'
Help = ''

NumberOfInputs = 0
OutputDataType = 'vtkImageData'
ExtraXml = '''\
<Hints>
    <ReaderFactory extensions="sgems SGEMS SGeMS dat txt"
                   file_description="SGeMS Grid File Format" />
</Hints>'''


Properties = dict(
    FileName='absolute path',
    Delimiter_Field=' ',
    Use_tab_delimiter=False,
    # TODO: SEPLIB
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

        # Get file header (part of format)
        #header = next(f) # TODO: do something with the header
        #print(os.path.basename(FileName) + ': ' + header)
        h = reader.next()
        n1,n2,n3 = int(h[0]), int(h[1]), int(h[2])

        pdo.SetDimensions(n1, n2, n3)
        pdo.SetExtent(0,n1-1, 0,n2-1, 0,n3-1)


        # Get titles
        numCols = int(next(f))
        for i in range(numCols):
            titles.append(next(f).rstrip('\r\n'))

        # Read data
        for row in reader:
            data.append(row)
        f.close()

    # Put first column into table
    for i in range(numCols):
        col = []
        for row in data:
            col.append(row[i])
        VTK_data = numpy_support.numpy_to_vtk(num_array=col, deep=True, array_type=vtk.VTK_FLOAT)
        VTK_data.SetName(titles[i])
        pdo.GetPointData().AddArray(VTK_data)


def RequestInformation():
    from paraview import util
    import csv
    with open(FileName) as f:
        reader = csv.reader(f, delimiter=Delimiter_Field)
        h = reader.next()
        n1,n2,n3 = int(h[0]), int(h[1]), int(h[2])
        # ABSOLUTELY NECESSARY FOR THE FILTER TO WORK:
        util.SetOutputWholeExtent(self, [0,n1-1, 0,n2-1, 0,n3-1])
        f.close()
