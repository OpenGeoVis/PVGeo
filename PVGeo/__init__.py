# Import base classes
try:
    # Safely test if VTK is avaialable. This is needed for Windows installation
    def tryVTK():
        import vtk
        return
    tryVTK() # Safe import in this manner so docs soes not iterate over VTK
except ImportError:
    import sys
    import mock
    import warnings
    # Mock the VTK module to run installation
    sys.modules['vtk'] = mock.Mock()
    # This is because VTK is not compatible with Windows Python 2
    warnings.warn('VTK Python package is unavailable! PVGeo is running in safe mode.')
else:
    # Import Base Classes
    from .base import *

    # Import Suites
    from . import filters
    from . import grids
    from . import gslib
    from . import model_build
    from . import readers
    #TODO: from . import tunneling
    from . import ubc

    # Import Helpers
    from . import _helpers
    from . import interface
# VTK-dependent imports complete

from . import version

# Project MetaData
__author__ = 'Bane Sullivan'
__license__ = 'BSD-3-Clause'
__copyright__ = '2018, Bane Sullivan'
__version__ = '1.1.29'
__displayname__ = 'PVGeo'


# Now check that NumPy is at a satisfactory version
version.checkNumpy()
