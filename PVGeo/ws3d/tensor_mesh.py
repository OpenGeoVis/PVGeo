__all__ = [
    # 3D Mesh
    'wsMesh3DReader',
    '_write_ws3d',

    # Both
    #TODO: 'wsTensorMesh',
]

import numpy as np
from vtk.util import numpy_support as nps
import vtk
import os

# Import Helpers:
from ..base import ReaderBase
from .. import _helpers

class wsMesh3DReader(ReaderBase):
    """This reader handles a ws3dinv Mesh file and builds a ``vtkRectilinearGrid`` with topology
    and model data.
    Information about the files can be found
        Siripunvaraporn, W.; Egbert, G.; Lenbury, Y. & Uyeshima, M.
        Three-dimensional magnetotelluric inversion: data-space method
        Physics of The Earth and Planetary Interiors, 2005, 150, 3-14
    """
    def __init__(self, x0=0.0, y0=0.0, z0=0.0, angle=0.0, **kwargs):
        ReaderBase.__init__(self, nOutputPorts=1, outputType='vtkRectilinearGrid', **kwargs)

        # Parameters:
        self.__x0 = x0
        self.__y0 = y0
        self.__z0 = z0
        self.__angle = angle


    def _wsMesh3D(self, FileName, pdo):
        """This method reads a ws3dinv Mesh file and builds a ``vtkRectilinearGrid`` with topology
        and model data.

        Information about the files can be found:
            Siripunvaraporn, W.; Egbert, G.; Lenbury, Y. & Uyeshima, M.
            Three-dimensional magnetotelluric inversion: data-space method
            Physics of The Earth and Planetary Interiors, 2005, 150, 3-14

        Args:
            FileName (str) : The mesh filename as an absolute path for the input mesh
            file in ws3dinv Mesh/Model Format.
            pdo (vtkRectilinearGrid) : The output data object

        Return:
            vtkRectilinearGrid : Returns a ``vtkRectilinearGrid`` generated from the ws3dinv Mesh/Model grid. Mesh is defined by the input mesh file and does contain data attributes.
        """

        # Simple file tests
        try:
            if not os.path.isfile(FileName):
                raise IOError('modelFile : {:s}'.format(FileName))
        except Exception as e:
            raise e
        # Read the model file
        with open(FileName, 'r') as fid:
            fileLines = fid.readlines()
        # Start extracting information
        # NOTE: The line indexing is hard coded into the program so if there are additional lines it will cause a miss read
        # NOTE: The WS3D model coord frame is x=j(northing),y=i(easting),z=depth(positive down). In order for the grid
        #       to be in a cartisian ref frame, with x,y,z obeing the right hand rule
        #       Globaly x is Easting, y is Northing and z is Elevation(that is positive upwards).
        # Read the number off cells information
        ny,nx,nz,tmp = np.array(fileLines[1].split(), dtype=int)
        # Read the vector extent information
        lnr = 2
        # Easting - x/i direction in vtk
        dy = np.array([])
        while len(dy) < ny:
            dy = np.append(dy, np.array(fileLines[lnr].split(), float))
            lnr = lnr + 1
        # Northing - y/j direction in vtk
        dx = np.array([])
        while len(dx) < nx:
            dx = np.append(dx, np.array(fileLines[lnr].split(), float))
            lnr = lnr + 1
        # Elevation - z/k direction in vtk
        dz = np.array([])
        while len(dz) < nz:
            dz = np.append(dz, np.array(fileLines[lnr].split(), float))
            lnr = lnr + 1
        # Read the physical property data
        model = np.reshape(np.array(fileLines[lnr::], float), (nz, nx, ny))
        # The values are listed from the NW-top corner of the internal ref
        # frame, need to flip in order
        # to be complient with vtk structured grid
        mod = model[:, :, -1::-1].transpose(0, 2, 1).reshape(
            (np.prod(model.shape), 1)
        )
        # Model Array - switch between S/m and Ohm*m
        VTKArrName = 'Ohm*m'
        modVTKArr = _helpers.numToVTK(mod, deep=1)
        modVTKArr.SetName(VTKArrName)

        ## Calculate the global nodal coordintes
        # The internal orgin is defined in the center and top of the mesh
        x0int = np.sum(dx) / 2
        y0int = np.sum(dy) / 2
        nodeX = np.cumsum(np.append(np.array([0]), dx)) - x0int
        nodeY = np.cumsum(np.append(np.array([0]), dy)) - y0int
        nodeZ = np.cumsum(np.append(np.array([0]), dz))
        # Make nodal grid
        # NOTE: Don't fully understand way, but mesh grids need northing,easting,elev
        # in/output to correspond with VTK
        ly, lx, lz = np.meshgrid(nodeY, nodeX, nodeZ)
        # Rotate the nodal grid
        # Set the dims and coordinates for the output
        pdo.SetDimensions(dim[0],dim[1],dim[2])
        # Convert to VTK array for setting coordinates
        pdo.SetXCoordinates(_helpers.numToVTK(cox, deep=True))
        pdo.SetYCoordinates(_helpers.numToVTK(coy, deep=True))
        pdo.SetZCoordinates(_helpers.numToVTK(coz, deep=True))

        # Return the object
        return pdo



    def RequestData(self, request, inInfo, outInfo):
        # Get output:
        output = vtk.vtkRectilinearGrid.GetData(outInfo)
        # Get requested time index
        i = _helpers.GetRequestedTime(self, outInfo)
        # Perform Read
        self._wsMesh3D(self.GetFileNames(idx=i), output)
        return 1


    #### Seters and Geters ####


    def GetOrigin(self):
        return (self.__x0, self.__y0, self.__z0)

    def SetAngle(self, angle):
        """Set the coordinate rotation angle

        Args:
            angle (float) : angle rotation for the model (clockwise rotation)
        """
        if self.__angle != angle:
            self.__angle = angle
            self.Modified()

    def SetX0(self, x0):
        if self.__x0 != x0:
            self.__x0 = x0
            self.Modified()

    def SetY0(self, y0):
        if self.__y0 != y0:
            self.__y0 = y0
            self.Modified()

    def SetZ0(self, z0):
        if self.__z0 != z0:
            self.__z0 = z0
            self.Modified()

    def SetOrigin(self, x0, y0, z0):
        """Set the origin of the gird

        Args:
            x0 (float) : the globl x coordinate (Easting) of for the orgin point in the model (0,0,0)
            y0 (float) : the globl y coordinate (Northing) of for the orgin point in the model (0,0,0)
            z0 (float) : the globl z coordinate (Elevation) of for the orgin point in the model (0,0,0)
        """
        self.SetX0(x0)
        self.SetY0(y0)
        self.SetZ0(z0)


