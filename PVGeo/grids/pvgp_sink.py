__all__ = ['savePVGPGrid']

import json
import struct
import numpy as np
import base64

def _getdtypes(dtype):
    if dtype == 'float64':
        num_bytes = 8 # DOUBLE
        sdtype = 'd'
    elif dtype == 'float32':
        num_bytes = 4 # FLOAT
        sdtype = 'f'
    elif 'int' in dtype:
        num_bytes = 4 # INTEGER
        sdtype = 'i'
    else:
        raise Exception('dtype \'%s\' unknown.' % dtype)

    return dtype, sdtype, num_bytes


def savePVGPGrid(data, path, basename, spacing=(1,1,1), origin=(0,0,0), order='F', dataNames=None, endian='@'):
    """
    @desc:
    The method is for use outside of pvpython in Python 2 or 3 to save a regularly sampled grid in the PVGP format. Pass lists of multidimensional numpy arrays of same shape to save out.

    @params:
    data : list of numpy.ndarray : The attirbutes for a single model in a multidimensional array. Max dimensionality of 3. All arrays in the list must have the same shape.
    path : str : The absolute path to the location to save the file.
    basename : str : The basename of the file to be saved out.
    spacing : tuple of ints : optional : The spacings along each axial dimension
    origin : tuple of floats : optional : The XYZ location of the origin to build the volume out from
    order : char : optional : The order to unpack/pack the data arrays.
    dataNames : list of strings : optional :A list of the data names for each model attribute. Must have same number of names as number of model inputs in the `data` parameter.
    endian : char : optional : The endianness to pack the data when compressing it. Not necessary anymore.

    @returns:
    None : This method saves out a file in the PVGP Grid format.

    """
    if type(data) is not list:
        data = [data]
    numArrays = len(data)
    if dataNames is not None and len(dataNames) != numArrays:
        raise Exception('%d data array names needed. %d given to `dataNames`.' % (numArrays, len(dataNames)))
    elif dataNames is None:
        dataNames = []
        for i in range(numArrays):
            dataNames.append('Array%0d' % i)



    shps = []
    dtypes = []
    for arr in data:
        shps.append(np.shape(arr))
        dtypes.append(str(arr.dtype))
    # TODO: check that all data array shapes are the same
    ext = shps[0]

    # save the data arrays
    dataArrsDict = dict()
    for i in range(numArrays):
        # save out each data array to own file
        #format is `basename-%d.pvgp@`
        dd = data[i].flatten(order=order)
        no, sdtype, num_bytes = _getdtypes(str(dd.dtype))
        dd = struct.pack(endian+str(len(dd))+sdtype,*dd)

        dataArrsDict[dataNames[i]] = dict(
            dtype=dtypes[i],
            data=base64.encodestring(dd).decode('ascii')
        )

    # Parse out the header
    lib = dict(
        basename=basename,
        extent=ext,
        spacing=spacing,
        origin=origin,
        order=order,
        endian=endian,
        numArrays=numArrays,
        originalPath=path,
        dataArrays=dataArrsDict
    )

    # save the header
    with open('%s/%s.pvgp' % (path, basename), 'w') as fp:
        json.dump(lib, fp, indent=4)

    return None
