paraview_plugin_version = '2.1.0'
# This is module to import. It provides VTKPythonAlgorithmBase, the base class
# for all python-based vtkAlgorithm subclasses in VTK and decorators used to
# 'register' the algorithm with ParaView along with information about UI.
from paraview.util.vtkAlgorithm import smhint, smproxy

from pyvista import examples
import vtk
from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase


MENU_CAT = 'PyVista: Example Data Sets'


class _ExampleLoader(VTKPythonAlgorithmBase):

    def __init__(self):
        VTKPythonAlgorithmBase.__init__(self, nInputPorts=0, nOutputPorts=1,
                                        outputType=self._example_data.GetClassName())


    def RequestData(self, request, inInfo, outInfo):
        """Used by pipeline to get data for current timestep and populate the
        output data object.
        """
        # Get output:
        output = self.GetOutputData(outInfo, 0)
        output.DeepCopy(self._example_data)
        return 1


    def RequestInformation(self, request, inInfo, outInfo):
        """Used by pipeline to handle output extents"""
        try:
            extent = self._example_data.GetExtent()
            # Now set whole output extent
            # ext = [0, extent[0]-1, 0,extent[1]-1, 0,extent[2]-1]
            info = outInfo.GetInformationObject(0)
            # Set WHOLE_EXTENT: This is absolutely necessary
            info.Set(vtk.vtkStreamingDemandDrivenPipeline.WHOLE_EXTENT(), extent, 6)
        except AttributeError:
            pass
        return 1



@smproxy.source(name='PyVistaStHelens', label='Mt. St. Helens')
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
class PyVistaStHelens(_ExampleLoader):
    def __init__(self):
        self._example_data = examples.download_st_helens()
        _ExampleLoader.__init__(self)


@smproxy.source(name='PyVistaChannels', label='Channels')
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
class PyVistaChannels(_ExampleLoader):
    def __init__(self):
        self._example_data = examples.load_channels()
        _ExampleLoader.__init__(self)


@smproxy.source(name='PyVistaActionFigure', label='Action Figure')
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
class PyVistaActionFigure(_ExampleLoader):
    def __init__(self):
        self._example_data = examples.download_action_figure()
        _ExampleLoader.__init__(self)


@smproxy.source(name='PyVistaArmadillo', label='Armadillo')
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
class PyVistaArmadillo(_ExampleLoader):
    def __init__(self):
        self._example_data = examples.download_armadillo()
        _ExampleLoader.__init__(self)


@smproxy.source(name='PyVistaBloodVessels', label='Blood Vessels')
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
class PyVistaBloodVessels(_ExampleLoader):
    def __init__(self):
        self._example_data = examples.download_blood_vessels()
        _ExampleLoader.__init__(self)



@smproxy.source(name='PyVistaBlow', label='Blow')
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
class PyVistaBlow(_ExampleLoader):
    def __init__(self):
        self._example_data = examples.download_blow()
        _ExampleLoader.__init__(self)


@smproxy.source(name='PyVistaBoltNut', label='Bolt & Nut')
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
class PyVistaBoltNut(_ExampleLoader):
    def __init__(self):
        self._example_data = examples.download_bolt_nut()
        _ExampleLoader.__init__(self)


@smproxy.source(name='PyVistaBrain', label='Brain')
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
class PyVistaBrain(_ExampleLoader):
    def __init__(self):
        self._example_data = examples.download_brain()
        _ExampleLoader.__init__(self)


@smproxy.source(name='PyVistaBunny', label='Bunny')
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
class PyVistaBunny(_ExampleLoader):
    def __init__(self):
        self._example_data = examples.download_bunny()
        _ExampleLoader.__init__(self)


@smproxy.source(name='PyVistaCadModel', label='Cad Model')
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
class PyVistaCadModel(_ExampleLoader):
    def __init__(self):
        self._example_data = examples.download_cad_model()
        _ExampleLoader.__init__(self)



@smproxy.source(name='PyVistaCarotid', label='Carotid')
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
class PyVistaCarotid(_ExampleLoader):
    def __init__(self):
        self._example_data = examples.download_carotid()
        _ExampleLoader.__init__(self)


@smproxy.source(name='PyVistaCow', label='Cow')
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
class PyVistaCow(_ExampleLoader):
    def __init__(self):
        self._example_data = examples.download_cow()
        _ExampleLoader.__init__(self)


@smproxy.source(name='PyVistaCowHead', label='Cow Head')
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
class PyVistaCowHead(_ExampleLoader):
    def __init__(self):
        self._example_data = examples.download_cow_head()
        _ExampleLoader.__init__(self)


@smproxy.source(name='PyVistaNefertiti', label='Nefertiti')
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
class PyVistaNefertiti(_ExampleLoader):
    def __init__(self):
        self._example_data = examples.download_nefertiti()
        _ExampleLoader.__init__(self)


@smproxy.source(name='PyVistaLidar', label='Lidar')
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
class PyVistaLidar(_ExampleLoader):
    def __init__(self):
        self._example_data = examples.download_lidar()
        _ExampleLoader.__init__(self)


@smproxy.source(name='PyVistaTopo', label='Global Topography')
@smhint.xml('''<ShowInMenu category="%s"/>
    <RepresentationType view="RenderView" type="Surface" />''' % MENU_CAT)
class PyVistaTopo(_ExampleLoader):
    def __init__(self):
        self._example_data = examples.download_topo_global()
        _ExampleLoader.__init__(self)
