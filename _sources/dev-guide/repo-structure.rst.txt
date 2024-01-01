Project Structure
=================

The Plugin Framework
--------------------


In developing the *PVGeo* repository, we decided to follow a framework of
development that generates various sets of tools that can be used within
ParaView or outside in other Python environments with the VTK Python library.
This would allow for users of *PVGeo* to be able to use all of the functionality
as plugins in ParaView with interactive user menus or outside of ParaView be
able to integrate with there existing data processing suites using Python and
VTK. This development framework also focuses heavily on the open source paradigm
in that *PVGeo* contains many base classes for developers to inherit
functionality to aid in the development of new features. Unfortunately, the
development of plugins for the ParaView software platform may imply an ambitious
programming endeavor, including creating CMakeLists, developing in lower level
programming languages like C++, learning new libraries to create interactive GUI
components, and building the plugins into the ParaView source code. However, the
*PVGeo* module takes advantage of functionality by Kitware that facilitates the
rapid development of readers, sources, filters, and writers: instantiations of
the ``VTKPythonAlgorithmBase`` class in Python. Python is an accessible language,
easy to learn, and popular among geoscientists using packages like: SimPEG,
ObsPy, EarthPy, pyFLOWGO, GeoNotebook, and more. We choose to develop the
*PVGeo* library to work well with other Python libraries by following the
following framework:

- **Extendable:** This software will harness the established and robust visualization platforms ParaView and VTK, extend their functionality, and remain open-source for contributions and integration into other Python powered geoscientific processing suites.
- **Safe:** The software must preserve data integrity and precision.
- **Dynamic:** The software must enable a dynamic link between external processing software and visualization libraries.
- **Modular:** The software will be modular so that various visualization suites can be implemented separately but also work together. This software should be usable both within and outside of ParaView.
- **Rapid development:** Through further subclasses of the ``VTKPythonAlgorithmBase`` class and the templates in *PVGeo*, it is easy to prototype and develop a plugin in a matter of minutes without the need to rebuild the software.
- **Computational power:** VTK has NumPy wrapping to allow for the use of Python's complex numerical analysis libraries like SciPy and NumPy.
- **Easy customization by end user:** since most geoscientists know and use Python, they can easily dive into the source code delivered in this repo to tailor it to their needs.
- **Easy GUI component creation:** Graphical User Interface elements can be easily produced to pair with plugins.



Outline of Goals
----------------

* Develop and document geoscientific plugins for ParaView encompassed in various suites. Each suite of plugins will be tailored to specific data formats and/or processing needs in geoscience. These plugins will take advantage of ParaView and VTK’s Python wrapping and use the Python Programmable Filter in ParaView. The advantage to using Python Programmable filters is that they are easily modified by the end user and can be wrapped in XML to create a GUI for its use in ParaView while having the option to directly edit the source code live in ParaView. The suites of plugins will consist of the following plugin types:

    * **Readers:** A reader puts data from files into proper ParaView data structures on the pipeline. These are plugins that read common geoscientific and geophysical spatial data files (GSLIB, UBC Tensor and OcTree meshes, etc.). Also make readers that read common raw data files (packed binary floats, delimited ASCII, etc.)

    * **Filters:** A filter modifies, transforms, combines, analyses, etc. data on the ParaView pipeline. Plugins that perform post-processing analysis of geoscientific data for visualization. For example, filters that build tubes from a series of points that represent a tunnel or filters that take a 1D array, reshape it to 2D or 3D, and make a volumetric model ready for visualization all while adding spatial reference for visual integration.

    * **Sources:** Plugins that create simple synthetic data sources that could be used for model generation. We are creating a suite of plugins for generating various types of discretized models/meshes which can be exported. Another example could include a sphere or cube with a specified attribute like a spatially varying density or electrical conductivity. Other sources might include using that synthetic sphere or cube to make a volumetric field of some response. These plugins will tailor to the educational needs in applications of this code base.

* Develop and document the ``PVGeo`` Python modules.

    * The ``PVGeo`` module will hold all of the code used in the plugins so that shared features across plugins can be called rather the rewritten and so that we can version control the plugins. This module will be primarily for use in the plugins scripts and not necessary for use in the ParaViewPython shell.

* Make tutorials on the use of the tools provided by this repository as well as share how to use ParaView's native features on open source data (for example):

* Develop customizable scripts for the visualization of common data formats. This will include developing scripts on an individual basis to help others quickly visualize their data and models for quality assessment and unique research needs.
