<a href="http://pvgeo.org"><img src="PVGeo_icon_horiz.png" width="35%" /></a>


[![Documentation Status](https://readthedocs.org/projects/pvgeo/badge/?version=latest)](http://docs.pvgeo.org/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/PVGeo.svg)](https://pypi.org/project/PVGeo/)
[![Slack Bage](https://img.shields.io/badge/Slack-PVGeo-4B0082.svg?logo=slack)](http://slack.pvgeo.org)
[![Build Status](https://travis-ci.org/OpenGeoVis/PVGeo.svg?branch=master)](https://travis-ci.org/OpenGeoVis/PVGeo)
[![AppVeyor](https://ci.appveyor.com/api/projects/status/it085qovtnb0mcgr/branch/master?svg=true)](https://ci.appveyor.com/project/banesullivan/pvgeo/branch/master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/4b9e8d0ef37a4f70a2d02c0d53ed096f)](https://www.codacy.com/app/banesullivan/PVGeo?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=OpenGeoVis/PVGeo&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/OpenGeoVis/PVGeo/branch/master/graph/badge.svg)](https://codecov.io/gh/OpenGeoVis/PVGeo/branch/master)

The *PVGeo* python package contains VTK powered tools for data visualization in geophysics which are wrapped for direct use within the application [ParaView by Kitware](https://www.paraview.org). These tools are tailored to data visualization in the geosciences with a heavy focus on structured data sets like 2D or 3D time-varying grids.

## Demonstrations of *PVGeo*

For a quick overview of how  *PVGeo* can be used in a Python environment or directly within ParaView, please checkout the code snippets and videos on the  [**About Examples Page**](http://pvgeo.org/examples/about-examples/)

Also, check out the [**demo page**](http://demo.pvgeo.org/) for a synopsis of the project and some visualization examples. Then check out the rest of the [**full website**](http://pvgeo.org/) to explore the technical aspects of the project and to find use examples.


## Report Issues and Contribute
Please feel free to post features you would like to see from this package on the [**issues page**](https://github.com/OpenGeoVis/PVGeo/issues) as a feature request. If you stumble across any bugs or crashes while using code distributed here, please report it in the issues section so we can promptly address it. For other questions please join the [***PVGeo* community on Slack**](http://slack.pvgeo.org).

## About the Authors [![GitHub contributors](https://img.shields.io/github/contributors/OpenGeoVis/PVGeo.svg)](https://GitHub.com/OpenGeoVis/PVGeo/graphs/contributors/) [![Open Source](https://img.shields.io/badge/open--source-yes-brightgreen.svg)](https://opensource.com/resources/what-open-source)

The *PVGeo* code library is managed by [**Bane Sullivan**](http://banesullivan.com), graduate student in the Hydrological Science and Engineering interdisciplinary program at the Colorado School of Mines under Whitney Trainor-Guitton. If you would like to contact us, please inquire with [**info@pvgeo.org**](mailto:info@pvgeo.org).

It is important to note the project is open source and that many features in this repository were made possible by contributors volunteering their time. Please take a look at the [**Contributors Page**](https://github.com/OpenGeoVis/PVGeo/graphs/contributors) to learn more about the developers of *PVGeo*.



# Getting Started

To begin using the *PVGeo* python package, create a new Python virtual environment and install *PVGeo* through pip.

```bash
# Please use Python 2.7
$ conda create -n PVGeoEnv27 python=2.7

$ conda activate PVGeoEnv27
(PVGeoEnv27) $ pip install PVGeo

```

**Non-Windows users:** Now you must install VTK to your virtual environment. For Linux and Mac users, simply install VTK through `pip`:

```bash

# Now install VTK
(PVGeoEnv27) $ pip install vtk

```

## Windows Users

PVGeo on Windows can be quite (*VERY*) tricky to setup, so please reference previous issues with the installation label and join the [**PVGeo community on Slack**](http://slack.pvgeo.org) for guidance.

Please proceed with the full instructions on the [**Getting Started**](http://pvgeo.org/overview/getting-started/) page.


## Linking PVGeo to ParaView

Now *PVGeo* is ready for use in your standard Python environment (non-Windows) and ready for use in PVGeo (All ). To use the *PVGeo* library as plugins in ParaView, please see the detailed explanation [**here**](http://pvgeo.org/overview/getting-started/).
