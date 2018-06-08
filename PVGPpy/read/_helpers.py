"""
These are helpers specifically for the file readers for private use only.
@author: Bane Sullivan
"""
__all__ = [
    '_parseString',
    '_getVTKtype',
    '_placeArrInTable',
    '_rows2table',
    '_getdTypes',
    '_cleanDataNm'
]

import numpy as np
from vtk.util import numpy_support as nps
import vtk
import ast
import os


def _parseString(val):
    try:
        val = ast.literal_eval(val)
        if val is 0:
            val = float(0.0)
    except ValueError:
        if 'nan' in val.lower():
            val = float('NaN')
        pass
    return val


def _getVTKtype(typ):
    lookup = dict(
        char=vtk.VTK_CHAR,
        int=vtk.VTK_INT,
        uns_int=vtk.VTK_UNSIGNED_INT,
        long=vtk.VTK_LONG,
        uns_long=vtk.VTK_UNSIGNED_LONG,
        single=vtk.VTK_FLOAT,
        double=vtk.VTK_DOUBLE,
    )
    if typ is str or typ is np.string_:
        return lookup['char']
    if typ is np.float64:
        return lookup['double']
    if typ is float or typ is np.float or typ is np.float32:
        return lookup['single']
    if typ is int or np.int_:
        return lookup['int']
    raise Exception('Data type %s unknown to _getVTKtype() method.' % typ)


def _placeArrInTable(dlist, titles, pdo):
    # Put columns into table
    for i in range(len(dlist)):
        typ = _getVTKtype(type(dlist[i][0]))
        VTK_data = nps.numpy_to_vtk(num_array=dlist[i], deep=True, array_type=typ)
        VTK_data.SetName(titles[i])
        pdo.AddColumn(VTK_data)
    return None


def _rows2table(rows, titles, pdo, toVTK=True):
    # now rotate data and extract numpy arrays of same array_type
    data = np.asarray(rows).T
    typs = []
    dlist = []
    for i in range(len(titles)):
        # get data types
        typs.append(type(_parseString(data[i][0])))
        dlist.append(np.asarray(data[i], dtype=typs[i]))
    # Put columns into table
    if toVTK:
        _placeArrInTable(dlist, titles, pdo)
        return None
    return dlist


def _getdTypes(dtype='', endian=None):
    # If native `@` was chosen then do not pass an endian
    if endian is '@':
        #print('WARNING: Native endianness no longer supported for packed binary reader. Please chose `>` or `<`. This defaults to big `>`.')
        endian = ''
    # No endian specified:
    elif endian is None:
        endian = ''
    # Get numpy and VTK data types and return them both
    if dtype is 'd':
        dtype = np.dtype('%sf64'%endian) # DOUBLE
        vtktype = vtk.VTK_DOUBLE
    elif dtype is 'f':
        dtype = np.dtype('%sf32'%endian) # FLOAT
        vtktype = vtk.VTK_FLOAT
    elif dtype is 'i':
        dtype = np.dtype('%si4'%endian) # INTEGER
        vtktype = vtk.VTK_INT
    else:
        raise Exception('dtype \'%s\' unknown/.' % dtype)
    # Return data types
    return dtype, vtktype


def _cleanDataNm(dataNm, FileName):
    if dataNm is None or dataNm == '' or dataNm == 'values':
        dataNm = os.path.splitext(os.path.basename(FileName))[0]
    return dataNm
