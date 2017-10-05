# import the simple module from the paraview and other needed libraries
from paraview.simple import *
import numpy as np
from scipy.spatial import cKDTree
from vtk.util import numpy_support as nps
from vtk.numpy_interface import dataset_adapter as dsa
#from Tkinter import *
#import tkFileDialog

# disable automatic camera reset on 'Show'
#paraview.simple._DisableFirstRenderCameraReset()

# Where to save data. Absolute path:
path = 'ABSOLUTE PATH'
#path = tkFileDialog.askdirectory()

# Specify Points for the Line Source:
line = servermanager.Fetch(FindSource('TableToPoints2'))

# Specify data set to be sliced
data = FindSource('Delaunay3D1')

# Get the Points over the NumPy interface
wpdi = dsa.WrapDataObject(line) # NumPy wrapped points
points = np.array(wpdi.Points) # New NumPy array of points so we dont destroy input
numPoints = line.GetNumberOfPoints()
tree = cKDTree(points)
dist, ptsi = tree.query(points[0], k=numPoints)

# iterate of points in order (skips last point):
num = 0
numSlices = 10
for i in range(0, numPoints - 1, numPoints/numSlices):
    # get normal
    pts1 = points[ptsi[i]]
    pts2 = points[ptsi[i+1]]
    x1, y1, z1 = pts1[0], pts1[1], pts1[2]
    x2, y2, z2 = pts2[0], pts2[1], pts2[2]
    norm = [x2-x1,y2-y1,z2-z1]

    # create slice
    slc = Slice(Input=data)
    slc.SliceType = 'Plane'

    # set origin at points
    slc.SliceType.Origin = [x1,y1,z1]
    # set normal as vector from current point to next point
    slc.SliceType.Normal = norm

    # save out slice with good metadata: TODO: change name
    filename = path + 'Slice' + str(num) + '.csv'
    print(filename)
    #SaveData(filename, proxy=slc)

    # delete slice source
    #Delete(slc)
    num += 1

RenderAllViews()
ResetCamera()
