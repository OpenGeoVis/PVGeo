__all__ = [
    'CreateEvenRectilinearGrid',
    'CreateUniformGrid',
]

import vtk
import numpy as np
#from vtk.numpy_interface import dataset_adapter as dsa
# Import Helpers:
from ..base import AlgorithmBase
from .. import _helpers
from .. import interface


def _makeSpatialCellData(nx, ny, nz):
    """Used for testing
    """
    arr = np.fromfunction(lambda k, j, i: k*j*i, (nz, ny, nz))
    return arr.flatten()


class CreateUniformGrid(AlgorithmBase):
    """Create uniform grid (``vtkImageData``)
    """
    __displayname__ = 'Create Uniform Grid'
    __category__ = 'source'
    def __init__(self,
                 extent=[10, 10, 10],
                 spacing=[1.0, 1.0, 1.0],
                 origin=[0.0, 0.0, 0.0]):
        AlgorithmBase.__init__(self,
            nInputPorts=0,
            nOutputPorts=1, outputType='vtkImageData')
        self.__extent = extent
        self.__spacing = spacing
        self.__origin = origin


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
        data = interface.convertArray(data, name='Spatial Cell Data', deep=True)
        # THIS IS CELL DATA! Add the model data to CELL data:
        pdo.GetCellData().AddArray(data)
        # Add Point data
        data = _makeSpatialCellData(nx, ny, nz)
        data = interface.convertArray(data, name='Spatial Point Data', deep=True)
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
        """Set the extent of the output grid.
        """
        if self.__extent != [nx, ny, nz]:
            self.__extent = [nx, ny, nz]
            self.Modified()

    def SetSpacing(self, dx, dy, dz):
        """Set the spacing for the points along each axial direction.
        """
        if self.__spacing != [dx, dy, dz]:
            self.__spacing = [dx, dy, dz]
            self.Modified()

    def SetOrigin(self, x0, y0, z0):
        """Set the origin of the output grid.
        """
        if self.__origin != [x0, y0, z0]:
            self.__origin = [x0, y0, z0]
            self.Modified()





class CreateEvenRectilinearGrid(AlgorithmBase):
    """This creates a vtkRectilinearGrid where the discretization along a given axis is uniformly distributed.
    """
    __displayname__ = 'Create Even Rectilinear Grid'
    __category__ = 'source'
    def __init__(self,
                 extent=[10, 10, 10],
                 xrng=[-1.0, 1.0],
                 yrng=[-1.0, 1.0],
                 zrng=[-1.0, 1.0]):
        AlgorithmBase.__init__(self,
            nInputPorts=0,
            nOutputPorts=1, outputType='vtkRectilinearGrid')
        self.__extent = extent
        self.__xrange = xrng
        self.__yrange = yrng
        self.__zrange = zrng


    def RequestData(self, request, inInfo, outInfo):
        # Get output of Proxy
        pdo = self.GetOutputData(outInfo, 0)
        # Perfrom task
        nx,ny,nz = self.__extent[0]+1, self.__extent[1]+1, self.__extent[2]+1

        xcoords = np.linspace(self.__xrange[0], self.__xrange[1], num=nx)
        ycoords = np.linspace(self.__yrange[0], self.__yrange[1], num=ny)
        zcoords = np.linspace(self.__zrange[0], self.__zrange[1], num=nz)

        # CONVERT TO VTK #
        xcoords = interface.convertArray(xcoords,deep=True)
        ycoords = interface.convertArray(ycoords,deep=True)
        zcoords = interface.convertArray(zcoords,deep=True)

        pdo.SetDimensions(nx,ny,nz)
        pdo.SetXCoordinates(xcoords)
        pdo.SetYCoordinates(ycoords)
        pdo.SetZCoordinates(zcoords)

        data = _makeSpatialCellData(nx-1, ny-1, nz-1)
        data = interface.convertArray(data, name='Spatial Data', deep=True)
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
        """Set the extent of the output grid.
        """
        if self.__extent != [nx, ny, nz]:
            self.__extent = [nx, ny, nz]
            self.Modified()

    def SetXRange(self, start, stop):
        """Set range (min, max) for the grid in the X-direction.
        """
        if self.__xrange != [start, stop]:
            self.__xrange = [start, stop]
            self.Modified()

    def SetYRange(self, start, stop):
        """Set range (min, max) for the grid in the Y-direction
        """
        if self.__yrange != [start, stop]:
            self.__yrange = [start, stop]
            self.Modified()

    def SetZRange(self, start, stop):
        """Set range (min, max) for the grid in the Z-direction
        """
        if self.__zrange != [start, stop]:
            self.__zrange = [start, stop]
            self.Modified()
