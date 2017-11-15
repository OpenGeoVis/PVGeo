Name = 'ReadUBCMesh'
Label = 'Read UBC Mesh Two-File Format'
FilterCategory = 'CSM GP Readers'
Help = 'UBC Mesh 3D models are defined using a 2-file format. The "mesh" file describes how the data is descritized. The "model" file lists the physical property values for all cells in a mesh. A model file is meaningless without an associated mesh file. Default file delimiter is a space character.'

NumberOfInputs = 0
OutputDataType = 'vtkRectilinearGrid'
Extensions = 'mesh msh dat'
ReaderDescription = 'UBC Mesh Two-File Format'


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

    # Make sure we have input files
    if FileName_Mesh == 'absolute path':
        raise Exception('No mesh file selected. Aborting.')
    if FileName_Model == 'absolute path':
        raise Exception('No model file selected. Aborting.')

    pdo = self.GetOutput() # vtkRectilinearGrid

    # Set the tab delimiter if needed
    if (Use_tab_delimiter):
        Delimiter_Field = '\t'

    #--- Read in the mesh ---#
    with open(FileName_Mesh) as f:
        reader = csv.reader(f, delimiter=Delimiter_Field)
        h = reader.next()
        # Ignore header lines if start with '!'
        while h[0][0] == '!':
            h = reader.next()

        # Number of CELLS in each axial direction
        n1,n2,n3 = int(h[0]), int(h[1]), int(h[2])
        numCells = n1*n2*n3
        # Change to number of POINTS in each axial direction
        #- We do ths because we have to specify the points along each axial dir
        nn = [n1,n2,n3] = [n1+1,n2+1,n3+1]

        # The origin corner (South-west-top)
        #- Remember UBC Mesh Specifies down as the positive Z
        h = reader.next()
        oo = [o1,o2,o3] = [float(h[0]), float(h[1]), float(h[2])]

        vv = [None, None, None]
        for i in range(3):
            # Get spacings for this dimension:
            h = reader.next()
            # Construct coordinates on this axis
            s = np.zeros(nn[i])
            s[0] = o1
            for j in range(1, nn[i]):
                if (i == 2):
                    # Z dimension (down is positive Z!)
                    s[j] = s[j-1] - float(h[j-1])
                else:
                    # X and Y dimensions
                    s[j] = s[j-1] + float(h[j-1])
            # Convert to VTK array for setting coordinates
            vv[i] = nps.numpy_to_vtk(num_array=s,deep=True)

        # Set the Dims and coordinates for the output
        pdo.SetDimensions(n1,n2,n3)
        pdo.SetXCoordinates(vv[0])
        pdo.SetYCoordinates(vv[1])
        pdo.SetZCoordinates(vv[2])

        f.close()

    #--- Read in the model ---#
    # Add the model data to CELL data
    data = np.zeros((n1-1,n2-1,n3-1),dtype=float)
    # Count number of lines in file
    with open(FileName_Model) as f:
        for i, l in enumerate(f):
            pass
        numLines = i + 1
        f.close()
    # Read in data from file with new iterator
    with open(FileName_Model) as f:
        h = f.next()
        skipped = 0
        # Ignore header lines if start with '!'
        while h[0][0] == '!':
            h = f.next()
            skipped += 1

        # Make sure this model file fits the dimensions of the mesh
        if (numCells < (numLines - skipped)):
            raise Exception('This model file has more cell data than for which the given mesh has cells to hold that data')
        elif (numCells > (numLines - skipped)):
            raise Exception('This model file does not have enough cell data to fill the given mesh\'s cells')

        # Iterate over everyline of the file and pull data
        try:
            for i in range(n1-1):
                for j in range(n2-1):
                    for k in range(n3-1):
                        data[i,j,k] = float(h)
                        if i*j*k == (n1*n2*n3)-3:
                            raise StopIteration
                        h = f.next()
        except StopIteration:
            pass
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

    # Convert data to VTK data structure and append to output
    c = nps.numpy_to_vtk(num_array=data,deep=True)
    c.SetName(data_name)
    # THIS IS CELL DATA!
    pdo.GetCellData().AddArray(c)


def RequestInformation():
    from paraview import util
    import csv

    if FileName_Mesh == 'absolute path':
        raise Exception('No mesh file selected. Aborting.')

    # Read in the mesh and set up structure of output grid from mesh file input
    with open(FileName_Mesh) as f:
        reader = csv.reader(f, delimiter=Delimiter_Field)
        h = reader.next()
        # TODO: ignore header lines if start with '!'
        # Ignore header lines if start with '!'
        while h[0][0] == '!':
            h = reader.next()

        # Number of CELLS in each axial direction
        n1,n2,n3 = int(h[0]), int(h[1]), int(h[2])
        # change to number of POINTS in each axial direction
        n1,n2,n3 = n1+1,n2+1,n3+1

        # ABSOLUTELY NECESSARY FOR THE FILTER TO WORK:
        util.SetOutputWholeExtent(self, [0,n1-1, 0,n2-1, 0,n3-1])

        f.close()
