# *PVGeo*

[![docs](https://img.shields.io/badge/docs-built-blue.svg)](http://pvgeo.org) [![Open Source](https://img.shields.io/badge/open--source-yes-brightgreen.svg)](https://opensource.com/resources/what-open-source) [![PyPI](https://img.shields.io/pypi/v/PVGeo.svg)](https://pypi.org/project/PVGeo/) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/4b9e8d0ef37a4f70a2d02c0d53ed096f)](https://www.codacy.com/app/banesullivan/PVGeo?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=OpenGeoVis/PVGeo&amp;utm_campaign=Badge_Grade) [![Slack Bage](http://slack.pvgeo.org/badge.svg)](http://slack.pvgeo.org) [![Build Status](https://travis-ci.org/OpenGeoVis/PVGeo.svg?branch=master)](https://travis-ci.org/OpenGeoVis/PVGeo) [![codecov](https://codecov.io/gh/OpenGeoVis/PVGeo/branch/master/graph/badge.svg)](https://codecov.io/gh/OpenGeoVis/PVGeo/branch/master) [![GitHub contributors](https://img.shields.io/github/contributors/OpenGeoVis/PVGeo.svg)](https://GitHub.com/OpenGeoVis/PVGeo/graphs/contributors/)

This repository contains plugins tailored to data visualization in geophysics for the application [ParaView by Kitware](https://www.paraview.org). These plugins are tailored to data visualization in the geosciences with a heavy focus on structured data sets like 2D or 3D time-varing grids.

Check out the [**demo page**](http://demo.pvgeo.org/) for a synopsis of the project and some visualization examples. Then check out the [**docs pages**](http://pvgeo.org/) to explore the motivation for publishing this repo as well as to find all code documentation. This contains documentation for readers, filters, macros, and more as you need. **NOTE: These are currently out of date and will be updated and finished by end of July 2018**

## About the Authors
The *PVGeo* code library is managed by [**Bane Sullivan**](http://banesullivan.com), graduate student in the Hydrological Science and Engineering interdisciplinary program at the Colorado School of Mines under Whitney Trainor-Guitton. If you would like to contact us, please inquire with [**info@pvgeo.org**](mailto:info@pvgeo.org).

It is important to note the project is open source and that many features in this repository were made possible by contributors volunteering their time. Please take a look at the [**Contributors Page**](https://github.com/OpenGeoVis/PVGeo/graphs/contributors) to learn more about the developers of *PVGeo*.


## Requesting Features, Reporting Issues, and Contributing
Please feel free to post features you would like to see from this repo on the [**Issues page**](https://github.com/OpenGeoVis/PVGeo/issues) as a feature request. If you stumble across any bugs or crashes while using code distributed here, please report it in the Issues section so we can promptly address it. For other questions please join the [***PVGeo* community on Slack**](http://slack.pvgeo.org).


# Getting Started
To begin using the *PVGeo* python package, create a new virtual environment and install *PVGeo* through pip.

```bash
$ conda create -n PVGeoEnv python=2.7

# Install VTK through conda as this is OS-independent
$ conda install -n PVGeoEnv vtk

$ source activate PVGeoEnv
(PVGeoEnv) $ pip install PVGeo

# Test the install on non-Windows OS
(PVGeoEnv) $ python -m PVGeo test
```

Now *PVGeo* is ready for use in your standard python environment. To use the *PVGeo* library as plugins in ParaView, please see the detailed explanation [here](http://pvgeo.org/overview/getting-started/).
