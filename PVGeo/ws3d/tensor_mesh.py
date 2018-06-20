__all__ = [
    # 3D Mesh
    'wsMesh3D',

    # Both
    'wsTensorMesh',
]

import numpy as np
from vtk.util import numpy_support as nps
import vtk
import os



def wsMesh3D(FileName, x0=0.0, y0=0.0, z0=0.0, ang0=0.0, pdo=None):
    """
    @desc:
    This method reads a ws3dinv Mesh file and builds a vtkStructuredGrid with topology
    and model data.
    Information about the files can be found
        Siripunvaraporn, W.; Egbert, G.; Lenbury, Y. & Uyeshima, M.
        Three-dimensional magnetotelluric inversion: data-space method
        Physics of The Earth and Planetary Interiors, 2005, 150, 3-14

    @params:
    FileName : str : The mesh filename as an absolute path for the input mesh
        file in ws3dinv Mesh/Model Format.
    x0 : float : the globl x coordinate (Easting) of for the orgin point in the model (0,0,0)
    y0 : float : the globl y coordinate (Northing) of for the orgin point in the model (0,0,0)
    z0 : float : the globl z coordinate (Elevation) of for the orgin point in the model (0,0,0)
    ang0 : float : angle rotation for the model (clockwise rotation)
    pdo : vtk.vtkStructuredGrid : opt : The output data object

    @returns:
    vtkStructuredGrid : Returns a vtkStructuredGrid generated from the ws3dinv Mesh/Model grid.
    Mesh is defined by the input mesh file and does contain data attributes.

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
    VTKArrName ='Ohm*m'
    modVTKArr = npsup.numpy_to_vtk(mod, deep=1)
    modVTKArr.SetName(VTKArrName)

    ## Calculate the global nodal coordintes
    # The internal orgin is defined in the center and top of the mesh
    x0int = np.sum(dx) / 2
    y0int = np.sum(dy) / 2
    nodeX = np.cumsum(np.append(np.array([0]), dx)) - x0int
    nodeY = np.cumsum(np.append(np.array([0]), dy)) - y0int
    nodeZ = np.cumsum(np.append(np.array([0]), dz))
    # Make nodal grid
    # NOTE: Don't fully understand way, but mesh grids need northing,easting,elev in/output to correspond with VTK
    ly, lx, lz = np.meshgrid(nodeY, nodeX, nodeZ)
    # Rotate the nodal grid
    angRad = np.deg2rad(ang0)
    rot = np.array([
        [np.cos(angRad), -np.sin(angRad)],
        [np.sin(angRad), np.cos(angRad)]])
    nodeRot = np.hstack((
        lx.T.reshape((np.prod(lx.shape), 1)),
        ly.T.reshape((np.prod(ly.shape), 1))
    )).dot(rot)
    nodCoordGlo = np.hstack(
        (nodeRot, -lz.T.reshape((np.prod(lz.shape), 1)))
    ) + np.array([x0, y0, z0])
    vtkCoordDoub = nps.numpy_to_vtk(nodCoordGlo, deep=1)
    vtkNodeCoordPts = vtk.vtkPoints()
    vtkNodeCoordPts.SetData(vtkCoordDoub)
    # Assign to a vts object
    vtsObj = vtk.vtkStructuredGrid()
    vtsObj.SetDimensions(nx + 1, ny + 1, nz + 1)
    vtsObj.SetPoints(vtkNodeCoordPts)
    vtsObj.GetCellData().AddArray(modVTKArr)

    # Return the object
    return vtsObj
