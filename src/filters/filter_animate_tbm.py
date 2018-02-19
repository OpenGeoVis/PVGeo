Name = 'AnimateTBM'
Label = 'Animate Tunnel Boring Machine'
FilterCategory = 'CSM GP Filters'
Help = 'This filter analyzes a vtkTable containing position information about a Tunnel Boring Machine (TBM). This Filter iterates over each row of the table as a timestep and uses the XYZ coordinates of the three different parts of the TBM to generate a tube that represents the TBM.'
NumberOfInputs = 1
InputDataType = 'vtkTable'
OutputDataType = 'vtkPolyData'
# Have two array selection drop downs for the two arrays to correlate
NumberOfInputArrayChoices = 9
ExtraXml = '''\
    <DoubleVectorProperty
      name="TimestepValues"
      repeatable="1"
      information_only="1">
      <TimeStepsInformationHelper/>
          <Documentation>
          Available timestep values.
          </Documentation>
    </DoubleVectorProperty>
'''

InputArrayLabels = ['Head Easting', 'Head Northing', 'Head Elevation',
                    'Arti Easting', 'Arti Northing', 'Arti Elevation',
                    'Tail Easting', 'Tail Northing', 'Tail Elevation']

Properties = dict(
    Diameter=17.45,
    #Lengths=[1.66,7.76,10.17],
    dt=1.0
)

PropertiesHelp = dict(
)


def RequestData():
    import numpy as np
    from vtk.numpy_interface import dataset_adapter as dsa
    import PVGPpy.helpers as inputhelp
    from PVGPpy.filt import pointsToTube
    # Get input/output of Proxy
    pdi = self.GetInput()
    pdo = self.GetOutput()
    # Grab input arrays to process from drop down menus
    #- Assume all fiels are same for now:
    field = inputhelp.getSelectedArrayField(self, 0)
    #- Simply grab the names
    names = []
    for i in range(9):
        names.append(inputhelp.getSelectedArrayName(self, i))
    # Pass array names and associations on to process
    # Get the input arrays
    wpdi = dsa.WrapDataObject(pdi)
    arrs = []
    for i in range(9):
        arrs.append(inputhelp.getArray(wpdi, field, names[i]))

    # grab coordinates for each part of boring machine at time idx as row
    executive = self.GetExecutive()
    outInfo = executive.GetOutputInformation(0)
    idx = int(outInfo.Get(executive.UPDATE_TIME_STEP())/dt)
    pts = []
    for i in range(3):
        x = arrs[i*3][idx]
        y = arrs[i*3+1][idx]
        z = arrs[i*3+2][idx]
        # TODO: if we want to account for length of actual parts of the machine
        # then calc extra points here and append to pts in correct order
        pts.append((x,y,z))
    # now exectute a points to tube filter
    vtk_pts = vtk.vtkPoints()
    for i in range(len(pts)):
        vtk_pts.InsertNextPoint(pts[i][0],pts[i][1],pts[i][2])
    # missing something here
    poly = vtk.vtkPolyData()
    poly.SetPoints(vtk_pts)
    pointsToTube(poly, radius=Diameter/2, numSides=20, nrNbr=False, pdo=pdo)


def RequestInformation(self):
    # This is necessary to set time steps
    executive = self.GetExecutive()
    outInfo = executive.GetOutputInformation(0)

    # Calculate list of timesteps here
    # set up time space
    def _calculateTimeRange(num, dt=0.001):
        """Discretizes time range accoridng to step size `dt` in seconds"""
        import numpy as np
        return np.arange(0,num*dt,dt, dtype=float)
    #- Get number of rows in table and use that for num time steps
    pdi = self.GetInput()
    nrows = int(pdi.GetColumn(0).GetNumberOfTuples())
    xtime = _calculateTimeRange(nrows,dt=dt)
    outInfo.Remove(executive.TIME_STEPS())
    for i in range(len(xtime)):
        outInfo.Append(executive.TIME_STEPS(), xtime[i])
    # Remove and set time range info
    outInfo.Remove(executive.TIME_RANGE())
    outInfo.Append(executive.TIME_RANGE(), xtime[0])
    outInfo.Append(executive.TIME_RANGE(), xtime[-1])
