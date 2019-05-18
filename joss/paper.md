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
  - name: Whitney J. Trainor-Guitton
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
visualization, yet the development of tools compatible with geoscience data and
models has been limited.
As a software extension package to VTK and ParaView, PVGeo addresses the lack of
geoscientific compatibility by creating a framework for geovisualization.
PVGeo aims to make the process of importing geoscience data into VTK based
software fluid and straightforward for users while providing a framework for new features
avoiding the typical, ambitious programming endeavor of building VTK software
plugins.
We have developed this code library, PVGeo, to link geoscientific data and
models with VTK-based 3D rendering environments like ParaView: an open-source
platform built on top of VTK [@pvguide].
Since VTK is an established and robust visualization platform, it provides
a rich toolbox of features common for visualization and spatial analysis across
disciplines [@vtkbook].
Examples of standard features include volume rendering, glyphing, subsetting,
K-Means clustering, volume interpolation, iso-contouring, and Virtual Reality
[@pvguide], [@vtkbook].
By linking geoscience to VTK and ParaView, geoscientists can harness all of the
native tools within ParaView, and other VTK powered libraries like ParaViewWeb
[@pvweb], VTK.js [@vtkjs], and PyVista [@pyvista] or extend that data into new
domains like Virtual Reality, as outlined in Figure 1.
PVGeo couples geoscientific information to software libraries at the forefront
of scientific visualization, which enables scientists to cost-effectively and
reproducibly communicate their findings.


![PVGeo providing a link for geoscience to the VTK and ParaView
realm of data visualization.](images/expansion-diagram.png)


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


Geoscientists often use specific visualization software for different data
processing routines which can lead to using several different visualization
environments for a single project.
Unfortunately, geoscientists are often left without a toolset for visual
integration across those different data types, like pairing well locations,
resource models, and geological models, which can hinder their ability to
interpret the spatial relationships of varying data types.


As authors of this software and geoscientists, we rely on calibrating and
integrating our data with all types of subsurface information to further
illuminate the value of geophysical imaging techniques.
This fosters a need for a visualization package to work seamlessly across
data types and formats that extends the functionality of an already
robust visualization platform like ParaView [@pvguide] or PyVista [@pyvista].
This visualization library is the PVGeo Python package; a free and open-source
library for integrating geoscientific datasets in a common rendering environment
to address various visualization and spatial analysis needs in geoscience.
The PVGeo package is powered by VTK [@vtkbook] and provides plugins for
ParaView, a user-friendly software environment for VTK.
As a pure-Python package, PVGeo is interoperable with other Python, VTK-based
software like the PyVista Python package [@pyvista].


There are various software available for geoscientific visualization; however,
these software often handle a few proprietary data formats and are closed-source
with licensing fees. Witter et al. [@witter] provides a comprehensive list and
discussion of the various software packages and finds that there are many
platforms available for integrated visualizations for limited data types.
Having the ability to visually fuse datasets, construct 3D models, or generate
horizons within the visualizations can be what separates closed-source software
from open-source software [@witter] - development of PVGeo aims to create an
open-source alternative for researchers.



## Mentions


Development for PVGeo is complemented by development for PyVista:
*3D plotting and mesh analysis through a streamlined interface for the Visualization Toolkit (VTK)*
[@pyvista].
PVGeo provides an extension package to PyVista linking data formats
and filtering routines common in geoscientific disciplines to PyVista's
generalized framework for 3D visualization.
PVGeo leverages PyVista to make the inputs and outputs of PVGeo algorithms more
accessible so that users can create compelling, integrated visualizations of
their work in a reproducible workflow.



## Acknowledgements

Funding: Newmont Mining Corporation supported this work, and we thank
Marcelo Godoy and Richard Inglis for collaboration on software development for
the ParaView platform.

We thank Jacob Grasmick (Colorado School of Mines) for his interest throughout
the project's inception and for providing sample datasets to demonstrate
PVGeo's filtering algorithms.



## References
