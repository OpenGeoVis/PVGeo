__all__ = [
    'TableToTimeGrid',
    'ReverseImageDataAxii',
    'TranslateGridOrigin',
]

__displayname__ = 'Transform'

import warnings

import numpy as np
import vtk
from vtk.numpy_interface import dataset_adapter as dsa

from .. import _helpers, interface
from ..base import FilterBase


###############################################################################

class TableToTimeGrid(FilterBase):
    """A filter to convert a static (no time variance) table to a time varying
    grid. This effectively reashapes a table full of data arrays as a 4D array
    that is placed onto the CellData of a ``vtkImageData`` object.
    """
    __displayname__ = 'Table To Time Grid'
    __category__ = 'filter'
    def __init__(self, extent=(10, 10, 10, 1), order='C',
                 spacing=(1.0, 1.0, 1.0), origin=(0.0, 0.0, 0.0),
                 dims=(0, 1, 2, 3), dt=1.0, points=False, **kwargs):
        FilterBase.__init__(self, nInputPorts=1, nOutputPorts=1,
                inputType='vtkTable', outputType='vtkImageData', **kwargs)
        if len(extent) != 4:
            raise _helpers.PVGeoError('`extent` must be of length 4.')
        self.__extent = list(extent)
        self.__dims = list(dims) # these are indexes for the filter to use on the reshape.
        # NOTE: self.__dims[0] is the x axis index, etc., self.__dims[3] is the time axis
        self.__spacing = list(spacing) # image data spacing
        self.__origin = list(origin) # image data origin
        self.__order = list(order) # unpacking order: 'C' or 'F'
        self.__data = None # this is where we hold the data so entire filter does
        # not execute on every time step. Data will be a disctionary of 4D arrays
        # each 4D array will be in (nx, ny, nz, nt) shape
        self.__needToRun = True
        self.__timesteps = None
        self.__dt = dt
        # Optional parameter to switch between cell and point data
        self.__usePointData = points
        self.__needToUpdateOutput = True


    def _set_data(self, table):
        """Internal helper to restructure the inpt table arrays"""
        self.__data = dict()
        dims = np.array([d for d in self.__dims])
        sd = dims.argsort()
        df = interface.table_to_data_frame(table)
        keys = df.keys().tolist()
        for k in keys:
            # perfrom the reshape properly. using the user given extent
            arr = np.reshape(df[k].values, self.__extent, order=self.__order)
            # Now order correctly for the image data spatial reference
            #   this uses the user specified dimension definitions
            for i in range(4):
                arr = np.moveaxis(arr, sd[i], dims[i])
            # Now add to disctionary
            self.__data[k] = arr
        self.__needToRun = False
        return

    def _build_image_data(self, img):
        """Internal helper to consturct the output"""
        if self.__needToUpdateOutput:
            # Clean out the output data object
            img.DeepCopy(vtk.vtkImageData())
            self.__needToUpdateOutput = False
        ext = self.__extent
        dims = self.__dims
        nx, ny, nz = ext[dims[0]], ext[dims[1]], ext[dims[2]]
        if not self.__usePointData:
            nx += 1
            ny += 1
            nz += 1
        sx, sy, sz = self.__spacing[0],self.__spacing[1],self.__spacing[2]
        ox, oy, oz = self.__origin[0],self.__origin[1],self.__origin[2]
        img.SetDimensions(nx, ny, nz)
        img.SetSpacing(sx, sy, sz)
        img.SetOrigin(ox, oy, oz)
        return img

    def _update_time_steps(self):
        """For internal use only: appropriately sets the timesteps.
        """
        nt = self.__extent[self.__dims[3]]
        if nt > 1:
            self.__timesteps = _helpers.update_time_steps(self, nt, self.__dt)
        return 1


    #### Algorithm Methods ####

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output"""
        # Get input/output of Proxy
        table = self.GetInputData(inInfo, 0, 0)
        img = self.GetOutputData(outInfo, 0)
        self._build_image_data(img)
        # Perfrom task
        if self.__needToRun:
            self._set_data(table)
        # Get requested time index
        i = _helpers.get_requested_time(self, outInfo)
        for k, arr in self.__data.items():
            # NOTE: Keep order='F' because of the way the grid is already reshaped
            #       the 3D array has XYZ structure so VTK requires F ordering
            narr = interface.convert_array(arr[:,:,:,i].flatten(order='F'), name=k)
            if self.__usePointData:
                img.GetPointData().AddArray(narr)
            else:
                img.GetCellData().AddArray(narr)
        return 1


    def RequestInformation(self, request, inInfo, outInfo):
        """Used by pipeline to set whole output extent."""
        # Setup the ImageData
        ext = self.__extent
        dims = self.__dims
        nx, ny, nz = ext[dims[0]], ext[dims[1]], ext[dims[2]]
        if self.__usePointData:
            ext = [0,nx-1, 0,ny-1, 0,nz-1]
        else:
            ext = [0,nx, 0,ny, 0,nz]
        info = outInfo.GetInformationObject(0)
        # Set WHOLE_EXTENT: This is absolutely necessary
        info.Set(vtk.vtkStreamingDemandDrivenPipeline.WHOLE_EXTENT(), ext, 6)
        # Now set the number of timesteps:
        self._update_time_steps()
        return 1



    #### Setters / Getters ####

    def Modified(self, run_again=True):
        """Call modified if the filter needs to run again"""
        if run_again:
            self.__needToRun = run_again
            self.__needToUpdateOutput = True
        FilterBase.Modified(self)

    def modified(self, run_again=True):
        """Call modified if the filter needs to run again"""
        return self.Modified(run_again=run_again)

    def set_extent(self, nx, ny, nz, nt):
        """Set the extent of the output grid"""
        if self.__extent != [nx, ny, nz, nt]:
            self.__extent = [nx, ny, nz, nt]
            self.Modified()

    def set_dimensions(self, x, y, z, t):
        """Set the dimensions of the output grid"""
        if self.__dims != [x, y, z, t]:
            self.__dims = [x, y, z, t]
            self.Modified()

    def set_spacing(self, dx, dy, dz):
        """Set the spacing for the points along each axial direction"""
        if self.__spacing != [dx, dy, dz]:
            self.__spacing = [dx, dy, dz]
            self.Modified()

    def set_origin(self, x0, y0, z0):
        """Set the origin of the output `vtkImageData`"""
        if self.__origin != [x0, y0, z0]:
            self.__origin = [x0, y0, z0]
            self.Modified()

    def set_order(self, order):
        """Set the reshape order (`'C'` or `'F'`)"""
        if self.__order != order:
            self.__order = order
            self.Modified(run_again=True)

    def get_time_step_values(self):
        """Use this in ParaView decorator to register timesteps on the pipeline.
        """
        return self.__timesteps.tolist() if self.__timesteps is not None else None

    def set_time_delta(self, dt):
        """An advanced property to set the time step in seconds.
        """
        if dt != self.__dt:
            self.__dt = dt
            self.Modified()

    def set_use_points(self, flag):
        """Set whether or not to place the data on the nodes/cells of the grid.
        True places data on nodes, false places data at cell centers (CellData).
        In ParaView, switching can be a bit buggy: be sure to turn the visibility
        of this data object OFF on the pipeline when changing between nodes/cells.
        """
        if self.__usePointData != flag:
            self.__usePointData = flag
            self.Modified(run_again=True)


###############################################################################



class ReverseImageDataAxii(FilterBase):
    """This filter will flip ``vtkImageData`` on any of the three cartesian axii.
    A checkbox is provided for each axis on which you may desire to flip the data.
    """
    __displayname__ = 'Reverse Image Data Axii'
    __category__ = 'filter'
    def __init__(self, axes=(True, True, True)):
        FilterBase.__init__(self,
            nInputPorts=1, inputType='vtkImageData',
            nOutputPorts=1, outputType='vtkImageData')
        self.__axes = list(axes[::-1]) # Z Y X (FORTRAN)

    def _reverse_grid_axes(self, idi, ido):
        """Internal helper to reverse data along specified axii"""
        # Copy over input to output to be flipped around
        # Deep copy keeps us from messing with the input data
        ox, oy, oz = idi.GetOrigin()
        ido.SetOrigin(ox, oy, oz)
        sx, sy, sz = idi.GetSpacing()
        ido.SetSpacing(sx, sy, sz)
        ext = idi.GetExtent()
        nx, ny, nz = ext[1]+1, ext[3]+1, ext[5]+1
        ido.SetDimensions(nx, ny, nz)

        widi = dsa.WrapDataObject(idi)
        # Iterate over all array in the PointData
        for j in range(idi.GetPointData().GetNumberOfArrays()):
            # Go through each axis and rotate if needed
            arr = widi.PointData[j]
            arr = np.reshape(arr, (nz,ny,nx))
            for i in range(3):
                if self.__axes[i]:
                    arr = np.flip(arr, axis=i)
            # Now add that data array to the output
            data = interface.convert_array(arr.flatten(), name=idi.GetPointData().GetArrayName(j))
            ido.GetPointData().AddArray(data)

        # Iterate over all array in the CellData
        for j in range(idi.GetCellData().GetNumberOfArrays()):
            # Go through each axis and rotate if needed
            arr = widi.CellData[j]
            arr = np.reshape(arr, (nz-1,ny-1,nx-1))
            for i in range(3):
                if self.__axes[i]:
                    arr = np.flip(arr, axis=i)
            # Now add that data array to the output
            data = interface.convert_array(arr.flatten(), name=idi.GetCellData().GetArrayName(j))
            ido.GetCellData().AddArray(data)

        return ido

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output.
        """
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        pdo = self.GetOutputData(outInfo, 0)
        # Perfrom task
        self._reverse_grid_axes(pdi, pdo)
        return 1


    #### Seters and Geters ####


    def set_flip_x(self, flag):
        """Set the filter to flip th input data along the X-axis
        """
        if self.__axes[2] != flag:
            self.__axes[2] = flag
            self.Modified()

    def set_flip_y(self, flag):
        """Set the filter to flip th input data along the Y-axis
        """
        if self.__axes[1] != flag:
            self.__axes[1] = flag
            self.Modified()

    def set_flip_z(self, flag):
        """Set the filter to flip th input data along the Z-axis
        """
        if self.__axes[0] != flag:
            self.__axes[0] = flag
            self.Modified()


