#! pvpython

# import the simple module from the paraview
from paraview.simple import *
from os import listdir
from os.path import isfile, join
from pvmacros import *


#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Cone'
cone1 = Cone()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
cone1Display = Show(cone1, renderView1)
# trace defaults for the display properties.
cone1Display.Representation = 'Surface'

# reset view to fit data
renderView1.ResetCamera()

# update the view to ensure updated data information
renderView1.Update()

#### uncomment the following to render all views and export
RenderAllViews()
export.exportVTKjs(FileName='test')
# alternatively, if you want to write images, you can use SaveScreenshot(...).
