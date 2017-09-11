# Script to read in packed floats, reshape them to a table and extract coordinates

# import the simple module from the paraview
from paraview.simple import *
from os import listdir
from os.path import isfile, join

# TODO: make sure this is the same as the PVPATH variable in the installation script
PVPATH = '/Applications/ParaView-5.4.0.app/Contents/MacOS/plugins/'
filters = [f for f in listdir(PVPATH) if f.endswith(".xml")]
for f in filters:
    LoadPlugin(PVPATH + f, remote=True, ns=globals())

# TODO: change the directory!
# Get all the files to be displayed
path = '/Users/bane/school/GPVR/closed_data/traces/DASV_data/'
# TODO: you may want to change where this saves!
merge_name = path + '../all_coords.vtu'

# This finds all the coord files in the specified directory
coord_files = [f for f in listdir(path) if f.endswith(".H@") & ('_coord' in f)]

# Disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get active view
renderView = GetActiveViewOrCreate('RenderView')

group = GroupDatasets()

count = 0
for c in coord_files:
    # strip filename to get the trace number
    num = ''.join(i for i in c if i.isdigit())
    perc = (1.0 * count/ (1.0 * len(coord_files))) * 100.0
    print('Processing trace %d' % int(num), '%d percent complete' % perc)
    count += 1
    attname = 'value'
    # Read coord file:
    coord = ReadPackedBinaryFileToTable(FileName=path + c)

    #---- Display the source and reciever coordinates
    # Apply 'Reshape Table' filter to get 126*6 table
    reshapeTable = ReshapeTable(Input=coord, nrows=126, ncols=6)

    # Source 'Table To Points'
    spts = TableToPoints(Input=reshapeTable)
    # trace defaults for the display properties.
    # NOTE: Field indexes changed to match the other models (original commented out)
    spts.XColumn = 'Field4' #1
    spts.YColumn = 'Field1' #0
    spts.ZColumn = 'Field0' #4
    # show data in view
    sptsDisplay = Show(spts, renderView)
    sptsDisplay.Representation = 'Points'
    sptsDisplay.PointSize = 20.0

    # Receiver 'Table To Points'
    gpts = TableToPoints(Input=reshapeTable)
    # trace defaults for the display properties.
    gpts.XColumn = 'Field5' #3
    gpts.YColumn = 'Field3' #2
    gpts.ZColumn = 'Field2' #5
    # show data in view
    gptsDisplay = Show(gpts, renderView)
    gptsDisplay.Representation = 'Points'
    gptsDisplay.PointSize = 20.0

    #---- Give meaningful names to for pipeline browser
    RenameSource('T'+num+'_coord', coord)
    RenameSource('T'+num+'_source_loc', spts)
    RenameSource('T'+num+'_receiver_loc', gpts)
    RenameSource('T'+num+'_coord_reshape', reshapeTable)

    group.Input.append(gpts)
    group.Input.append(spts)
# Render all views
RenderAllViews()
ResetCamera()
print('Saving out to: ', merge_name)
merge = MergeBlocks(Input=group)
SaveData(merge_name, proxy=merge)
