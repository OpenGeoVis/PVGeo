"""This module contains general grid writers for programs like Surfer"""

__all__ = [
    'WritePolyDataToSurfer',
    'WriteRectilinearGridToSurfer',
]


import vtk
from vtk.util import numpy_support as nps
import numpy as np
from vtk.numpy_interface import dataset_adapter as dsa

# Import Helpers:
from ..base import WriterBase
from .. import _helpers


#------------------------------------------------------------------------------

class WritePolyDataToSurfer(WriterBase):
    __displayname__ = 'Write PolyData to Surfer Format'
    __type__ = 'writer'
    def __init__(self):
        WriterBase.__init__(self, inputType='vtkPolyData')


    def RequestData(self, request, inInfoVec, outInfoVec):
        pdi = self.GetInputData(inInfoVec, 0, 0)

        # Convert poly data to surfer grid format and write out

        return 1


#------------------------------------------------------------------------------

class WriteRectilinearGridToSurfer(WriterBase):
    __displayname__ = 'Write RectilinearGrid to Surfer Format'
    __type__ = 'writer'
    def __init__(self):
        WriterBase.__init__(self, inputType='vtkRectilinearGrid')


    def RequestData(self, request, inInfoVec, outInfoVec):
        grd = self.GetInputData(inInfoVec, 0, 0)

        # Convert rectilinear grid data to surfer grid format and write out

        return 1


#------------------------------------------------------------------------------

# class WriteTemplate(WriterBase):
#     __displayname__ = 'Write XXX to XXX Format'
#     __type__ = 'writer'
#     def __init__(self):
#         WriterBase.__init__(self, inputType='vtkPolyData')
#
#
#     def RequestData(self, request, inInfoVec, outInfoVec):
#         pdi = self.GetInputData(inInfoVec, 0, 0)
#
#         # Convert XXX data to XXX format and write out
#
#         return 1
