__all__ = [
    'CreateEvenRectilinearGrid',
    'CreateUniformGrid',
    'CreateTensorMesh',
]

__displayname__ = 'Grids'

import numpy as np
import vtk
from vtk.numpy_interface import dataset_adapter as dsa

from .. import _helpers, interface
from ..base import AlgorithmBase


def _makeSpatialCellData(nx, ny, nz):
    """Used for testing
    """
    arr = np.fromfunction(lambda k, j, i: k*j*i, (nz, ny, nx))
    return arr.flatten()


class CreateUniformGrid(AlgorithmBase):
    """Create uniform grid (``vtkImageData``)
    """
    __displayname__ = 'Create Uniform Grid'
    __category__ = 'source'
    def __init__(self,
                 extent=(10, 10, 10),
                 spacing=(1.0, 1.0, 1.0),
                 origin=(0.0, 0.0, 0.0)):
        AlgorithmBase.__init__(self,
            nInputPorts=0,
            nOutputPorts=1, outputType='vtkImageData')
        self.__extent = extent
        self.__spacing = spacing
        self.__origin = origin


    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate the output"""
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
        data = interface.convert_array(data, name='Spatial Cell Data', deep=True)
        # THIS IS CELL DATA! Add the model data to CELL data:
        pdo.GetCellData().AddArray(data)
        # Add Point data
        data = _makeSpatialCellData(nx, ny, nz)
        data = interface.convert_array(data, name='Spatial Point Data', deep=True)
        # THIS IS CELL DATA! Add the model data to CELL data:
        pdo.GetPointData().AddArray(data)
        return 1


    def RequestInformation(self, request, inInfo, outInfo):
        """Used by pipeline to handle output extents"""
        # Now set whole output extent
        ext = [0, self.__extent[0]-1, 0,self.__extent[1]-1, 0,self.__extent[2]-1]
        info = outInfo.GetInformationObject(0)
        # Set WHOLE_EXTENT: This is absolutely necessary
        info.Set(vtk.vtkStreamingDemandDrivenPipeline.WHOLE_EXTENT(), ext, 6)
        return 1


    #### Setters / Getters ####


    def set_extent(self, nx, ny, nz):
        """Set the extent of the output grid.
        """
        if self.__extent != [nx, ny, nz]:
            self.__extent = [nx, ny, nz]
            self.Modified()

    def set_spacing(self, dx, dy, dz):
        """Set the spacing for the points along each axial direction.
        """
        if self.__spacing != [dx, dy, dz]:
            self.__spacing = [dx, dy, dz]
            self.Modified()

    def set_origin(self, x0, y0, z0):
        """Set the origin of the output grid.
        """
        if self.__origin != [x0, y0, z0]:
            self.__origin = [x0, y0, z0]
            self.Modified()





class CreateEvenRectilinearGrid(AlgorithmBase):
    """This creates a vtkRectilinearGrid where the discretization along a
    given axis is uniformly distributed.
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
        """Used by pipeline to generate the output"""
        # Get output of Proxy
        pdo = self.GetOutputData(outInfo, 0)
        # Perfrom task
        nx,ny,nz = self.__extent[0]+1, self.__extent[1]+1, self.__extent[2]+1

        xcoords = np.linspace(self.__xrange[0], self.__xrange[1], num=nx)
        ycoords = np.linspace(self.__yrange[0], self.__yrange[1], num=ny)
        zcoords = np.linspace(self.__zrange[0], self.__zrange[1], num=nz)

        # CONVERT TO VTK #
        xcoords = interface.convert_array(xcoords,deep=True)
        ycoords = interface.convert_array(ycoords,deep=True)
        zcoords = interface.convert_array(zcoords,deep=True)

        pdo.SetDimensions(nx,ny,nz)
        pdo.SetXCoordinates(xcoords)
        pdo.SetYCoordinates(ycoords)
        pdo.SetZCoordinates(zcoords)

        data = _makeSpatialCellData(nx-1, ny-1, nz-1)
        data = interface.convert_array(data, name='Spatial Data', deep=True)
        # THIS IS CELL DATA! Add the model data to CELL data:
        pdo.GetCellData().AddArray(data)
        return 1


    def RequestInformation(self, request, inInfo, outInfo):
        """Used by pipeline to handle output extents"""
        # Now set whole output extent
        ext = [0, self.__extent[0], 0,self.__extent[1], 0,self.__extent[2]]
        info = outInfo.GetInformationObject(0)
        # Set WHOLE_EXTENT: This is absolutely necessary
        info.Set(vtk.vtkStreamingDemandDrivenPipeline.WHOLE_EXTENT(), ext, 6)
        return 1


    #### Setters / Getters ####


    def set_extent(self, nx, ny, nz):
        """Set the extent of the output grid.
        """
        if self.__extent != [nx, ny, nz]:
            self.__extent = [nx, ny, nz]
            self.Modified()

    def set_x_range(self, start, stop):
        """Set range (min, max) for the grid in the X-direction.
        """
        if self.__xrange != [start, stop]:
            self.__xrange = [start, stop]
            self.Modified()

    def set_y_range(self, start, stop):
        """Set range (min, max) for the grid in the Y-direction
        """
        if self.__yrange != [start, stop]:
            self.__yrange = [start, stop]
            self.Modified()

    def set_z_range(self, start, stop):
        """Set range (min, max) for the grid in the Z-direction
        """
        if self.__zrange != [start, stop]:
            self.__zrange = [start, stop]
            self.Modified()



