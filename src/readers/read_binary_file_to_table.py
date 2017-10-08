Name = 'ReadPackedBinaryFileToTable'
Label = 'Read Packed Binary File To Table'
FilterCategory = 'CSM GP Readers'
Help = 'This filter reads in float data that is packed into a binary file fomrat. It will treat the data as one long array and make a vtkTable with one column of that data. The reader uses big endian and defaults to import as floats. Use the Table to ImageData or the Reshape Table filters to reshape the data. We chose to make a vtkTable object as the output of this reader because it gives us more flexibility in the filters we can apply to this data down the pipeline. If you simply want the VTK data array we imported, then use the Extract Column filter.'

NumberOfInputs = 0
OutputDataType = 'vtkTable'
ExtraXml = '''\
<Hints>
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
    typ = 'f' #FLOAT
    if double_values:
        num_bytes = 8 # DOUBLE
        typ = 'd' # DOUBLE

    tn = os.stat(FileName).st_size / num_bytes
    tn_string = str(tn)
    raw = []
    with open(FileName, 'rb') as file:
        # Unpack by num_bytes
        raw = struct.unpack('>'+tn_string+typ, file.read(num_bytes*tn))

    # Put raw data into vtk array
    data = nps.numpy_to_vtk(num_array=raw, deep=True, array_type=vtk.VTK_FLOAT)

    # If no name given for data by user, use the basename of the file
    if data_name == '':
        data_name = os.path.basename(FileName)
    data.SetName(data_name)

    # Table with single column of data only
    pdo.AddColumn(data)
