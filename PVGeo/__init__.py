# flake8: noqa: F401
try:
    # Safely test if VTK is available. This is needed for Windows installation
    def tryVTK():
        import vtk

        return

    tryVTK()  # Safe import in this manner so docs soes not iterate over VTK
except ImportError:
    import sys
    import warnings

    import mock

    # Mock the VTK module to run installation
    sys.modules['vtk'] = mock.Mock()
    # This is because VTK is not compatible with Windows Python 2
    warnings.warn(
        'VTK Python package is unavailable! '
        'PVGeo is running in safe mode for installation.'
    )
else:
    # Import Base Classes
    # TODO: from . import tunneling
    # Import Suites
    from . import filters, grids, gslib, model_build, readers, ubc
    from .base import *

    try:
        __import__('omf')
        __import__('omfvista')
    except ImportError:
        pass
    else:
        from . import gmggroup

    # Import Helpers
    from . import _helpers
    from .interface import *
# VTK-dependent imports complete

from .cmaps import *

# Project MetaData
__author__ = 'Bane Sullivan'
__license__ = 'BSD-3-Clause'
__copyright__ = '2018, Bane Sullivan'
__version__ = '3.0.2'
__displayname__ = 'PVGeo'