def _write_ws3d(file_name, mesh, model):
    """Function that write a WS3D file from a SimPEG mesh object and model dict.

    :param string file_name: path of the WS3D model file to be written
    :param discretize.TensorMesh: mesh object
    :param numpy.ndarray model: Model vector to be writen
        (has to be resistivity [Ohm*m])

    """
    import SimPEG as simpeg
    import datetime
    # Small internal help function
    def write_8_val_per_line(file_id, array):
        """
        Function to write cell sizes no more then 8 values per line
        """
        for nr, item in enumerate(array):
            file_id.write('{:2.7E} '.format(item))
            if not (nr + 1)%8 or nr == array.size - 1:
                file_id.write('\n')
    # Error check
    if mesh.nC != model.size:
        raise IOError('Given model does not match the size of the mesh')
    # Read the physical property data
    mod_mat = mesh.r(model,'CC','CC','M').transpose(1, 0, 2)
    # The values are listed from the NW-top corner of the internal ref frame, need to flip in order
    # to be complient with vtk structured grid
    mod_vec = simpeg.mkvc(mod_mat[::-1, :, ::-1])
    # Write the model file
    with open(file_name,'w') as fid:
        fid.write(
            '# Model written by simpeg_meshmodel_to_ws3d on {}\n'.format(
                datetime.datetime.now()))
        # NOTE: The line indexing is hard coded into the program so if there are additional
        #  lines it will cause a miss read
        # NOTE: The WS3D model coord frame is x=j(northing),y=i(easting),z=depth(positive down).
        #  In order for the grid to be in a cartisian ref frame, with x,y,z obeing the right hand rule
        #       Globaly x is Easting, y is Northing and z is Elevation(that is positive upwards).
        fid.write('{:d} {:d} {:d} 0\n'.format(mesh.nCy, mesh.nCx, mesh.nCz))
        write_8_val_per_line(fid, mesh.hy[::-1])
        write_8_val_per_line(fid, mesh.hx)
        write_8_val_per_line(fid, mesh.hz[::-1])
        # Write the
        np.savetxt(fid, mod_vec, fmt='%2.7E')

    # Calculate the center location
    center_loc = mesh.x0 + np.array([np.sum(mesh.hx)/2., np.sum(mesh.hy)/2., np.sum(mesh.hz)])
    return center_loc
