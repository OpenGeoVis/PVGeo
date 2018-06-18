# Import base classes
from .base import *

# Import Suites
from . import filters_general
from . import grids
from . import gslib
from . import model_build
from . import readers_general
from . import tunneling
from . import ubc

from . import _helpers
#from . import pvplugins
#from . import _detail

__author__ = 'Bane Sullivan'
__license__ = 'BSD-3-Clause'
__copyright__ = '2018, Bane Sullivan'
__version__ = '0.7.2'

def checkNumpy():
    import numpy as np
    v = np.array(np.__version__.split('.')[0:2], dtype=int)
    if v[0] >= 1 and v[1] >= 10:
        return True
    else:
        print('WARNING: Your version of NumPy is below 1.10.x (you are using %s), please update the NumPy module used in ParaView for performance enhancement.' % np.__version__)
        return False

#needToUpdateNumPy = checkNumpy()
