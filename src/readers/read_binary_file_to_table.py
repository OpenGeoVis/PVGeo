Name = 'ReadPackedBinaryFileToTable'
Label = 'Read Packed Binary File To Table'
FilterCategory = 'CSM GP Readers'
Help = 'This filter reads in float or double data that is packed into a binary file format. It will treat the data as one long array and make a vtkTable with one column of that data. The reader uses big endian and defaults to import as floats. Use the Table to Uniform Grid or the Reshape Table filters to give more meaning to the data. We chose to use a vtkTable object as the output of this reader because it gives us more flexibility in the filters we can apply to this data down the pipeline and keeps thing simple when using filters in this repository.'

NumberOfInputs = 0
OutputDataType = 'vtkTable'
Extensions = 'H@ bin rsf rsf@ HH'
ReaderDescription = 'Binary Packed Floats or Doubles'
ExtraXml = '''\
      <IntVectorProperty
        name="Endianness"
        command="SetParameter"
        number_of_elements="1"
        initial_string="test_drop_down_menu"
        default_values="0">
        <EnumerationDomain name="enum">
          <Entry value="0" text="Big-Endian"/>
          <Entry value="1" text="Little-Endian"/>
          <Entry value="2" text="Native"/>
        </EnumerationDomain>
        <Documentation>
          This is the type memory endianness.
        </Documentation>
      </IntVectorProperty>

      <IntVectorProperty
        name="DataType"
        command="SetParameter"
        number_of_elements="1"
        initial_string="test_drop_down_menu"
        default_values="0">
        <EnumerationDomain name="enum">
          <Entry value="0" text="Float"/>
          <Entry value="1" text="Double"/>
          <Entry value="2" text="Integer"/>
        </EnumerationDomain>
        <Documentation>
          This is data type to read.
        </Documentation>
      </IntVectorProperty>
'''


Properties = dict(
    Data_Name='values',
    Time_Step=1.0,
    Endianness=0,
    DataType=0
)

PropertiesHelp = dict(
    Data_Name='The string name of the data array generated from the inut file.',
    Time_Step='An advanced property for the time step in seconds.'
)


def RequestData():
    from PVGPpy.read import packedBinaries, getTimeStepFileIndex

    # This finds the index for the FileNames for the requested timestep
    i = getTimeStepFileIndex(self, FileNames, dt=Time_Step)
    endi = ['>', '<', '@']
    dtype = ['f', 'd', 'i']

    # Generate Output
    pdo = self.GetOutput()
    packedBinaries(FileNames[i], dataNm=Data_Name, pdo=pdo, endian=endi[Endianness], dtype=dtype[DataType])


def RequestInformation(self):
    from PVGPpy.read import setOutputTimesteps
    # This is necessary to set time steps
    setOutputTimesteps(self, FileNames, dt=Time_Step)
