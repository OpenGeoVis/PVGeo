# Welcome to the ParaView for Geophysics wiki!

#### *NOTICE:* This wiki is under development and may currently lack content.

This repository is all about using ParaView in the geosciences for data and model visualization. Through visualization, we can bring value to data and hold the products of geoscience in a new light to interested parties.

This repository was produced from the work of an undergraduate research project at the Colorado School of Mines titled: Illuminating the Value of Geophysical Imaging through Visualization and Virtual Reality. Checkout [this PDF](https://drive.google.com/file/d/0B6v2US3m042-dzBSR1laSXdiYlU/view?usp=sharing) standalone presentation to learn more about the project.

Use the [Wiki Contents](Wiki-Contents) to explore the Wiki and to find all documentation for readers, filters, macros, and more as you need.


<img src="figs/indo_clip.png" height="200"/> <img src="figs/vel2_iso.png" height="200"/>

## Purpose
The primary goal of this project is to build plugins for the open-source, multi-platform, data analysis, and visualization application [ParaView](https://www.paraview.org) by Kitware. These plugins are tailored to the visualization of spatially referenced data in the geosciences. The overarching  goal of this project is to develop a framework to funnel geophysical data/models into virtual reality for the purpose of:
- Extracting Value of Information (VOI)
- User/Stakeholder engagement with geophysical findings
- Communicating uncertainty in an useable way

My specific goal is to develop a heavily documented library of plugins, macros, and examples of how to view standard formats of geoscientific and geophysical data on the ParaView software platform. These plugins will provide tools to perform post-processing visual analysis and interpretation of geoscientific data and models.

Through the deployment of this software, geophysicists will gain an ability to represent their 3D spatially referenced data intuitively to interested parties and stakeholders. By integrating the visualization of various data, interested parties will gain insight into the value of the information in the models. A spatially defined 3D model yields minimal value to an outside party unless they can relate that model to other spatial features. For example, a 3D model of faults in the subsurface is unhelpful unless the location of known features to interested parties can be displayed simultaneously. To give a value of information, we must be able to show where the spatially referenced data is in relation to intuitive features like topography, well locations, survey points, or other known features. Through visual integration, we try to mimic the reality of the space in which data was acquired so that it will hold meaning to anyone that immerses into the visualization regardless of background.

-------
### Outline of Goals:
These are the goals to achieve through publishing this repository but not necessarily the goals of the research project from which this repository was developed.

* Develop and document geoscientific plugins for ParaView. These plugins will take advantage of ParaView and VTK’s Python wrapping and use the Python Programmable Filter in ParaView. The advantage to using Python Programmable filters is that they are easily modified by the end user and can be wrapped in XML to create a GUI for its use in ParaView while having the option to directly edit the source code live in ParaView.

    * Readers: Plugins that read common geoscientific and geophysical spatial data files (GSLIB, UBC mesh, ESRI grid, etc.). Also make readers that read common raw data files (packed binary floats, delimited ASCII, etc.)

    * Filters: Plugins that perform post-processing analysis of geoscientific data for visualization. For example, filters that build tubes from a series of points that represent a tunnel or filters that take a 1D array, reshape it to 2D or 3D, and make a volumetric model ready for visualization all while adding spatial reference for visual integration.  

    * Sources: Plugins that create simple synthetic data sources such as a sphere or cube with a specified attribute like a spatially varying density or electrical conductivity. Other sources might include using that synthetic sphere or cube to make a volumetric field of some response.

* Make tutorials on the use of ParaView's native features and the plugins distributed in this repository on open source data (for example):

    * Document explanations of how to get sophisticated geoscientific data formats like topography DEMs into a format ParaView can read.

     * Document how to use ParaView’s native filters to complete common tasks in the visualization of geoscientific data. For example, applying satellite imagery to a surface that represents topography.

* Develop customizable macros for the visualization of common data formats. This will include developing macros on an individual basis to help others quickly visualize their data and models for quality assessment and individual research needs.
