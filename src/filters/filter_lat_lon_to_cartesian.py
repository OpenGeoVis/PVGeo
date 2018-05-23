Name = 'LatLonToCartesian'
Label = 'Lat Lon To Cartesian'
FilterCategory = 'PVGP Filters'
Help = 'Help for the Test Filter'

NumberOfInputs = 1
InputDataType = 'vtkTable'
OutputDataType = 'vtkPolyData'
ExtraXml = ''

# Have two array selection drop downs for the two arrays to correlate
NumberOfInputArrayChoices = 3
InputArrayLabels = ['Latitude', 'Longitude', 'Altitude']


Properties = dict(
    Radius=6371.0,
)

# TODO: filter works but assumes a spherical earth wich is very wrong
# NOTE: Msatches the vtkEarth SOurce however so we gonna keep it this way

def RequestData():
    from PVGPpy.filt import latLonTableToCartesian
    import PVGPpy.helpers as inputhelp
    # Get input/output of Proxy
    pdi = self.GetInput()
    pdo = self.GetOutput()
    # Grab input arrays to process from drop down menus
    # Simply grab the name and field association
    namelat = inputhelp.getSelectedArrayName(self, 0)
    fieldlat = inputhelp.getSelectedArrayField(self, 0)
    namelon = inputhelp.getSelectedArrayName(self, 1)
    fieldlon = inputhelp.getSelectedArrayField(self, 1)
    namealt = inputhelp.getSelectedArrayName(self, 2)
    fieldalt = inputhelp.getSelectedArrayField(self, 2)
    # Pass on to do conversion
    latLonTableToCartesian(pdi, (namelat, fieldlat), (namelon, fieldlon), (namealt, fieldalt), radius=Radius, pdo=pdo)
