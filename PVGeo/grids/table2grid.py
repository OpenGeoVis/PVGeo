__all__ = [
    'TableToGrid',
]

import vtk
from vtk.util import numpy_support as nps
import numpy as np
# Import Helpers:
from ..base import FilterBase
from .. import _helpers


#---- Table To Grid Stuff ----#



class TableToGrid(FilterBase):
    """This filter takes a ``vtkTable`` object with columns that represent data to be translated (reshaped) into a 3D grid (2D also works, just set the third dimensions extent to 1). The grid will be a ``n1`` by ``n2`` by ``n3`` ``vtkImageData`` structure and an origin (south-west bottom corner) can be set at any xyz point. Each column of the ``vtkTable`` will represent a data attribute of the ``vtkImageData`` formed (essentially a uniform mesh). The SEPlib option allows you to unfold data that was packed in the SEPlib format where the most important dimension is z and thus the z data is d1 (``d1=z``, ``d2=y``, ``d3=x``). When using SEPlib, specify ``n1`` as the number of elements in the Z-direction, ``n2`` as the number of elements in the X-direction, and ``n3`` as the number of elements in the Y-direction (and so on for other parameters).

    Warning:
        **Work in progress**
    """
    __displayname__ = 'Table To Grid'
    __type__ = 'filter'
    def __init__(self, extent=[10, 10, 10], order='C', spacing=[1.0, 1.0, 1.0],
                 origin=[0.0, 0.0, 0.0], seplib=False, swapXY=False):
        FilterBase.__init__(self,
            nInputPorts=1, inputType='vtkTable',
            nOutputPorts=1, outputType='vtkImageData')
        self.__extent = extent # MUST BE SET
        self.__spacing = spacing
        self.__origin = origin
        self.__SEPlib = seplib
        self.__order = order
        self.__swapXY = swapXY


    @staticmethod
    def _unpack(arr, extent, order='C'):
        """This is a helper method that handles the initial unpacking of a data array.
        ParaView and VTK use Fortran packing so this is convert data saved in
        C packing to Fortran packing.
        """
        n1,n2,n3 = extent[0],extent[1],extent[2]
        if order == 'C':
            arr = np.reshape(arr, (n1,n2,n3))
            arr = np.swapaxes(arr,0,2)
            extent = np.shape(arr)
        elif order == 'F':
            # effectively doing nothing
            #arr = np.reshape(arr, (n3,n2,n1))
            return arr.flatten(), extent
        return arr.flatten(), extent

    @staticmethod
    def _rearangeSEPlib(arr, extent):
        """This is a helper method to swap axes when using SEPlib axial conventions.
        """
        n1,n2,n3 = extent[0],extent[1],extent[2]
        arr = np.reshape(arr, (n3,n2,n1))
        arr = np.swapaxes(arr,0,2)
        return arr.flatten(), (n1,n2,n3)

    @staticmethod
    def _transposeXY(arr, extent, SEPlib=False):
        """Transposes X and Y axes. Needed for PoroTomo project.
        """
        n1,n2,n3 = extent[0],extent[1],extent[2]
        arr = np.reshape(arr, (n1,n2,n3))
        if SEPlib:
            arr = np.swapaxes(arr,1,2)
            ext = (n1,n3,n2)
        else:
            # print('bef: ', np.shape(arr))
            arr = np.swapaxes(arr,0,1)
            # print('aft: ', np.shape(arr))
            ext = np.shape(arr)
        return arr.flatten(), ext

    @staticmethod
    def _refold(arr, extent, SEPlib=True, order='F', swapXY=False):
        """This is a helper method to handle grabbing a data array and make sure it is ready for VTK/Fortran ordering in ``vtkImageData``.
        """
        # Fold into 3D using extents. Packing dimensions should be in order extent
        arr, extent = TableToGrid._unpack(arr, extent, order=order)
        if SEPlib:
            arr, extent = TableToGrid._rearangeSEPlib(arr, extent)
        if swapXY:
            arr, extent = TableToGrid._transposeXY(arr, extent, SEPlib=SEPlib)
        return arr#, extent

    @staticmethod
    def RefoldIdx(SEPlib=True, swapXY=False):
        """Theses are indexing corrections to set the spacings and origin witht the correct axes after refolding.
        """
        if SEPlib:
            idx = (2,1,0)
            if swapXY:
                idx = (1,2,0)
        else:
            idx = (0,1,2)
            if swapXY:
                idx = (1,0,2)
        return idx

    def _TableToGrid(self, pdi, ido):
        """Converts a table of data arrays to vtkImageData given an extent to reshape that table.
        Each column in the table will be treated as seperate data arrays for the described data space.
        """
        cols = pdi.GetNumberOfColumns()
        rows = pdi.GetColumn(0).GetNumberOfTuples()

        idx = TableToGrid.RefoldIdx(SEPlib=self.__SEPlib, swapXY=self.__swapXY)
        nx,ny,nz = self.__extent[idx[0]],self.__extent[idx[1]],self.__extent[idx[2]]
        sx,sy,sz = self.__spacing[idx[0]],self.__spacing[idx[1]],self.__spacing[idx[2]]
        ox,oy,oz = self.__origin[idx[0]],self.__origin[idx[1]],self.__origin[idx[2]]
        # make sure dimensions work
        if (nx*ny*nz != rows):
            raise _helpers.PVGeoError('Total number of elements must remain %d. Check reshape dimensions (n1 by n2 by n3).' % (rows))

        ido.SetDimensions(nx, ny, nz)
        #ido.SetExtent(0,nx-1, 0,ny-1, 0,nz-1)
        ido.SetOrigin(ox, oy, oz)
        ido.SetSpacing(sx, sy, sz)

        # Add all columns of the table as arrays to the PointData
        for i in range(cols):
            c = pdi.GetColumn(i)
            name = c.GetName()
            arr = nps.vtk_to_numpy(c)
            arr = TableToGrid._refold(arr, self.__extent, SEPlib=self.__SEPlib, order=self.__order, swapXY=self.__swapXY)
            c = nps.numpy_to_vtk(num_array=arr, deep=True)
            c.SetName(name)
            #ido.GetCellData().AddArray(c) # Should we add here? flipper won't flip these...
            # Also, image data is built by points from numrows in table
            ido.GetPointData().AddArray(c)
            #scal = ido.GetPointData().GetArray(i)

        return ido

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output"""
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        ido = self.GetOutputData(outInfo, 0)
        # Perfrom task
        self._TableToGrid(pdi, ido)
        return 1


    def RequestInformation(self, request, inInfo, outInfo):
        """Used by pipeline to set whole output extent.
        """
        # Setup the ImageData
        idx = TableToGrid.RefoldIdx(SEPlib=self.__SEPlib, swapXY=self.__swapXY)
        ext = [0, self.__extent[idx[0]]-1, 0,self.__extent[idx[1]]-1, 0,self.__extent[idx[2]]-1]
        info = outInfo.GetInformationObject(0)
        # Set WHOLE_EXTENT: This is absolutely necessary
        info.Set(vtk.vtkStreamingDemandDrivenPipeline.WHOLE_EXTENT(), ext, 6)
        return 1


    #### Setters / Getters ####


    def SetExtent(self, nx, ny, nz):
        """Set the extent of the output grid"""
        if self.__extent != [nx, ny, nz]:
            self.__extent = [nx, ny, nz]
            self.Modified()

    def SetSpacing(self, dx, dy, dz):
        """Set the spacing for the points along each axial direction
        """
        if self.__spacing != [dx, dy, dz]:
            self.__spacing = [dx, dy, dz]
            self.Modified()

    def SetOrigin(self, x0, y0, z0):
        """Set the origin of the output `vtkImageData`
        """
        if self.__origin != [x0, y0, z0]:
            self.__origin = [x0, y0, z0]
            self.Modified()

    def SetSEPlib(self, flag):
        """Set a flag to swap the axial order for the refold of the table
        """
        if self.__SEPlib != flag:
            self.__SEPlib = flag
            self.Modified()

    def SetOrder(self, order):
        """Set the reshape order (`'C'` or `'F'`)"""
        if self.__order != order:
            self.__order = order
            self.Modified()

    def SetSwapXY(self, flag):
        """Set a flag to swap the X and Y axii
        """
        if self.__swapXY != flag:
            self.__swapXY = flag
            self.Modified()
