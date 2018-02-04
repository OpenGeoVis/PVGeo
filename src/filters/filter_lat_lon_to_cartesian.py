Name = 'LatLonToCartesian'
Label = 'Lat Lon To Cartesian'
FilterCategory = 'CSM GP Filters'
Help = 'Help for the Test Filter'

NumberOfInputs = 1
InputDataType = 'vtkTable'
OutputDataType = 'vtkTable'
ExtraXml = ''


Properties = dict(
    Radius=6371.0,
    lat_i=1,
    lon_i=0,
)

# TODO: filter works but assumes a spherical earth wich is very wrong
# NOTE: Msatches the vtkEarth SOurce however so we gonna keep it this way

def RequestData():
    from PVGPpy.filt import latLonTableToCartesian
    pdi = self.GetInput()
    pdo = self.GetOutput()

    latLonTableToCartesian(pdi, lat_i, lon_i, radius=Radius, pdo=pdo)
