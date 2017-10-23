Name = 'ReadUBCMesh'
Label = 'Read UBC Mesh Two-File Format'
FilterCategory = 'CSM GP Readers'
Help = '3D models are defined using a 2-file format. The "mesh" file describes how the earth is descritized. The "model" file lists the physical property values for all cells in a mesh. A model file is meaningless without an associated mesh file. The first value is for the model\'s top-front-right, (top-south-west) corner cell. Default file delimeter is a space character'

NumberOfInputs = 0
OutputDataType = 'vtkRectilinearGrid'
ExtraXml = '''\
<Hints>
    <ReaderFactory extensions="mesh msh dat"
                   file_description="UBC Mesh Two-File Format" />
</Hints>'''


Properties = dict(
    FileName_Mesh='absolute path',
    FileName_Model='absolute path',
    data_name='',
    Delimiter_Field=' ',
    Use_tab_delimiter=False
)


def RequestData():
    import numpy as np
    import csv
    import os
    from vtk.util import numpy_support as nps

    if FileName_Mesh == 'absolute path':
        raise Exception('No mesh file selected. Aborting.')
    if FileName_Model == 'absolute path':
        raise Exception('No model file selected. Aborting.')

    pdo = self.GetOutput() # vtkRectilinearGrid

    if (Use_tab_delimiter):
        Delimiter_Field = '\t'

    #--- Read in the mesh ---#
    with open(FileName_Mesh) as f:
        reader = csv.reader(f, delimiter=Delimiter_Field)

        # TODO: ignore header lines if start with '!'

        # Number of CELLS in each axial direction
        h = reader.next()
        n1,n2,n3 = int(h[0]), int(h[1]), int(h[2])
        # change to number of POINTS in each axial direction
        n1,n2,n3 = n1+1,n2+1,n3+1
        pdo.SetDimensions(n1,n2,n3)
        #pdo.SetExtent(0,n1-1, 0,n2-1, 0,n3-1)

        # The origin corner
        h = reader.next()
        o1,o2,o3 = float(h[0]), float(h[1]), float(h[2])

        # Get spacings for 1st dimension:
        h = reader.next()
        # Set x-coordinates from spacings
        xCoords = np.zeros(n1)
        xCoords[0] = o1
        for i in range(1, n1):
            xCoords[i] = xCoords[i-1] + float(h[i-1])
        x = nps.numpy_to_vtk(num_array=xCoords,deep=True)
        pdo.SetXCoordinates(x)

        print(np.shape(x), len(h))

        # Get spacings for 2nd dimension:
        h = reader.next()
        # Set y-coordinates from spacings
        yCoords = np.zeros(n2)
        yCoords[0] = o2
        for i in range(1, n2):
            yCoords[i] = yCoords[i-1] + float(h[i-1])
        y = nps.numpy_to_vtk(num_array=yCoords,deep=True)
        pdo.SetYCoordinates(y)

        # Get spacings for 3rd dimension:
        h = reader.next()
        # Set z-coordinates from spacings
        # NOTE: UBC Mesh Specifies positive Z as down
        zCoords = np.zeros(n3)
        zCoords[0] = o3
        for i in range(1, n3):
            zCoords[i] = zCoords[i-1] - float(h[i-1])
        z = nps.numpy_to_vtk(num_array=zCoords,deep=True)
        pdo.SetZCoordinates(z)

        f.close()

    #--- Read in the model ---#
    # TODO: ignore header lines if start with '!'
    print('loaded the mesh!')
    # Add the model data to the output grid
    data = np.zeros((n1,n2,n3),dtype=float)
    with open(FileName_Model) as f:
        for i in range(n1):
            for j in range(n2):
                for k in range(n3):
                    data[i,j,k] = float(f.next())
        f.close()

    # Swap axes because VTK structures the coordinates a bit differently
    #-  This is absolutely crucial!
    #-  Do not play with unless you know what you are doing!
    data = np.swapaxes(data,0,1)
    data = np.swapaxes(data,0,2)
    data = data.flatten()

    # If no name given for data by user, use the basename of the file
    if data_name == '':
        data_name = os.path.basename(FileName_Model)

    c = nps.numpy_to_vtk(num_array=data,deep=True)
    c.SetName(data_name)
    pdo.GetPointData().AddArray(c)

def RequestInformation():
    from paraview import util
    import csv

    if FileName_Mesh == 'absolute path':
        raise Exception('No mesh file selected. Aborting.')

    # Read in the mesh and set up structure of output grid from mesh file input
    with open(FileName_Mesh) as f:
        reader = csv.reader(f, delimiter=Delimiter_Field)

        # TODO: ignore header lines if start with '!'

        # Number of points in each axial direction
        h = reader.next()
        n1,n2,n3 = int(h[0]), int(h[1]), int(h[2])

        # ABSOLUTELY NECESSARY FOR THE FILTER TO WORK:
        util.SetOutputWholeExtent(self, [0,n1-1, 0,n2-1, 0,n3-1])

        f.close()