class CreateTensorMesh(AlgorithmBase):
    """This creates a vtkRectilinearGrid where the discretization along a
    given axis is not uniform. Cell spacings along each axis can be set via
    strings with repeating patterns or explicitly using the ``Set*Cells``
    methods.
    """
    __displayname__ = 'Create Tensor Mesh'
    __category__ = 'source'
    def __init__(self, origin=[-350.0, -400.0, 0.0], data_name='Data',
            xcellstr='200 100 50 20*50.0 50 100 200',
            ycellstr='200 100 50 21*50.0 50 100 200',
            zcellstr='20*25.0 50 100 200',):
        AlgorithmBase.__init__(self, nInputPorts=0,
            nOutputPorts=1, outputType='vtkRectilinearGrid')
        self.__origin = origin
        self.__xcells = CreateTensorMesh._read_cell_line(xcellstr)
        self.__ycells = CreateTensorMesh._read_cell_line(ycellstr)
        self.__zcells = CreateTensorMesh._read_cell_line(zcellstr)
        self.__data_name = data_name


    @staticmethod
    def _read_cell_line(line):
        """Read cell sizes for each line in the UBC mesh line strings
        """
        # OPTIMIZE: work in progress
        # TODO: when optimized, make sure to combine with UBC reader
        line_list = []
        for seg in line.split():
            if '*' in seg:
                sp = seg.split('*')
                seg_arr = np.ones((int(sp[0]),), dtype=float) * float(sp[1])
            else:
                seg_arr = np.array([float(seg)], dtype=float)
            line_list.append(seg_arr)
        return np.concatenate(line_list)


    def get_extent(self):
        """Get the extent of the created mesh"""
        ne,nn,nz = len(self.__xcells), len(self.__ycells), len(self.__zcells)
        return (0,ne, 0,nn, 0,nz)



    def _make_model(self, pdo):
        """Generates the output data object"""
        ox,oy,oz = self.__origin[0], self.__origin[1], self.__origin[2]

        # Read the cell sizes
        cx = self.__xcells
        cy = self.__ycells
        cz = self.__zcells

        # Invert the indexing of the vector to start from the bottom.
        cz = cz[::-1]
        # Adjust the reference point to the bottom south west corner
        oz = oz - np.sum(cz)

        # Now generate the coordinates for from cell width and origin
        cox = ox + np.cumsum(cx)
        cox = np.insert(cox,0,ox)
        coy = oy + np.cumsum(cy)
        coy = np.insert(coy,0,oy)
        coz = oz + np.cumsum(cz)
        coz = np.insert(coz,0,oz)

        # Set the dims and coordinates for the output
        ext = self.get_extent()
        nx,ny,nz = ext[1]+1,ext[3]+1,ext[5]+1
        pdo.SetDimensions(nx,ny,nz)
        # Convert to VTK array for setting coordinates
        pdo.SetXCoordinates(interface.convert_array(cox, deep=True))
        pdo.SetYCoordinates(interface.convert_array(coy, deep=True))
        pdo.SetZCoordinates(interface.convert_array(coz, deep=True))

        return pdo


    def _add_model_data(self, pdo, data):
        """Add an array to the output data object. If data is None, random
        values will be generated.
        """
        nx, ny, nz = pdo.GetDimensions()
        nx, ny, nz = nx-1, ny-1, nz-1
        # ADD DATA to cells
        if data is None:
            data = np.random.rand(nx*ny*nz)
            data = interface.convert_array(data, name='Random Data', deep=True)
        else:
            data = interface.convert_array(data, name=data_name, deep=True)
        pdo.GetCellData().AddArray(data)
        return pdo


    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output data object
        """
        # Get input/output of Proxy
        pdo = self.GetOutputData(outInfo, 0)
        # Perform the task
        self._make_model(pdo)
        self._add_model_data(pdo, None) # TODO: add ability to set input data
        return 1


    def RequestInformation(self, request, inInfo, outInfo):
        """Used by pipeline to set output whole extent
        """
        # Now set whole output extent
        ext = self.get_extent()
        info = outInfo.GetInformationObject(0)
        # Set WHOLE_EXTENT: This is absolutely necessary
        info.Set(vtk.vtkStreamingDemandDrivenPipeline.WHOLE_EXTENT(), ext, 6)
        return 1


    #### Getters / Setters ####


    def set_origin(self, x0, y0, z0):
        """Set the origin of the output
        """
        if self.__origin != [x0, y0, z0]:
            self.__origin = [x0, y0, z0]
            self.Modified()

    def set_x_cells(self, xcells):
        """Set the spacings for the cells in the X direction

        Args:
            xcells (list or np.array(floats)) : the spacings along the X-axis"""
        if len(xcells) != len(self.__xcells) or not np.allclose(self.__xcells, xcells):
            self.__xcells = xcells
            self.Modified()

    def set_y_cells(self, ycells):
        """Set the spacings for the cells in the Y direction

        Args:
            ycells (list or np.array(floats)) : the spacings along the Y-axis"""
        if len(ycells) != len(self.__ycells) or not np.allclose(self.__ycells, ycells):
            self.__ycells = ycells
            self.Modified()

    def set_z_cells(self, zcells):
        """Set the spacings for the cells in the Z direction

        Args:
            zcells (list or np.array(floats)): the spacings along the Z-axis"""
        if len(zcells) != len(self.__zcells) or not np.allclose(self.__zcells, zcells):
            self.__zcells = zcells
            self.Modified()

    def set_x_cells_str(self, xcellstr):
        """Set the spacings for the cells in the X direction

        Args:
            xcellstr (str) : the spacings along the X-axis in the UBC style"""
        xcells = CreateTensorMesh._read_cell_line(xcellstr)
        self.set_x_cells(xcells)

    def set_y_cells_str(self, ycellstr):
        """Set the spacings for the cells in the Y direction

        Args:
            ycellstr (str) : the spacings along the Y-axis in the UBC style"""
        ycells = CreateTensorMesh._read_cell_line(ycellstr)
        self.set_y_cells(ycells)

    def set_z_cells_str(self, zcellstr):
        """Set the spacings for the cells in the Z direction

        Args:
            zcellstr (str)  : the spacings along the Z-axis in the UBC style"""
        zcells = CreateTensorMesh._read_cell_line(zcellstr)
        self.set_z_cells(zcells)
