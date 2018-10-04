__all__ = [
    'TableToGrid',
    'TableToTimeGrid',
]

import vtk
import numpy as np
# Import Helpers:
from ..base import FilterBase
from .. import _helpers
from .. import interface


#---- Table To Grid Stuff ----#



class TableToGrid(FilterBase):
    """This filter takes a ``vtkTable`` object with columns that represent data
    to be translated (reshaped) into a 3D grid (2D also works, just set the
    third dimensions extent to 1). The grid will be a ``n1`` by ``n2`` by ``n3``
    ``vtkImageData`` structure and an origin (south-west bottom corner) can be
    set at any xyz point. Each column of the ``vtkTable`` will represent a data
    attribute of the ``vtkImageData`` formed (essentially a uniform mesh).
    The SEPlib option allows you to unfold data that was packed in the SEPlib
    format where the most important dimension is z and thus the z data is d1
    (``d1=z``, ``d2=y``, ``d3=x``). When using SEPlib, specify ``n1`` as the
    number of elements in the Z-direction, ``n2`` as the number of elements in
    the X-direction, and ``n3`` as the number of elements in the Y-direction
    (and so on for other parameters).

    Warning:
        **Work in progress**
    """
    __displayname__ = 'Table To Grid'
    __category__ = 'filter'
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
        """This is a helper method that handles the initial unpacking of a data
        array. ParaView and VTK use Fortran packing so this is convert data
        saved in C packing to Fortran packing.
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
        """This is a helper method to swap axes when using SEPlib axial
        conventions.
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
        """This is a helper method to handle grabbing a data array and make
        sure it is ready for VTK/Fortran ordering in ``vtkImageData``.
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
        """Theses are indexing corrections to set the spacings and origin witht
        the correct axes after refolding.
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
        """Converts a table of data arrays to vtkImageData given an extent to
        reshape that table. Each column in the table will be treated as seperate
        data arrays for the described data space.
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
            arr = interface.convertArray(c)
            arr = TableToGrid._refold(arr, self.__extent, SEPlib=self.__SEPlib, order=self.__order, swapXY=self.__swapXY)
            c = interface.convertArray(arr, name=name)
            #ido.GetCellData().AddArray(c) # Should we add here? flipper won't flip these...
            # Also, image data is built by points from numrows in table
            ido.GetPointData().AddArray(c)
            #scal = ido.GetPointData().GetArray(i)

        return ido


    #### Algorithm Methods ####

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output"""
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        ido = self.GetOutputData(outInfo, 0)
        # Perfrom task
        self._TableToGrid(pdi, ido)
        return 1


    def RequestInformation(self, request, inInfo, outInfo):
        """Used by pipeline to set whole output extent."""
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
        """Set the spacing for the points along each axial direction"""
        if self.__spacing != [dx, dy, dz]:
            self.__spacing = [dx, dy, dz]
            self.Modified()

    def SetOrigin(self, x0, y0, z0):
        """Set the origin of the output `vtkImageData`"""
        if self.__origin != [x0, y0, z0]:
            self.__origin = [x0, y0, z0]
            self.Modified()

    def SetSEPlib(self, flag):
        """Set a flag to swap the axial order for the refold of the table"""
        if self.__SEPlib != flag:
            self.__SEPlib = flag
            self.Modified()

    def SetOrder(self, order):
        """Set the reshape order (`'C'` or `'F'`)"""
        if self.__order != order:
            self.__order = order
            self.Modified()

    def SetSwapXY(self, flag):
        """Set a flag to swap the X and Y axii"""
        if self.__swapXY != flag:
            self.__swapXY = flag
            self.Modified()




###############################################################################

