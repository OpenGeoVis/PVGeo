# *PVGeophysics*

??? tip "How to explore this documentation"
    *On a Desktop:* There are six main sections to this website shown in the navigation tab at the top of the page. Use these tabs to explore the different aspects of the project! Use the sidebar to the right to explore the contents of the current page and use the sidebar to the left to find all the different pages for this active section/tab. Here is an overview of each section:

    - **Home:** An introduction to the project with installation details on how to get started.
    - **Plugins & PVGPpy:** A guide to all of the plugins we have implemented for use directly in ParaView. This section has all the information you will need to Understand how to use our plugins. The code docs for the `PVGPpy` module are included here.
    - **PV Macros:** A guide on how to use all of the macros developed in the `pvmacros` module. This section contains all of the code docs for the `pvmacros` module as well.
    - **Examples:** A series of exercises to demonstrate the use of different plugins and macros developed in `PVGPpy` and `pvmacros` respectively.
    - **Resources:** A conglomerate of additional resources that are helpful when using ParaView for geoscientific applications.
    - **Development Guide:** This is an all encompassing guid on how to start making your own plugins as well as how to contribute to the *PVGeophysics* repository.

Welcome to the *PVGeophysics* (PVGP) documentation! Through visualization, we can bring value to data and hold the products of geoscience in a more intuitive light to interested parties. *PVGeophysics* is a code repository for visualizing geophysical data and this website documents the entire code base and includes several examples and tutorials of how to use this code base to for common tasks in the visualization of geophysical data.

