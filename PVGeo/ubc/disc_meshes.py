__all__ = [
    'DiscretizeMeshReader',
]

__displayname__ = 'General Tools'

import numpy as np
import pandas as pd
import vtk
from vtk.numpy_interface import dataset_adapter as dsa

import sys
sys.path.append('/Users/bane/Documents/OpenGeoVis/Software/discretize')
import discretize


# Import Helpers:
from .. import _helpers
from ..base import InterfacedBaseReader
from .. import interface


class DiscretizeMeshReader(InterfacedBaseReader):
    """A general reader for all ``discretize`` mesh objects saved to the
    ``.json`` serialized format"""
    extensions = 'json'
    __displayname__ = 'Discretize Mesh Reader'
    description = 'Serialized Discretize Meshes'
    def __init__(self, **kwargs):
        InterfacedBaseReader.__init__(self, outputType='vtkStructuredGrid', **kwargs)

    @staticmethod
    def _readFile(filename):
        """Reads a mesh object from the serialized format"""
        return discretize.MeshIO.load_mesh(filename)

    @staticmethod
    def _getVTKObject(obj):
        """Returns the mesh's proper VTK data object"""
        return obj.toVTK()
