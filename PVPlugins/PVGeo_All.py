"""
This module provides a convenient means of loading all of PVGeo's plugins at once
through ParaView's plugin manager. This is a hack of a solution and will be
removed once ParaView fixes the autoloading of ParaView plugins as described in
this issue:
"""
# flake8: noqa: F401
import os
import sys

sys.path.append(os.path.dirname(__file__))

from PVGeo_Filters import *
from PVGeo_GSLib import *
from PVGeo_Grid_Tools import *
from PVGeo_Model_Builder import *
from PVGeo_Readers import *
from PVGeo_Tunneling import *
from PVGeo_UBC_Tools import *
from PyVista_Examples import *

try:
    import omf
    import omfvista
except ImportError:
    pass
else:
    from PVGeo_OMF import *
