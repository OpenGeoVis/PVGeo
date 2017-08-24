Name = 'ReadPackedBinaryFileToTable'
Label = 'Read Packed Binary File To Table'
Help = 'This filter reads in float data that is packed into a binary file fomrat. It will treat the data as one long array and make a vtkTable with one column of that data. The reader uses big endian. Use the Table to ImageData filter to reshape the data.'

NumberOfInputs = 0
OutputDataType = 'vtkTable'
ExtraXml = '''\
<Hints>
    <ShowInMenu category="CSM GP Readers" />
    <ReaderFactory extensions="H@ bin"
                   file_description="Binary Packed Floats or Doubles" />
</Hints>'''


Properties = dict(
    FileName='absolute path',
    data_name='', # TODO: can I set the default dynamically?
    double_values=False
)


def RequestData():
    import struct
    import os
    from vtk.util import numpy_support as nps

    pdo = self.GetOutput() # vtkTable

    num_bytes = 4 # FLOAT
    if double_values:
        num_bytes = 8 # DOUBLE

    tn = os.stat(FileName).st_size / num_bytes
    tn_string = str(tn)
    raw = []
    with open(FileName, 'rb') as file:
        # Unpack by num_bytes
        raw = struct.unpack('>'+tn_string+'f', file.read(num_bytes*tn))

    # Put raw data into vtk array
    data = nps.numpy_to_vtk(num_array=raw, deep=True, array_type=vtk.VTK_FLOAT)

    # If no name given for data by user, use the basename of the file
    if data_name == '':
        data_name = os.path.basename(FileName)
    data.SetName(data_name)

    # Table with single column of data only
    pdo.AddColumn(data)
