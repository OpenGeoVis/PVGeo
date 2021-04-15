<a href="http://pvgeo.org"><img src="PVGeo_icon_horiz.png" width="35%" /></a>

Share this project: [![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=Check%20out%20this%20project%20for%20data%20and%20model%20visualization%20in%20ParaView&url=https://github.com/OpenGeoVis/PVGeo&hashtags=ParaView,PVGeo,visualization,geoscience)


The *PVGeo* Python package contains VTK powered tools for data visualization in
geophysics which are wrapped for direct use within the application
[ParaView by Kitware](https://www.paraview.org) or in a Python environment with
[**PyVista**](https://github.com/pyvista/pyvista). These tools are tailored to
data visualization in the geosciences with a heavy focus on structured data sets
like 2D or 3D time-varying grids.


**Learn More:**
[![DOI](http://joss.theoj.org/papers/10.21105/joss.01451/status.svg)](https://doi.org/10.21105/joss.01451)
[![Vimeo](https://img.shields.io/badge/demos-grey.svg?logo=vimeo)](https://vimeo.com/user82050125)
[![Slack Badge](https://img.shields.io/badge/Slack-PVGeo-4B0082.svg?logo=slack)](http://slack.pvgeo.org)

**Status:** [![PyPI](https://img.shields.io/pypi/v/PVGeo.svg?logo=python&logoColor=white)](https://pypi.org/project/PVGeo/)
[![Testing](https://github.com/OpenGeoVis/PVGeo/actions/workflows/test.yml/badge.svg)](https://github.com/OpenGeoVis/PVGeo/actions/workflows/test.yml)


**Metrics:**
[![GitHub contributors](https://img.shields.io/github/contributors/OpenGeoVis/PVGeo.svg?logo=github&logoColor=white)](https://GitHub.com/OpenGeoVis/PVGeo/graphs/contributors/)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/4b9e8d0ef37a4f70a2d02c0d53ed096f)](https://www.codacy.com/app/banesullivan/PVGeo?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=OpenGeoVis/PVGeo&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/OpenGeoVis/PVGeo/branch/master/graph/badge.svg)](https://codecov.io/gh/OpenGeoVis/PVGeo/branch/master)


## Demonstrations of *PVGeo*

For a quick overview of how  *PVGeo* can be used in a Python environment or
directly within ParaView, checkout the code snippets and videos on the
[**About Examples Page**](https://pvgeo.org/about-examples.html)



## Connections

This package provides many VTK-like algorithms designed for geoscientific data
formats and types to perform data integration and analysis.
To ensure our users have powerful and easy to use tools that can visualize the
results of PVGeo algorithms, we are actively involved in the development of
[**PyVista**](https://github.com/pyvista/pyvista): a toolset for easy access to
VTK data objects and 3D visualization in Python.
To learn more about pairing PVGeo with PyVista, please check out the
[**example Jupyter notebooks**](https://github.com/OpenGeoVis/PVGeo-Examples).


## Getting Started

To begin using the *PVGeo* Python package, create/activate your Python virtual
environment (we highly recommend using anaconda) and install *PVGeo* through pip:

```bash
pip install PVGeo
```

Now *PVGeo* is ready for use in your standard Python environment (2.7 or >=3.6)
with all dependencies installed! Go ahead and test your install:

```bash
python -c "import PVGeo; print(PVGeo.__version__)"
```

Note that Windows users must use Python >=3.6 when outside of ParaView.
Further insight can be found in the [**Getting Started Guide**](http://pvgeo.org/overview/getting-started.html).


## Report Issues and Contribute

Please feel free to post features you would like to see from this package on the
[**issues page**](https://github.com/OpenGeoVis/PVGeo/issues) as a feature
request.
If you stumble across any bugs or crashes while using code distributed here,
report them in the issues section so we can promptly address it.
For other questions, join the [***PVGeo* community on Slack**](http://slack.pvgeo.org).

Interested in contributing to PVGeo? Please see the [contributing guide](https://pvgeo.org/dev-guide/contributing.html)

## About the Authors [![Open Source](https://img.shields.io/badge/open--source-yes-brightgreen.svg)](https://opensource.com/resources/what-open-source)

The *PVGeo* code library was created and is managed by [**Bane Sullivan**](http://banesullivan.com),
graduate student in the Hydrological Science and Engineering interdisciplinary
program at the Colorado School of Mines under Whitney Trainor-Guitton.
If you would like to contact us, inquire with [**info@pvgeo.org**](mailto:info@pvgeo.org).

It is important to note the project is open source and that many features in
this repository were made possible by contributors volunteering their time.
Head over to the [**Contributors Page**](https://github.com/OpenGeoVis/PVGeo/graphs/contributors)
to learn more about the developers of *PVGeo*.


### Citing PVGeo

There is a [paper about PVGeo](https://doi.org/10.21105/joss.01451)!

If you are using PVGeo in your scientific research, please help our scientific
visibility by citing our work!

> Sullivan et al., (2019). PVGeo: an open-source Python package for geoscientific visualization in VTK and ParaView. Journal of Open Source Software, 4(38), 1451, https://doi.org/10.21105/joss.01451

See [CITATION.rst](https://github.com/OpenGeoVis/PVGeo/blob/master/CITATION.rst)
for more details.


## Linking PVGeo to ParaView

To use the *PVGeo* library as plugins in ParaView, please see the detailed
explanation [**here**](http://pvgeo.org/overview/getting-started) where you
must create a second isolated Python 2.7 environment that will host PVGeo for
ParaView.
