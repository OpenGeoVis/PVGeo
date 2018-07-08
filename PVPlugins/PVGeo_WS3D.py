# This is module to import. It provides VTKPythonAlgorithmBase, the base class
# for all python-based vtkAlgorithm subclasses in VTK and decorators used to
# 'register' the algorithm with ParaView along with information about UI.
from paraview.util.vtkAlgorithm import *

# Helpers:
from PVGeo import _helpers
# Classes to Decorate
from PVGeo.ws3d import wsMesh3DReader

WS3D_EXTS = 'ws3d' # TODO: what extensions does this use?
WS3D_DESC = 'The WS3D Format' # TODO: Description of this format for GUI


@smproxy.reader(name="PVGeowsMesh3DReader",
       label="PVGeo: WS3D Reader",
       extensions=WS3D_EXTS,
       file_description=WS3D_DESC)
@smhint.xml('''<RepresentationType view="RenderView" type="Surface With Edges" />''')
class PVGeowsMesh3DReader(wsMesh3DReader):
    def __init__(self):
        wsMesh3DReader.__init__(self)

    #### Seters and Geters ####

    # Reader decorators:

    @smproperty.xml(_helpers.getFileReaderXml(WS3D_EXTS, readerDescription=WS3D_DESC))
    def AddFileName(self, fname):
        wsMesh3DReader.AddFileName(self, fname)

    @smproperty.doublevector(name="TimeDelta", default_values=1.0, panel_visibility="advanced")
    def SetTimeDelta(self, dt):
        wsMesh3DReader.SetTimeDelta(self, dt)

    # Plugin specific Parameter decorators:

    @smproperty.doublevector(name="Origin", default_values=[0.0, 0.0, 0.0])
    def SetOrigin(self, x0, y0, z0):
        wsMesh3DReader.SetOrigin(self, x0, y0, z0)

    @smproperty.doublevector(name="Rotation", default_values=0.0)
    def SetAngle(self, angle):
        wsMesh3DReader.SetAngle(self, angle)

    @smproperty.doublevector(name="TimestepValues", information_only="1", si_class="vtkSITimeStepsProperty")
    def GetTimestepValues(self):
        """This is critical for registering the timesteps"""
        return wsMesh3DReader.GetTimestepValues(self)