<!-- #TODO: SAGEEP presentation
This repository was produced from the work of an undergraduate research project at the Colorado School of Mines titled: Illuminating the Value of Geophysical Imaging through Visualization and Virtual Reality. Checkout [**this PDF**](https://drive.google.com/file/d/0B6v2US3m042-MFIwUy1uUTlfVHM/view?usp=sharing) standalone presentation to learn more about the project.

-->
!!! warning "Pre-Release Notice"
    This is a Beta release of the *PVGeophysics* code base and documentation. The plugins and Python modules might be changed in backward-incompatible ways and are not subject to any deprecation policy. The current documentation is a work in progress and we are trying our best to get everything fully documented by June 2018.

!!! question "Suggestions?"
    If you have an idea for a macro, plugin, or would like to see how we would address a geoscientific visualization problem with ParaView, please post your thoughts on the [**issues page**](https://github.com/banesullivan/PVGeophysics/issues).

!!! tip "Where to get the code"
    All code is published on the GitHub repository *PVGeophysics* linked to this page. Click the 'PVGP on GitHub' link on the right side of the menu bar at the top to find all of the code or you can follow [**this link**](https://github.com/banesullivan/PVGeophysics).


## Demo
Check out the [**Demo Page**](http://demo.pvgp.io) to see a project overview, video demos, and interactive demos like the scene below. This is an example of three data sets visually integrated using our framework and exported to a shareable format. Go ahead, click it and move it around!

<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="http://gpvis.org?fileURL=https://dl.dropbox.com/s/6gxax6fp9muk65e/volc.vtkjs?dl=0" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>


-------

## About the Project
This code base is full of plugins and macros for the open-source, multi-platform, data analysis, and visualization application [**ParaView**](https://www.paraview.org) by Kitware. These plugins are tailored to the visualization of spatially referenced data in the geosciences, especially geophysics. The overarching  goal of this project is to develop set of codes to visually integrate post-processed data for more *intuitive* visualization. To make more intuitive visualizations, we think it is necessary to reference data in relation to features like topography, well locations, survey points, or other known features that are easier to spatially grasp.

This code base deploys tools to perform post-processing visual analysis and interpretation of geophysical data and models and we hope that geophysicists will gain an ability to represent their 3D spatially referenced data intuitively to interested parties and stakeholders. By integrating the visualization of various data, and creating a sort of visual data fusion, interested parties will gain insight into the value of the information in their models. Through visual integration, we try to mimic the reality of the space in which data was acquired so that it will hold meaning to anyone that immerses into the visualization regardless of background.

??? abstract "SAGEEP 2018 Abstract"
    The results of geophysical imaging techniques often hold high significance to stakeholders in the problems addressed yet the effective perception of those results remains a dynamic challenge for all. To illuminate the value of geophysical imaging techniques, we are developing a framework to visually integrate geophysical data and models in 3D which extends into Virtual Reality (VR) as well as statistically analyzing interpretation advantages in VR. The motivation for this effort comes from a desire to directly engage stakeholders with geophysical data gaining Value of Information (VOI) and de-risking decision making in project planning. This framework is a code base that extends the functionality of the open-source visualization platform ParaView by Kitware. These extensions make it possible to visually integrate geophysical data in a multidimensional rendering space so that the end product is interpretable to non-geoscientists and that all parties can gain insight and VOI from geophysical imaging techniques. To show value in the VR presentation of multi-dimensional visualizations, we aim to develop metrics that will analyze the effectiveness of visual analysis in VR compared to traditional methods. We will evaluate these metrics through statistical gaming type protocol, where we will task subjects with making spatial decisions and finding features of interest in complex geoscientific scenes. We hypothesize that VR will bring the needed perception to most efficiently make spatial decisions and detect features of interest as well as convey information such as uncertainty in a usable manner. We will have preliminary results of the gaming protocol by March 2018 as well as share our visual framework along that journey in the form of a GitHub repository titled “PVGeophysics.” Our goal in sharing the repository is to deliver a toolset that enables geophysicists to rapidly visualize their data and models as well as effectively communicate their findings to interested stakeholders.


### About the Author
<script type="text/javascript" src="https://platform.linkedin.com/badges/js/profile.js" async defer></script>

<div style="float: left; margin:10px 10px 10px 10px"" class="LI-profile-badge"  data-version="v1" data-size="large" data-locale="en_US" data-type="horizontal" data-theme="light" data-vanity="bane-sullivan"><a class="LI-simple-link" href='https://www.linkedin.com/in/bane-sullivan?trk=profile-badge'>Linkedin: Bane Sullivan</a></div>

The code and documentation distributed here were produced by [**Bane Sullivan**](http://banesullivan.com), graduate student in the Hydrological Science and Engineering interdisciplinary program at the Colorado School of Mines under Dr. Whitney J. Trainor-Guitton. Feel free to contact Bane through his contact information on [**his website**](http://banesullivan.com) for questions or through the [**issues page**](https://github.com/banesullivan/PVGeophysics/issues) for custom filters/readers to visualize geoscience data.

<div style="float: left; margin:10px 10px 10px 10px"> </div>


!!! info "Thank you to our contributors!"
    It is important to note the project is open source and that many features in this repository were made possible by contributors volunteering their time. The following people deserve many thanks and acknowledgments for their contributions:

    - [**Daan van Vugt**](https://github.com/Exteris)
    - [**Gudni Karl Rosenkjaer**](https://github.com/grosenkj)


## Outline of Goals

* Develop and document geoscientific plugins for ParaView. These plugins will take advantage of ParaView and VTK’s Python wrapping and use the Python Programmable Filter in ParaView. The advantage to using Python Programmable filters is that they are easily modified by the end user and can be wrapped in XML to create a GUI for its use in ParaView while having the option to directly edit the source code live in ParaView.

    * **Readers:** A reader puts data from files into proper ParaView data structures on the pipeline. These are plugins that read common geoscientific and geophysical spatial data files (GSLIB, UBC Tensor and OcTree meshes, etc.). Also make readers that read common raw data files (packed binary floats, delimited ASCII, etc.)

    * **Filters:** A filter modifies, transforms, combines, analyses, etc. data on the ParaView pipeline. Plugins that perform post-processing analysis of geoscientific data for visualization. For example, filters that build tubes from a series of points that represent a tunnel or filters that take a 1D array, reshape it to 2D or 3D, and make a volumetric model ready for visualization all while adding spatial reference for visual integration.  

    * **Sources:** Plugins that create simple synthetic data sources such as a sphere or cube with a specified attribute like a spatially varying density or electrical conductivity. Other sources might include using that synthetic sphere or cube to make a volumetric field of some response. These plugins will tailor to the educational needs in applications of this code base.

* Develop and document the `PVGPpy` and `pvmacros` Python modules for use in ParaView's Python Shell. These modules will contain all of the macros, batch processing tasks, and common codes to apply to 3D data scenes.

    * The `PVGPpy` module will hold all of the code used in the plugins so that shared features across plugins can be called rather the rewritten and so that we can version control the plugins. This module will be primarily for use in the plugins scripts and not necessary for use in the ParaViewPython shell.

    * The `pvmacros` module with be full of macros and other data-independent scripts that can be used directly in the ParaViewPython shell.

* Make tutorials on the use of the tools provided by this repository as well as share how to use ParaView's native features on open source data (for example):

* Develop customizable scripts for the visualization of common data formats. This will include developing scripts on an individual basis to help others quickly visualize their data and models for quality assessment and unique research needs.


------

## Documentation
All documentation for the code produced from this project is included on this website. The documentation contains an explanation of all of the produced plugins (filters and readers) and macros. Use the Sidebar to explore the documentation content and to find all documentation for readers, filters, macros, and more as you need. There are also details on how to [**build your own plugins**](./Dev-Guide/Build-Your-Own-Plugins.md), how to [**export data scenes**](./pvmacros/export/exportVTKjs.md), and transferring your complex data scenes into [**virtual reality**](./Virtual-Reality/Entering-Virtual-Reality.md).

The purpose of including all this extra documentation is to provide a convenient location for geoscientists to learn how to tailor ParaView to their needs because data representation and communication are an integral part of success in science. To efficiently represent our spatial data is the first step to becoming successful and productive geoscientists. This is the principle behind why we are publishing this documentation along with the code in the repository. Not only do we want to communicate the effort and motivation for this project efficiently, but we want to empower others to communicate their scientific endeavors through spatial visualizations effectively.

### Plugin Documentation
There is a page dedicated to every plugin in the respective readers and filters categories. On these pages, you will find implementation details, parameters, code quirks, and general usage information. We are working to have an example for every reader and filter so that users can get a feel for what is going on and how they might apply these plugins to address their needs. Since almost all geoscientific data is proprietary, these tutorials will likely come late so that we can find good open data sets and models that users can find outside of this repo for free.

### Macro documentation
Each macro produced in `pvmacros` will have a distinct purpose, be it to export isometric screenshots of any data scene or create various types of slices through a data volume. The macros will have broad applications and be formatted to work with generally any data scene or data of specific formats so that they can be easily expanded upon to complete specific tasks. For the macros, we will try to immediately have sample data and a tutorial upon publishing with documentation of what we are doing and why.
