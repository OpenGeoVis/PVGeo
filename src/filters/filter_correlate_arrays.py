Name = 'CorrelateArrays'
Label = 'Correlate Arrays'
FilterCategory = 'CSM GP Filters'
Help = 'Use `np.correlate()` on `mode=\'same\'` on two selected arrays from one input.'
NumberOfInputs = 1
# Have two array selection drop downs for the two arrays to correlate
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
    import PVGPpy.helpers as inputhelp
    # Get input/output of Proxy
    pdi = self.GetInput()
    pdo = self.GetOutput()
    # Grab input arrays to process from drop down menus
    # Simply grab the name and field association
    name0 = inputhelp.getSelectedArrayName(self, 0)
    field0 = inputhelp.getSelectedArrayField(self, 0)
    name1 = inputhelp.getSelectedArrayName(self, 1)
    field1 = inputhelp.getSelectedArrayField(self, 1)
    # Pass array names and associations on to process
    correlateArrays(pdi, (name0,field0), (name1,field1), multiplyer=Multiplyer, newName=New_Array_Name, pdo=pdo)
