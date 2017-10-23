#### import the simple module from the paraview
#from paraview.simple import *
import numpy as np
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()


# find source
clip2 = FindSource('Clip2')

# get active source.
#clip2 = GetActiveSource()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
for y in np.arange(9195039,9206413,200):
    clip2.ClipType.Origin = [801180.0, y, 1083.91499328613]
    renderView1.Update()
    RenderAllViews()
