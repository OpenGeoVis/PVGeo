# Import base classes
from .base import *

# Import Suites
from . import filters
from . import grids
from . import gslib
from . import model_build
from . import readers
#TODO: from . import tunneling
from . import ubc

from . import _helpers
from . import version

__author__ = 'Bane Sullivan'
__license__ = 'BSD-3-Clause'
__copyright__ = '2018, Bane Sullivan'
__version__ = '1.1.22'
__displayname__ = 'PVGeo'


# Now check that NumPy is at a satisfactory version
version.checkNumpy()
