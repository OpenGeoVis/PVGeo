paraview_plugin_version = '2.1.0'
# This is module to import. It provides VTKPythonAlgorithmBase, the base class
# for all python-based vtkAlgorithm subclasses in VTK and decorators used to
# 'register' the algorithm with ParaView along with information about UI.
from paraview.util.vtkAlgorithm import smdomain, smhint, smproperty, smproxy

# Helpers:
from PVGeo import _helpers
# Classes to Decorate
