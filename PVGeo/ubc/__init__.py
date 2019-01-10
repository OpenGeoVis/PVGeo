from .tensor import *
from .two_file_base import *
from .write import *
from .general import *

try:
    from .. import _helpers
    with _helpers.HiddenPrints():
        import discretize
except ImportError:
    pass
else:
    from .disc_meshes import *
    from .octree import *

__displayname__ = 'UBC Mesh Tools'

# NOTE: The following are a list of classes that require discretize:
#       - DiscretizeMeshReader
#       - OcTreeReader
#       - OcTreeAppender
