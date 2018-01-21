Name = 'ReadSGeMSFileToUniformGrid'
Label = 'Read SGeMS File To Uniform Grid'
FilterCategory = 'CSM GP Readers'
Help = ''

NumberOfInputs = 0
OutputDataType = 'vtkImageData'
Extensions = 'sgems SGEMS SGeMS dat txt'
ReaderDescription = 'SGeMS Grid File Format'


Properties = dict(
    FileName='absolute path',
    Delimiter_Field=' ',
    Use_tab_delimiter=False,
    # TODO: SEPLIB
)


def RequestData():
    from PVGPpy.read import sgemsGrid
    pdo = self.GetOutput() # vtkTable
    sgemsGrid(FileName, deli=Delimiter_Field, useTab=Use_tab_delimiter, pdo=pdo)


def RequestInformation():
    from paraview import util
    from PVGPpy.read import sgemsExtent
    ext = sgemsExtent(FileName, deli=Delimiter_Field, useTab=Use_tab_delimiter)
    # ABSOLUTELY NECESSARY FOR THE FILTER TO WORK:
    util.SetOutputWholeExtent(self, ext)