###############################################################################

#---- Translate Grid Origin ----#

class TranslateGridOrigin(FilterBase):
    """This filter will translate the origin of `vtkImageData` to any specified
    Corner of the data set assuming it is currently in the South West Bottom
    Corner (will not work if Corner was moved prior).
    """
    __displayname__ = 'Translate Grid Origin'
    __category__ = 'filter'
    def __init__(self, corner=1):
        FilterBase.__init__(self,
            nInputPorts=1, inputType='vtkImageData',
            nOutputPorts=1, outputType='vtkImageData')
        self.__corner = corner


    def _translate(self, pdi, pdo):
        """Internal helper to translate the inputs origin"""
        if pdo is None:
            pdo = vtk.vtkImageData()

        [nx, ny, nz] = pdi.GetDimensions()
        [sx, sy, sz] = pdi.GetSpacing()
        [ox, oy, oz] = pdi.GetOrigin()

        pdo.DeepCopy(pdi)

        xx,yy,zz = 0.0,0.0,0.0

        if self.__corner == 1:
            # South East Bottom
            xx = ox - (nx-1)*sx
            yy = oy
            zz = oz
        elif self.__corner == 2:
            # North West Bottom
            xx = ox
            yy = oy - (ny-1)*sy
            zz = oz
        elif self.__corner == 3:
            # North East Bottom
            xx = ox - (nx-1)*sx
            yy = oy - (ny-1)*sy
            zz = oz
        elif self.__corner == 4:
            # South West Top
            xx = ox
            yy = oy
            zz = oz - (nz-1)*sz
        elif self.__corner == 5:
            # South East Top
            xx = ox - (nx-1)*sx
            yy = oy
            zz = oz - (nz-1)*sz
        elif self.__corner == 6:
            # North West Top
            xx = ox
            yy = oy - (ny-1)*sy
            zz = oz - (nz-1)*sz
        elif self.__corner == 7:
            # North East Top
            xx = ox - (nx-1)*sx
            yy = oy - (ny-1)*sy
            zz = oz - (nz-1)*sz

        pdo.SetOrigin(xx, yy, zz)

        return pdo

    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to generate output.
        """
        # Get input/output of Proxy
        pdi = self.GetInputData(inInfo, 0, 0)
        pdo = self.GetOutputData(outInfo, 0)
        # Perfrom task
        self._translate(pdi, pdo)
        return 1


    #### Seters and Geters ####


    def set_corner(self, corner):
        """Set the corner to use

        Args:
            corner (int) : corner location; see note.

        Note:
            * 1: South East Bottom
            * 2: North West Bottom
            * 3: North East Bottom
            * 4: South West Top
            * 5: South East Top
            * 6: North West Top
            * 7: North East Top
        """
        if self.__corner != corner:
            self.__corner = corner
            self.Modified()



###############################################################################
