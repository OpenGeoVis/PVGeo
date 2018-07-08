all = [
    'CreateEvenRectilinearGrid',
    'CreateUniformGrid',
]

import vtk
from vtk.util import numpy_support as nps
import numpy as np
#from vtk.numpy_interface import dataset_adapter as dsa
from datetime import datetime
# Import Helpers:
from ..base import PVGeoAlgorithmBase
from .. import _helpers


def _makeSpatialCellData(nx, ny, nz):
    """Used for testing"""
    arr = np.zeros((nz, ny, nx))
    for k in range(nz):
        for j in range(ny):
            for i in range(nx):
                arr[k,j,i] = k * j * i
    return arr.flatten()


class CreateUniformGrid(PVGeoAlgorithmBase):
    """@desc: Create uniform grid (`vtkImageData`)"""
    def __init__(self):
        PVGeoAlgorithmBase.__init__(self,
            nInputPorts=0,
            nOutputPorts=1, outputType='vtkImageData')
        self.__extent = [10, 10, 10]
        self.__spacing = [1.0, 1.0, 1.0]
        self.__origin = [0.0, 0.0, 0.0]


    def RequestData(self, request, inInfo, outInfo):
        pdo = self.GetOutputData(outInfo, 0)
        nx,ny,nz = self.__extent[0],self.__extent[1],self.__extent[2]
        sx,sy,sz = self.__spacing[0],self.__spacing[1],self.__spacing[2]
        ox,oy,oz = self.__origin[0],self.__origin[1],self.__origin[2]
        # Setup the ImageData
        pdo.SetDimensions(nx, ny, nz)
        pdo.SetOrigin(ox, oy, oz)
        pdo.SetSpacing(sx, sy, sz)
        #pdo.SetExtent(0,nx-1, 0,ny-1, 0,nz-1)
        # Add CELL data
        data = _makeSpatialCellData(nx-1, ny-1, nz-1) # minus 1 b/c cell data not point data
        data = nps.numpy_to_vtk(num_array=data, deep=True)
        data.SetName('Spatial Cell Data')
        # THIS IS CELL DATA! Add the model data to CELL data:
        pdo.GetCellData().AddArray(data)
        # Add Point data
        data = _makeSpatialCellData(nx, ny, nz)
        data = nps.numpy_to_vtk(num_array=data, deep=True)
        data.SetName('Spatial Point Data')
        # THIS IS CELL DATA! Add the model data to CELL data:
        pdo.GetPointData().AddArray(data)
        return 1


    def RequestInformation(self, request, inInfo, outInfo):
        # Now set whole output extent
        ext = [0, self.__extent[0]-1, 0,self.__extent[1]-1, 0,self.__extent[2]-1]
        info = outInfo.GetInformationObject(0)
        # Set WHOLE_EXTENT: This is absolutely necessary
        info.Set(vtk.vtkStreamingDemandDrivenPipeline.WHOLE_EXTENT(), ext, 6)
        return 1


    #### Setters / Getters ####


    def SetExtent(self, nx, ny, nz):
        """@desc: Set the extent of the output grid"""
        if self.__extent != [nx, ny, nz]:
            self.__extent = [nx, ny, nz]
            self.Modified()

    def SetSpacing(self, dx, dy, dz):
        """@desc: Set the spacing for the points along each axial direction"""
        if self.__spacing != [dx, dy, dz]:
            self.__spacing = [dx, dy, dz]
            self.Modified()

    def SetOrigin(self, x0, y0, z0):
        """@desc: Set the origin of the output grid"""
        if self.__origin != [x0, y0, z0]:
            self.__origin = [x0, y0, z0]
            self.Modified()





class CreateEvenRectilinearGrid(PVGeoAlgorithmBase):
    """This creates a vtkRectilinearGrid where the discretization along a given axis is uniformly distributed."""
    def __init__(self):
        PVGeoAlgorithmBase.__init__(self,
            nInputPorts=0,
            nOutputPorts=1, outputType='vtkRectilinearGrid')
        self.__extent = [10, 10, 10]
        self.__xrange = [-1.0, 1.0]
        self.__yrange = [-1.0, 1.0]
        self.__zrange = [-1.0, 1.0]


    def RequestData(self, request, inInfo, outInfo):
        # Get output of Proxy
        pdo = self.GetOutputData(outInfo, 0)
        # Perfrom task
        nx,ny,nz = self.__extent[0]+1, self.__extent[1]+1, self.__extent[2]+1

        xcoords = np.linspace(self.__xrange[0], self.__xrange[1], num=nx)
        ycoords = np.linspace(self.__yrange[0], self.__yrange[1], num=ny)
        zcoords = np.linspace(self.__zrange[0], self.__zrange[1], num=nz)

        # CONVERT TO VTK #
        xcoords = nps.numpy_to_vtk(num_array=xcoords,deep=True)
        ycoords = nps.numpy_to_vtk(num_array=ycoords,deep=True)
        zcoords = nps.numpy_to_vtk(num_array=zcoords,deep=True)

        pdo.SetDimensions(nx,ny,nz)
        pdo.SetXCoordinates(xcoords)
        pdo.SetYCoordinates(ycoords)
        pdo.SetZCoordinates(zcoords)

        data = _makeSpatialCellData(nx-1, ny-1, nz-1)
        data = nps.numpy_to_vtk(num_array=data, deep=True)
        data.SetName('Spatial Data')
        # THIS IS CELL DATA! Add the model data to CELL data:
        pdo.GetCellData().AddArray(data)
        return 1


    def RequestInformation(self, request, inInfo, outInfo):
        # Now set whole output extent
        ext = [0, self.__extent[0], 0,self.__extent[1], 0,self.__extent[2]]
        info = outInfo.GetInformationObject(0)
        # Set WHOLE_EXTENT: This is absolutely necessary
        info.Set(vtk.vtkStreamingDemandDrivenPipeline.WHOLE_EXTENT(), ext, 6)
        return 1


    #### Setters / Getters ####


    def SetExtent(self, nx, ny, nz):
        """@desc: Set the extent of the output grid"""
        if self.__extent != [nx, ny, nz]:
            self.__extent = [nx, ny, nz]
            self.Modified()

    def SetXRange(self, start, stop):
        """@desc: Set range (min, max) for the grid in the X-direction"""
        if self.__xrange != [start, stop]:
            self.__xrange = [start, stop]
            self.Modified()

    def SetYRange(self, start, stop):
        """@desc: Set range (min, max) for the grid in the Y-direction"""
        if self.__yrange != [start, stop]:
            self.__yrange = [start, stop]
            self.Modified()

    def SetZRange(self, start, stop):
        """@desc: Set range (min, max) for the grid in the Z-direction"""
        if self.__zrange != [start, stop]:
            self.__zrange = [start, stop]
            self.Modified()
