def checkNumpy(warn=True):
    import numpy as np
    v = np.array(np.__version__.split('.')[0:2], dtype=int)
    if v[0] >= 1 and v[1] >= 10:
        return True
    elif warn:
        raise RuntimeWarning('WARNING: Your version of NumPy is below 1.10.x (you are using %s), please update the NumPy module used in ParaView for performance enhancement. Some filters/readers may crash otherwise.' % np.__version__)
    return False

#needToUpdateNumPy = checkNumpy()
