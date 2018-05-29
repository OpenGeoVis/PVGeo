from . import read
from . import filt
from . import helpers

__author__ = 'Bane Sullivan'
__license__ = 'BSD-3-Clause'
__copyright__ = '2018, Bane Sullivan'

def checkNumpy():
    import numpy as np
    v = np.array(np.__version__.split('.')[0:2], dtype=int)
    if v[0] >= 1 and v[1] >= 10:
        return True
    else:
        print('WARNING: Your version of NumPy is below 1.10.x (you are using %s), please update the NumPy module used in ParaView for performance enhancement.' % np.__version__)
        return False

#needToUpdateNumPy = checkNumpy()
