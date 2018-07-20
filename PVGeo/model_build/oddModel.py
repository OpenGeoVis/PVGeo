__all__ = [
    'CreateTensorMesh',
]

import vtk
from vtk.util import numpy_support as nps
import numpy as np
from vtk.numpy_interface import dataset_adapter as dsa
# Import Helpers:
from ..base import AlgorithmBase
#from .. import _helpers

class CreateTensorMesh(AlgorithmBase):
    """This creates a vtkRectilinearGrid where the discretization along a given axis is uniformly distributed.
    """
    __displayname__ = 'Create Tensor Mesh'
    __type__ = 'source'
    def __init__(self, origin=[-350.0, -400.0, 0.0], dataname='Data'):
        AlgorithmBase.__init__(self, nInputPorts=0,
            nOutputPorts=1, outputType='vtkRectilinearGrid')
        self.__origin = origin
        self.__xcells = CreateTensorMesh._ReadCellLine('200 100 50 20*50.0 50 100 200')
        self.__ycells = CreateTensorMesh._ReadCellLine('200 100 50 21*50.0 50 100 200')
        self.__zcells = CreateTensorMesh._ReadCellLine('20*25.0 50 100 200')
        self.__dataName = dataname


    @staticmethod
    def _ReadCellLine(line):
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


    def GetExtent(self):
        ne,nn,nz = len(self.__xcells), len(self.__ycells), len(self.__zcells)
        return (0,ne, 0,nn, 0,nz)



    def _MakeModel(self, pdo):
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
        ext = self.GetExtent()
        nx,ny,nz = ext[1]+1,ext[3]+1,ext[5]+1
        pdo.SetDimensions(nx,ny,nz)
        # Convert to VTK array for setting coordinates
        pdo.SetXCoordinates(nps.numpy_to_vtk(num_array=cox, deep=True))
        pdo.SetYCoordinates(nps.numpy_to_vtk(num_array=coy, deep=True))
        pdo.SetZCoordinates(nps.numpy_to_vtk(num_array=coz, deep=True))

        return pdo


    def _AddModelData(self, pdo, data):
        ext = self.GetExtent()
        nx,ny,nz = ext[1]+1,ext[3]+1,ext[5]+1
        # ADD DATA to cells
        if data is None:
            data = np.random.rand(nx*ny*nz)
            data = nps.numpy_to_vtk(num_array=data, deep=True)
            data.SetName('Random Data')
        else:
            data = nps.numpy_to_vtk(num_array=data, deep=True)
            data.SetName(dataNm)
        pdo.GetCellData().AddArray(data)
        return pdo


    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output data object
        """
        # Get input/output of Proxy
        pdo = self.GetOutputData(outInfo, 0)
        # Perform the task
        self._MakeModel(pdo)
        self._AddModelData(pdo, None) # TODO: add ability to set input data
        return 1


    def RequestInformation(self, request, inInfo, outInfo):
        """Used by pipeline to set output whole extent
        """
        # Now set whole output extent
        extent = self.GetExtent()
        ext = [0, extent[0]-2, 0,extent[1]-2, 0,extent[2]-2]
        info = outInfo.GetInformationObject(0)
        # Set WHOLE_EXTENT: This is absolutely necessary
        info.Set(vtk.vtkStreamingDemandDrivenPipeline.WHOLE_EXTENT(), ext, 6)
        return 1


    #### Getters / Setters ####


    def SetOrigin(self, x0, y0, z0):
        """Set the origin of the output
        """
        if self.__origin != [x0, y0, z0]:
            self.__origin = [x0, y0, z0]
            self.Modified()

    def SetXCells(self, xcells):
        """Set the spacings for the cells in the X direction

        Args:
            xcells (list or np.array(floats)) : the spacings along the X-axis"""
        if len(xcells) != len(self.__xcells) or not np.allclose(self.__xcells, xcells):
            self.__xcells = xcells
            self.Modified()

    def SetYCells(self, ycells):
        """Set the spacings for the cells in the Y direction

        Args:
            ycells (list or np.array(floats)) : the spacings along the Y-axis"""
        if len(ycells) != len(self.__ycells) or not np.allclose(self.__ycells, ycells):
            self.__ycells = ycells
            self.Modified()

    def SetZCells(self, zcells):
        """Set the spacings for the cells in the Z direction

        Args:
            zcells (list or np.array(floats)): the spacings along the Z-axis"""
        if len(zcells) != len(self.__zcells) or not np.allclose(self.__zcells, zcells):
            self.__zcells = zcells
            self.Modified()

    def SetXCellsStr(self, xcellstr):
        """Set the spacings for the cells in the X direction

        Args:
            xcellstr (str) : the spacings along the X-axis in the UBC style"""
        xcells = CreateTensorMesh._ReadCellLine(xcellstr)
        self.SetXCells(xcells)

    def SetYCellsStr(self, ycellstr):
        """Set the spacings for the cells in the Y direction

        Args:
            ycellstr (str) : the spacings along the Y-axis in the UBC style"""
        ycells = CreateTensorMesh._ReadCellLine(ycellstr)
        self.SetYCells(ycells)

    def SetZCellsStr(self, zcellstr):
        """Set the spacings for the cells in the Z direction

        Args:
            zcellstr (str)  : the spacings along the Z-axis in the UBC style"""
        zcells = CreateTensorMesh._ReadCellLine(zcellstr)
        self.SetZCells(zcells)
