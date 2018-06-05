Name = 'ReadMadagascarFileToTable'
Label = 'Read Madagascar File To Table'
FilterCategory = 'PVGP Readers'
Help = 'This reads in float or double data that is packed into a Madagascar Single Stream RSF binary file format with a leader header. The reader ignores all of the ascii header details by searching for the sequence of three special characters: EOL EOL EOT (\014\014\004) and it will treat the following binary packed data as one long array and make a `vtkTable` with one column of that data. The reader defaults to import as floats with native endianness. Use the Table to Uniform Grid or the Reshape Table filters to give more meaning to the data. We will later implement the ability to create a gridded volume from the header info. We chose to use a vtkTable object as the output of this reader because it gives us more flexibility in the filters we can apply to this data down the pipeline and keeps thing simple when using filters in this repository. Details: http://www.ahay.org/wiki/RSF_Comprehensive_Description#Single-stream_RSF'

NumberOfInputs = 0
OutputDataType = 'vtkTable'
Extensions = 'H@ bin rsf rsf@ HH'
ReaderDescription = 'PVGP: Madagascar Single Stream RSF Format'
ExtraXml = '''\
      <IntVectorProperty
        name="Endianness"
        command="SetParameter"
        number_of_elements="1"
        initial_string="test_drop_down_menu"
        default_values="0">
        <EnumerationDomain name="enum">
          <Entry value="0" text="Native"/>
          <Entry value="1" text="Little-Endian"/>
          <Entry value="2" text="Big-Endian"/>
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
    Data_Name='',
    Time_Step=1.0,
    Endianness=0,
    DataType=0
)

PropertiesHelp = dict(
    Data_Name='The string name of the data array generated from the inut file.',
    Time_Step='An advanced property for the time step in seconds.'
)


def RequestData():
    from PVGPpy.read import madagascar, getTimeStepFileIndex

    # This finds the index for the FileNames for the requested timestep
    i = getTimeStepFileIndex(self, FileNames, dt=Time_Step)
    endi = ['@', '<', '>']
    dtype = ['f', 'd', 'i']

    # Generate Output
    pdo = self.GetOutput()
    madagascar(FileNames[i], dataNm=Data_Name, pdo=pdo, endian=endi[Endianness], dtype=dtype[DataType])


def RequestInformation(self):
    from PVGPpy.read import setOutputTimesteps
    # This is necessary to set time steps
    setOutputTimesteps(self, FileNames, dt=Time_Step)