class TableToTimeGrid(FilterBase):
    """A filter to convert a static (no time variance) table to a time varying
    grid. This effectively reashapes a table full of data arrays as a 4D array
    that is place on to ``vtkImageData``.
    """
    __displayname__ = 'Table To Time Grid'
    __category__ = 'filter'
    def __init__(self, extent=[10, 10, 10, 1], order='C', spacing=[1.0, 1.0, 1.0],
                 origin=[0.0, 0.0, 0.0], dims=[0, 1, 2, 3], dt=1.0, **kwargs):
        FilterBase.__init__(self, nInputPorts=1, nOutputPorts=1,
                inputType='vtkTable', outputType='vtkImageData', **kwargs)
        if len(extent) != 4:
            raise _helpers.PVGeoError('`extent` must be of length 4.')
        self.__extent = extent
        self.__dims = dims # these are indexes for the filter to use on the reshape.
        # NOTE: self.__dims[0] is the x axis index, etc., self.__dims[3] is the time axis
        self.__spacing = spacing # image data spacing
        self.__origin = origin # image data origin
        self.__order = order # unpacking order: 'C' or 'F'
        self.__data = None # this is where we hold the data so entire filter does
        # not execute on every time step. Data will be a disctionary of 4D arrays
        # each 4D array will be in (nx, ny, nz, nt) shape
        self.__needToRun = True
        self.__timesteps = None
        self.__dt = dt


    def _SetData(self, table):
        self.__data = dict()
        dims = [d for d in self.__dims]
        df = interface.tableToDataFrame(table)
        keys = df.keys().tolist()
        for k in keys:
            # perfrom the reshape properly.
            arr = np.reshape(df[k].values, self.__extent, order=self.__order)
            # Now order correctly for the image data spatial reference
            for i in [0, 1, 2, 3]:
                d = dims[i]
                dims[d] = dims[i]
                dims[i] = i
                arr = arr.swapaxes(d, i)
            # Now add to disctionary
            self.__data[k] = arr
        self.__needToRun = False
        return

    def _BuildImageData(self, img):
        ext = self.__extent
        dims = self.__dims
        nx, ny, nz = ext[dims[0]], ext[dims[1]], ext[dims[2]]
        sx, sy, sz = self.__spacing[0],self.__spacing[1],self.__spacing[2]
        ox, oy, oz = self.__origin[0],self.__origin[1],self.__origin[2]
        img.SetDimensions(nx, ny, nz)
        img.SetSpacing(sx, sy, sz)
        img.SetOrigin(ox, oy, oz)
        return img

    def _UpdateTimeSteps(self):
        """For internal use only: appropriately sets the timesteps.
        """
        nt = self.__extent[self.__dims[3]]
        if nt > 1:
            self.__timesteps = _helpers.updateTimeSteps(self, nt, self.__dt)
        return 1


    #### Algorithm Methods ####

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output"""
        # Get input/output of Proxy
        table = self.GetInputData(inInfo, 0, 0)
        img = vtk.vtkImageData.GetData(outInfo, 0)
        self._BuildImageData(img)
        # Perfrom task
        if self.__needToRun:
            self._SetData(table)
        # Get requested time index
        i = _helpers.getRequestedTime(self, outInfo)
        for k, arr in self.__data.items():
            img.GetPointData().AddArray(
                interface.convertArray(arr[:,:,:,i].flatten(order='F'), name=k)
                )
        return 1


    def RequestInformation(self, request, inInfo, outInfo):
        """Used by pipeline to set whole output extent."""
        # Setup the ImageData
        ext = self.__extent
        dims = self.__dims
        nx, ny, nz = ext[dims[0]], ext[dims[1]], ext[dims[2]]
        ext = [0, nx-1, 0,ny-1, 0,nz-1]
        info = outInfo.GetInformationObject(0)
        # Set WHOLE_EXTENT: This is absolutely necessary
        info.Set(vtk.vtkStreamingDemandDrivenPipeline.WHOLE_EXTENT(), ext, 6)
        # Now set the number of timesteps:
        self._UpdateTimeSteps()
        return 1



    #### Setters / Getters ####

    def Modified(self, runAgain=True):
        """Call modified if the filter needs to run again"""
        if runAgain: self.__needToRun = runAgain
        FilterBase.Modified(self)

    def SetExtent(self, nx, ny, nz, nt):
        """Set the extent of the output grid"""
        if self.__extent != [nx, ny, nz, nt]:
            self.__extent = [nx, ny, nz, nt]
            self.Modified()

    def SetDimensions(self, x, y, z, t):
        if self.__dims != [x, y, z, t]:
            self.__dims = [x, y, z, t]
            self.Modified()

    def SetSpacing(self, dx, dy, dz):
        """Set the spacing for the points along each axial direction"""
        if self.__spacing != [dx, dy, dz]:
            self.__spacing = [dx, dy, dz]
            self.Modified()

    def SetOrigin(self, x0, y0, z0):
        """Set the origin of the output `vtkImageData`"""
        if self.__origin != [x0, y0, z0]:
            self.__origin = [x0, y0, z0]
            self.Modified()

    def SetOrder(self, order):
        """Set the reshape order (`'C'` or `'F'`)"""
        if self.__order != order:
            self.__order = order
            self.Modified()

    def GetTimestepValues(self):
        """Use this in ParaView decorator to register timesteps on the pipeline.
        """
        return self.__timesteps.tolist() if self.__timesteps is not None else None

    def SetTimeDelta(self, dt):
        """An advanced property to set the time step in seconds.
        """
        if dt != self.__dt:
            self.__dt = dt
            self.Modified()



###############################################################################
