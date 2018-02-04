Name = 'CorrelateArrays'
Label = 'Correlate Arrays'
FilterCategory = 'CSM GP Filters'
Help = ''

NumberOfInputs = 1
NumberOfInputArrayChoices = 2

# Works on any data type so no need to specify input/ouptut
ExtraXml = ''


Properties = dict(
    Multiplyer=1.0,
    New_Array_Name='Correlated',
)

PropertiesHelp = dict(
    Multiplyer="This is a static shifter/scale factor across the array after normalization.",
    New_Array_Name="Give the new normalized array a meaningful name.",
)


def RequestData():
    from PVGPpy.filt import correlateArrays

    pdi = self.GetInput()
    pdo = self.GetOutput()

    info1 = self.GetInputArrayInformation(0)
    info2 = self.GetInputArrayInformation(1)

    correlateArrays(pdi, info1, info2, multiplyer=Multiplyer, newName=New_Array_Name, pdo=pdo)
