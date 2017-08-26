#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Read Packed Binary File To Table'
# TODO: be sure to change this file path
faultModel = ReadPackedBinaryFileToTable(FileName='/Users/bane/school/GPVR/rectilinear_grids/fault_example/PetrelFaults_Smoothed_817.bin')

# Properties modified on faultModel
faultModel.dataname = 'faults'

# create a new 'Table To ImageData'
tableToImageDataFaultModel = TableToImageData(Input=faultModel)

# Properties modified on tableToImageDataFaultModel
tableToImageDataFaultModel.nx = 312
tableToImageDataFaultModel.ny = 183
tableToImageDataFaultModel.nz = 301
tableToImageDataFaultModel.xorigin = -73
tableToImageDataFaultModel.yorigin = -256
tableToImageDataFaultModel.zorigin = 0
tableToImageDataFaultModel.xspacing = 5.0
tableToImageDataFaultModel.yspacing = 5.0
tableToImageDataFaultModel.zspacing = 5.0

# create a new 'Flip ImageData Axii'
flipImageDataAxii = FlipImageDataAxii(Input=tableToImageDataFaultModel)

# Properties modified on flipImageDataAxii1
flipImageDataAxii.reversezdir = 1


# create a new 'Threshold'
threshold = Threshold(Input=flipImageDataAxii)
threshold.Scalars = ['POINTS', 'faults']
threshold.ThresholdRange = [0.5, 1.0]

# find view
RenderView1 = FindViewOrCreate('RenderView1', viewtype='RenderView')
# uncomment following to set a specific view size
# RenderView1.ViewSize = [2004, 1062]

# set active view
SetActiveView(RenderView1)

# set active source
SetActiveSource(threshold)

# show data in view
thresholdDisplay = Show(threshold, RenderView1)
ColorBy(thresholdDisplay, ('POINTS', 'faults'))
# trace defaults for the display properties.
thresholdDisplay.Representation = 'Surface'
#thresholdDisplay.ColorArrayName = [None, '']
thresholdDisplay.OSPRayScaleArray = 'faults'
thresholdDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
thresholdDisplay.SelectOrientationVectors = 'None'
thresholdDisplay.ScaleFactor = 31.1
thresholdDisplay.SelectScaleArray = 'None'
thresholdDisplay.GlyphType = 'Arrow'
thresholdDisplay.GlyphTableIndexArray = 'None'
thresholdDisplay.DataAxesGrid = 'GridAxesRepresentation'
thresholdDisplay.PolarAxes = 'PolarAxesRepresentation'
thresholdDisplay.ScalarOpacityUnitDistance = 6.593183272470766
thresholdDisplay.GaussianRadius = 15.55
thresholdDisplay.SetScaleArray = ['POINTS', 'faults']
thresholdDisplay.ScaleTransferFunction = 'PiecewiseFunction'
thresholdDisplay.OpacityArray = ['POINTS', 'faults']
thresholdDisplay.OpacityTransferFunction = 'PiecewiseFunction'

# reset view to fit data
RenderView1.ResetCamera()


#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
