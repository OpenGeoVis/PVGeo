"""
This file contains the necessary VTKPythonAlgorithmBase subclasses to implement
functionality in this submodule as filters, sources, readers, and writers in
ParaView.
"""


# This is module to import. It provides VTKPythonAlgorithmBase, the base class
# for all python-based vtkAlgorithm subclasses in VTK and decorators used to
# 'register' the algorithm with ParaView along with information about UI.
f#TODO:from paraview.util.vtkAlgorithm import *

import numpy as np
import vtk
from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase
from vtk.util import numpy_support as nps
