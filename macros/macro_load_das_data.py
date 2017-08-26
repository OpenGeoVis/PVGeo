#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'Read Packed Binary File To Table'
# TODO: be sure to change this file path
reflectorsModel = ReadPackedBinaryFileToTable(FileName='/Users/bane/school/GPVR/rectilinear_grids/das_example/GEOTfaultreflectivityflat.H@')

# create a new 'Read Packed Binary File To Table'
wellImage = ReadPackedBinaryFileToTable(FileName='/Users/bane/school/GPVR/rectilinear_grids/das_example/GEOTwellimage.H@')

# Properties modified on reflectorsModel
reflectorsModel.dataname = 'reflectors'

# create a new 'Table To ImageData'
tableToImageDataReflectorModel = TableToImageData(Input=reflectorsModel)

# Properties modified on tableToImageDataReflectorModel
tableToImageDataReflectorModel.nx = 301
tableToImageDataReflectorModel.ny = 312
tableToImageDataReflectorModel.nz = 183
tableToImageDataReflectorModel.xspacing = 5.0
tableToImageDataReflectorModel.yorigin = -73.0
tableToImageDataReflectorModel.yspacing = 5.0
tableToImageDataReflectorModel.zorigin = -256.0
tableToImageDataReflectorModel.zspacing = 5.0


# find view
RenderView1 = FindViewOrCreate('RenderView1', viewtype='RenderView')
# uncomment following to set a specific view size
# RenderView1.ViewSize = [2004, 1062]

# set active view
SetActiveView(RenderView1)

# set active source
SetActiveSource(tableToImageDataReflectorModel)

# show data in view
tableToImageDataReflectorModelDisplay = Show(tableToImageDataReflectorModel, RenderView1)
# trace defaults for the display properties.
tableToImageDataReflectorModelDisplay.Representation = 'Outline'
tableToImageDataReflectorModelDisplay.ColorArrayName = [None, '']
tableToImageDataReflectorModelDisplay.OSPRayScaleArray = 'reflectors'
tableToImageDataReflectorModelDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
tableToImageDataReflectorModelDisplay.SelectOrientationVectors = 'None'
tableToImageDataReflectorModelDisplay.ScaleFactor = 155.5
tableToImageDataReflectorModelDisplay.SelectScaleArray = 'None'
tableToImageDataReflectorModelDisplay.GlyphType = 'Arrow'
tableToImageDataReflectorModelDisplay.GlyphTableIndexArray = 'None'
tableToImageDataReflectorModelDisplay.DataAxesGrid = 'GridAxesRepresentation'
tableToImageDataReflectorModelDisplay.PolarAxes = 'PolarAxesRepresentation'
tableToImageDataReflectorModelDisplay.ScalarOpacityUnitDistance = 9.121031525735255
tableToImageDataReflectorModelDisplay.Slice = 91

# reset view to fit data
RenderView1.ResetCamera()

# change representation type
tableToImageDataReflectorModelDisplay.SetRepresentationType('Surface')

# set scalar coloring
ColorBy(tableToImageDataReflectorModelDisplay, ('POINTS', 'reflectors'))

# rescale color and/or opacity maps used to include current data range
tableToImageDataReflectorModelDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
tableToImageDataReflectorModelDisplay.SetScalarBarVisibility(RenderView1, True)

# get color transfer function/color map for 'reflectors'
reflectorsLUT = GetColorTransferFunction('reflectors')

# Properties modified on tableToImageDataReflectorModelDisplay
tableToImageDataReflectorModelDisplay.Opacity = 0.5

# Properties modified on wellImage
wellImage.dataname = 'das_data'

# create a new 'Table To ImageData'
tableToImageDataWellImage = TableToImageData(Input=wellImage)

# Properties modified on tableToImageDataReflectorModel
tableToImageDataWellImage.nx = 301
tableToImageDataWellImage.ny = 312
tableToImageDataWellImage.nz = 183
tableToImageDataWellImage.xspacing = -5.0
tableToImageDataWellImage.yorigin = -73.0
tableToImageDataWellImage.yspacing = 5.0
tableToImageDataWellImage.zorigin = -256.0
tableToImageDataWellImage.zspacing = 5.0

# set active source
SetActiveSource(tableToImageDataWellImage)

# set active view
SetActiveView(RenderView1)

# create a new 'Contour'
contour1 = Contour(Input=tableToImageDataWellImage)
contour1.ContourBy = ['POINTS', 'das_data']
contour1.ComputeNormals = 0
contour1.ComputeScalars = 1
contour1.Isosurfaces = [-7.00337e-06, -5.2265133333333336e-06, -3.449656666666667e-06, -1.6728000000000012e-06, 1.040566666666663e-07, 1.880913333333333e-06, 3.6577699999999987e-06, 5.434626666666666e-06, 7.211483333333333e-06, 8.98834e-06]
contour1.PointMergeMethod = 'Uniform Binning'

# set active source
SetActiveSource(contour1)

# get color transfer function/color map for 'das_data'
das_dataLUT = GetColorTransferFunction('das_data')

# show data in view
contour1Display = Show(contour1, RenderView1)
# trace defaults for the display properties.
contour1Display.Representation = 'Surface'
contour1Display.ColorArrayName = ['POINTS', 'das_data']
contour1Display.LookupTable = das_dataLUT
contour1Display.OSPRayScaleArray = 'das_data'
contour1Display.OSPRayScaleFunction = 'PiecewiseFunction'
contour1Display.SelectOrientationVectors = 'None'
contour1Display.ScaleFactor = 147.60284423828125
contour1Display.SelectScaleArray = 'das_data'
contour1Display.GlyphType = 'Arrow'
contour1Display.GlyphTableIndexArray = 'das_data'
contour1Display.DataAxesGrid = 'GridAxesRepresentation'
contour1Display.PolarAxes = 'PolarAxesRepresentation'
contour1Display.GaussianRadius = 73.80142211914062
contour1Display.SetScaleArray = ['POINTS', 'das_data']
contour1Display.ScaleTransferFunction = 'PiecewiseFunction'
contour1Display.OpacityArray = ['POINTS', 'das_data']
contour1Display.OpacityTransferFunction = 'PiecewiseFunction'

# show color bar/color legend
contour1Display.SetScalarBarVisibility(RenderView1, True)

# update the view to ensure updated data information
RenderView1.Update()

# Rescale transfer function
das_dataLUT.RescaleTransferFunction(-7.00336977388e-06, 7.21148353477e-06)

# get opacity transfer function/opacity map for 'das_data'
das_dataPWF = GetOpacityTransferFunction('das_data')

# Rescale transfer function
das_dataPWF.RescaleTransferFunction(-7.00336977388e-06, 7.21148353477e-06)

#### saving camera placements for all active views

# current camera placement for RenderView1
RenderView1.CameraPosition = [-1168.6586828745951, -3169.607722609265, -2109.2096970644675]
RenderView1.CameraFocalPoint = [-749.9999999999998, 704.4999999999994, 199.00000000000023]
RenderView1.CameraViewUp = [-0.9038465781847884, -0.1426568480179643, 0.4033737557368213]
RenderView1.CameraParallelScale = 1172.1907907845036

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
