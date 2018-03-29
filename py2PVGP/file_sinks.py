import os
import json
import struct
import numpy as np

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
    ## The import is working!!!!


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

        fname = '%s-%s.pvgp@' % (basename,dataNames[i])
        dataArrsDict[dataNames[i]] = dict(
            filemane=fname,
            dtype=dtypes[i]
        )
        with open('%s/%s' % (path, fname), 'wb') as f:
            f.write(dd)

    # Parse out the header
    lib = dict(
        basename=basename,
        extent=ext,
        spacing=spacing,
        origin=origin,
        order=order,
        endian=endian,
        numArrays=numArrays,
        dataArrays=dataArrsDict,
        originalPath=path
    )

    # save the header
    with open('%s/%s.pvgp' % (path, basename), 'w') as fp:
        json.dump(lib, fp, indent=4)

    return None
