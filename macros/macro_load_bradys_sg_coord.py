# Script to read in several traces and display all in

# import the simple module from the paraview
from paraview.simple import *
from os import listdir
from os.path import isfile, join

# Disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# Get all the files to be displayed
path = '/Users/bane/school/GPVR/closed_data/traces/DASV_data/'
data_files = [f for f in listdir(path) if f.endswith(".H@") & ('TScale' in f)]
coord_files = [f for f in listdir(path) if f.endswith(".H@") & ('_coord' in f)]

# get active view
renderView = GetActiveViewOrCreate('RenderView')

# Find pairs
for d in data_files:
    # strip to just the trace number
    num = ''.join(i for i in d if i.isdigit())
    for c in coord_files:
        # strip to just the trace number
        if (int(num) is int(''.join(i for i in c if i.isdigit()))):
            # Data and Coord pair found! Let's display this trace!
            #print('Displaying trace %d' % int(num))
            attname = 'value'
            # Read coord file:
            coord = ReadPackedBinaryFileToTable(FileName=path + c)

            #---- Display the source and reciever coordinates
            # Apply 'Reshape Table' filter to get 126*6 table
            reshapeTable = ReshapeTable(Input=coord, nrows=126, ncols=6)

            # Source 'Table To Points'
            spts = TableToPoints(Input=reshapeTable)
            # trace defaults for the display properties.
            spts.XColumn = 'Field1'
            spts.YColumn = 'Field0'
            spts.ZColumn = 'Field4'
            # show data in view
            sptsDisplay = Show(spts, renderView)
            sptsDisplay.Representation = 'Points'
            sptsDisplay.PointSize = 20.0

            # Receiver 'Table To Points'
            gpts = TableToPoints(Input=reshapeTable)
            # trace defaults for the display properties.
            gpts.XColumn = 'Field3'
            gpts.YColumn = 'Field2'
            gpts.ZColumn = 'Field5'
            # show data in view
            gptsDisplay = Show(gpts, renderView)
            gptsDisplay.Representation = 'Points'
            gptsDisplay.PointSize = 20.0


            #---- Give meaningful names to for pipeline browser
            RenameSource('T'+num+'_coord', coord)
            RenameSource('T'+num+'_source_loc', spts)
            RenameSource('T'+num+'_receiver_loc', gpts)
            RenameSource('T'+num+'_coord_reshape', reshapeTable)

# Display Fault Model


# Render all views
RenderAllViews()
ResetCamera()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
