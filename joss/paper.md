---
title: 'PVGeo: an open-source Python package for geoscientific visualization in VTK and ParaView'
tags:
  - Python
  - visualization
  - 3D
  - geoscience
authors:
  - name: C. Bane Sullivan
    orcid: 0000-0001-8628-4566
    affiliation: 1
  - name: Whitney Trainor-Guitton
    orcid: 0000-0002-5726-3886
    affiliation: 1
affiliations:
 - name: Department of Geophysics, Colorado School of Mines, Golden, CO, USA
   index: 1

date: 18 February 2019
bibliography: paper.bib
---

# Summary

PVGeo is an open-source Python package for geoscientific visualization and
analysis, harnessing an already powerful software platform: the Visualization
Toolkit (VTK) and its front-end application, ParaView.
The VTK software platform is well-maintained, contains an expansive set of
native functionality, and provides a robust foundation for scientific
visualization, yet the development of tools compatible for geoscience data and
models has been limited.
As a software extension package to VTK and ParaView, PVGeo addresses the lack of
geoscientific compatibility by creating a framework for geovisualization.
PVGeo aims to make the process of importing geoscience data into VTK based
software simple and fluid for users while providing a framework for new features
avoiding the typical, ambitious programming endeavor of building VTK software
plugins.


~~This framework is a set of tools for visually integrating geoscience data and
models directly within a Python environment or ParaView's graphical user
interface, simplifying the required routines to make compelling visualizations
of geoscientific datasets.~~



## Background


The results of geophysical imaging techniques often hold high significance to
stakeholders yet the effective perception of those results remains a dynamic
challenge.
In the geosciences and especially the field of geophysics, researchers often
need 3D and 4D (time-varying) visualizations to understand complex spatial and
temporal relationships in data which are challenging to capture in 2D
visualizations [@witter].
Better perceptions or new understandings may arise from data when referenced in
relation to intuitive features like topography, well locations, survey points,
or other known information.
Through these spatial relations, geoscientists and stakeholders can directly
engage with their data to gain insight and begin to rapidly evaluate data and
models either on various 2D planes simultaneously or in a complex 3D environment
[@witter, @Carr1997].

We have developed a code library, PVGeo, to link geoscientific data and
models with VTK-based 3D rendering environments.
As authors of this software and geophysicists, we rely on calibrating and
integrating our data with all types of subsurface information to further
illuminate the value of geophysical imaging techniques.

Geoscientists often use specific visualization software for different data
processing routines which can lead to using several different visualization
environments for a single project.
Unfortunately, geoscientists are often left without a toolset for visual
integration across those different data types, like pairing well locations,
resource models, and geophysical data slices in \autoref{fig:integrated}, which
can hinder their ability to interpret the spatial relationships of varying data
types.

Geoscientists need a visualization package to work seamlessly across data types
and formats that extends the functionality of an already robust visualization
platform like ParaView.
This visualization library is the PVGeo Python package; a free and open-source
library for integrating geoscientific datasets in a common rendering environment
to address various visualization and spatial analysis needs in geoscience.
The PVGeo package is powered by the Visualization Toolkit (VTK) [@vtkbook] and
provides plugins for ParaView, a user-friendly software environment for VTK.


There are various packages available for geoscientific visualization; however,
these software often handle a few proprietary data formats and are closed-source
with licensing fees.
Witter et al. [@witter] provides a comprehensive list and discussion of the
various software packages and finds that there are many platforms available for
integrated visualizations for limited data types.
Having the ability to visually fuse datasets, construct 3D models, or generate
horizons within the visualizations can be what separates closed-source software
from open-source software [@witter].


## Why VTK & ParaView for Geoscience

ParaView is an open-source platform built on top of the Visualization Toolkit
(VTK) that can visualize 2D, 3D, and 4D (time-varying) datasets [@pvguide].
This software platform is scalable which allows ParaView to process multiple data
sets in parallel then later collect the results to yield a responsive graphics
environment with which a user can interact [@pvguide].
Since ParaView is an established and robust visualization platform, it provides
a rich toolbox of features common for visualization and spatial analysis across
disciplines [@pvguide].
Examples of standard features include volume rendering, glyphing, subsetting,
K-Means clustering, volume interpolation, iso-contouring, and Virtual Reality
[@pvguide].
By linking geoscience to VTK and ParaView, geoscientists can harness all of the
native tools within ParaView, and other VTK powered libraries like ParaViewWeb
[@pvweb] and VTK.js [@vtkjs], or extend that data into new domains like Virtual
Reality, as demonstrated in \autoref{fig:expansion-diagram}.
PVGeo couples geoscientific information to software libraries at the forefront
of scientific visualization, which enables scientists to cost-effectively
communicate their findings [@Carr1997].


![Expansion Diagram](images/expansion-diagram.png){width=100%}
**Figure 2**. How PVGeo links geoscience to the VTK and ParaView realm of data
visualization.


## Connections

Development for PVGeo is complemented by development for
[`vtki`](http://docs.vtki.org): a streamlined Python interface for the
visualization toolkit.
Leveraging `vtki`'s to access the VTK data structures that output from all PVGeo
algorithms, users can create compelling, integrated visualizations of their work




## Acknowledgements


# References
