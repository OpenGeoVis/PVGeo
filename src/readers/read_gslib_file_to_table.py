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
    import os
    from PVGPpy.read import readGSLIB
    pdo = self.GetOutput() # vtkTable
    tbl, h = pdoreadGSLIB(FileName, deli=Delimiter_Field, useTab=Use_tab_delimiter, numIgLns=Number_Ignore_Lines)
    pdo.ShallowCopy(tbl)
    print(os.path.basename(FileName) + ': ' + h)
