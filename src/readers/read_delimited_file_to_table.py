Name = 'ReadDelimitedTextFileToTable'
Label = 'Read Delimited Text File To Table'
FilterCategory = 'CSM GP Readers'
Help = 'This reader will take in any delimited text file and make a vtkTable from it. This is not much different than the default .txt or .csv reader in Paraview, however it gives us room to use our own extensions and a little more flexibility in the structure of the files we import.'

NumberOfInputs = 0
OutputDataType = 'vtkTable'
Extensions = 'dat csv txt'
ReaderDescription = 'CSM GP Delimited Text File'


Properties = dict(
    FileName='absolute_path',
    Number_Ignore_Lines=0,
    Has_Titles=True,
    Delimiter_Field=' ',
    Use_tab_delimiter=False
)

def RequestData():
    from PVGPpy.read import readDelimetedFile
    pdo = self.GetOutput()
    tbl = readDelimetedFile(FileName, deli=Delimiter_Field, useTab=Use_tab_delimiter, hasTits=Has_Titles, numIgLns=Number_Ignore_Lines)
    pdo.ShallowCopy(tbl)
