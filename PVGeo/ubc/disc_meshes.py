__all__ = [
    'DiscretizeMeshReader',
]

__displayname__ = 'Discretize'

# Import Helpers:
from .. import _helpers
from ..base import InterfacedBaseReader
from .. import interface

with _helpers.HiddenPrints():
    import discretize


class DiscretizeMeshReader(InterfacedBaseReader):
    """A general reader for all ``discretize`` mesh objects saved to the
    ``.json`` serialized format"""
    extensions = 'json'
    __displayname__ = 'Discretize Mesh Reader'
    description = 'Serialized Discretize Meshes'
    def __init__(self, **kwargs):
        InterfacedBaseReader.__init__(self, **kwargs)

    @staticmethod
    def _read_file(filename):
        """Reads a mesh object from the serialized format"""
        return discretize.MeshIO.load_mesh(filename)

    @staticmethod
    def _get_vtk_object(obj):
        """Returns the mesh's proper VTK data object"""
        return obj.toVTK()
