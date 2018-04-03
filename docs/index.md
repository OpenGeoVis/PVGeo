# ParaViewGeophysics
Welcome to the ParaViewGeophysics (PVGP) documentation! Through visualization, we can bring value to data and hold the products of geoscience in a more intuitive light to interested parties. ParaViewGeophysics is a code repository for visualizing geophysical data and this website documents the entire code base and includes several examples and tutorials of how to use this code base to for common tasks in the visualization of geophysical data.

<!-- #TODO: SAGEEP presentation
This repository was produced from the work of an undergraduate research project at the Colorado School of Mines titled: Illuminating the Value of Geophysical Imaging through Visualization and Virtual Reality. Checkout [this PDF](https://drive.google.com/file/d/0B6v2US3m042-MFIwUy1uUTlfVHM/view?usp=sharing) standalone presentation to learn more about the project.

-->
!!! warning "Pre-Release Notice"
    This is a Beta release of the ParaViewGeophysics code base and documentation. The plugins and Python modules might be changed in backward-incompatible ways and are not subject to any deprecation policy. The current documentation is a work in progress and we are trying our best to get everything fully documented by May 2018.

!!! info "Suggestions?"
    If you have an idea for a macro, plugin, or would like to see how we would address a geoscientific visualization problem with ParaView, please post your thoughts on the [issues page](https://github.com/banesullivan/ParaViewGeophysics/issues).

??? tip "How to explore this documentation"
    On a Desktop: Use the sidebar to the right to explore the contents of the current page and use the sidebar to the left to find all the different pages for this website (readers & filters for ParaView are under 'Plugins & PVGPpy' while macros and code documentation for the `pvmacros` module are under the 'ParaView Macros' category). Explore around!

??? tip "Where to get the code"
    All code is published on the GitHub repository 'ParaViewGeophysics' linked to this page. Click the 'PVGP on GitHub' link on the right side of the menu bar at the top to find all of the code.


## Demo
Check out the [Demo Page](http://demo.pvgp.io) to see a project overview, video demos, and interactive demos like the scene below. This is an example of three data sets visually integrated using our framework and exported to a shareable format. Go ahead, click it and move it around!

<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="https://rawgit.com/banesullivan/PVGPvtk.js/master/StandaloneSceneLoader.html?fileURL=https://dl.dropbox.com/s/6gxax6fp9muk65e/volc.vtkjs?dl=0" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>


-------

## About the Project
This code base is full of plugins and macros for the open-source, multi-platform, data analysis, and visualization application [ParaView](https://www.paraview.org) by Kitware. These plugins are tailored to the visualization of spatially referenced data in the geosciences, especially geophysics. The overarching  goal of this project is to develop set of codes to visually integrate post-processed data for more *intuitive* visualization. To make more intuitive visualizations, we think it is necessary to reference data in relation to features like topography, well locations, survey points, or other known features that are easier to spatially grasp.

This code base deploys tools to perform post-processing visual analysis and interpretation of geophysical data and models and we hope that geophysicists will gain an ability to represent their 3D spatially referenced data intuitively to interested parties and stakeholders. By integrating the visualization of various data, and creating a sort of visual data fusion, interested parties will gain insight into the value of the information in their models. Through visual integration, we try to mimic the reality of the space in which data was acquired so that it will hold meaning to anyone that immerses into the visualization regardless of background.

??? abstract "SAGEEP 2018 Abstract"
    The results of geophysical imaging techniques often hold high significance to stakeholders in the problems addressed yet the effective perception of those results remains a dynamic challenge for all. To illuminate the value of geophysical imaging techniques, we are developing a framework to visually integrate geophysical data and models in 3D which extends into Virtual Reality (VR) as well as statistically analyzing interpretation advantages in VR. The motivation for this effort comes from a desire to directly engage stakeholders with geophysical data gaining Value of Information (VOI) and de-risking decision making in project planning. This framework is a code base that extends the functionality of the open-source visualization platform ParaView by Kitware. These extensions make it possible to visually integrate geophysical data in a multidimensional rendering space so that the end product is interpretable to non-geoscientists and that all parties can gain insight and VOI from geophysical imaging techniques. To show value in the VR presentation of multi-dimensional visualizations, we aim to develop metrics that will analyze the effectiveness of visual analysis in VR compared to traditional methods. We will evaluate these metrics through statistical gaming type protocol, where we will task subjects with making spatial decisions and finding features of interest in complex geoscientific scenes. We hypothesize that VR will bring the needed perception to most efficiently make spatial decisions and detect features of interest as well as convey information such as uncertainty in a usable manner. We will have preliminary results of the gaming protocol by March 2018 as well as share our visual framework along that journey in the form of a GitHub repository titled “ParaViewGeophysics.” Our goal in sharing the repository is to deliver a toolset that enables geophysicists to rapidly visualize their data and models as well as effectively communicate their findings to interested stakeholders.


### About the Author
<script type="text/javascript" src="https://platform.linkedin.com/badges/js/profile.js" async defer></script>

<div style="float: left; margin:10px 10px 10px 10px"" class="LI-profile-badge"  data-version="v1" data-size="large" data-locale="en_US" data-type="horizontal" data-theme="light" data-vanity="bane-sullivan"><a class="LI-simple-link" href='https://www.linkedin.com/in/bane-sullivan?trk=profile-badge'>Linkedin: Bane Sullivan</a></div>

Unless otherwise specified, all code and documentation distributed here were produced by [Bane Sullivan](http://banesullivan.com), undergraduate research assistant in the Geophysics Department at the Colorado School of Mines under Dr. Whitney J. Trainor-Guitton. Feel free to contact Bane for questions through his contact information on [his website](http://banesullivan.com) or for custom filters/readers to visualize geoscience data through the [Issues page](https://github.com/banesullivan/ParaViewGeophysics/issues)

<div style="float: left; margin:10px 10px 10px 10px"> </div>


## Outline of Goals

* Develop and document geoscientific plugins for ParaView. These plugins will take advantage of ParaView and VTK’s Python wrapping and use the Python Programmable Filter in ParaView. The advantage to using Python Programmable filters is that they are easily modified by the end user and can be wrapped in XML to create a GUI for its use in ParaView while having the option to directly edit the source code live in ParaView.

    * **Readers:** A reader puts data from files into proper ParaView data structures on the pipeline. These are plugins that read common geoscientific and geophysical spatial data files (GSLIB, UBC mesh, etc.). Also make readers that read common raw data files (packed binary floats, delimited ASCII, etc.)

    * **Filters:** A filter modifies, transforms, combines, analyses, etc. data on the ParaView pipeline. Plugins that perform post-processing analysis of geoscientific data for visualization. For example, filters that build tubes from a series of points that represent a tunnel or filters that take a 1D array, reshape it to 2D or 3D, and make a volumetric model ready for visualization all while adding spatial reference for visual integration.  

    * **Sources:** Plugins that create simple synthetic data sources such as a sphere or cube with a specified attribute like a spatially varying density or electrical conductivity. Other sources might include using that synthetic sphere or cube to make a volumetric field of some response. These plugins will tailor to the educational needs in applications of this code base.

* Develop and document the `PVGPpy` and `pvmacros` Python modules for use in ParaView's Python Shell. These modules will contain all of the macros, batch processing tasks, and common codes to apply to 3D data scenes.

    * The `PVGPpy` module will hold all of the code used in the plugins so that shared features across plugins can be called rather the rewritten and so that we can version control the plugins. This module will be primarily for use in the plugins scripts and not necessary for use in the ParaViewPython shell.

    * The `pvmacros` module with be full of macros and other data-independent scripts that can be used directly in the ParaViewPython shell.

* Make tutorials on the use of the tools provided by this repository as well as share how to use ParaView's native features on open source data (for example):

* Develop customizable scripts for the visualization of common data formats. This will include developing scripts on an individual basis to help others quickly visualize their data and models for quality assessment and unique research needs.



-------


## Features to Come

Here is a list of features that are shortly coming to this repo. This list will be regularly updated. More documentation is soon to come. We want to do it right: with tutorials, example data, and detailed justification for need and use of each reader, filter, and macro.

!!! help "Suggestions?"
    We need **your** suggestions for what kinds of file format readers to make as well as ideas for filters to meet your data needs. Post on the [Issues page](https://github.com/banesullivan/ParaViewGeophysics/issues) as a feature request.

### Readers
- [ ] **Open Mining Format:** All file types and data types found [here](https://github.com/GMSGDataExchange/omf)
- [ ] **UBC Mesh:** both 2D and 3D. Details [here](https://www.eoas.ubc.ca/ubcgif/iag/sftwrdocs/technotes/faq.htm#mesh) and [here](https://gif.eos.ubc.ca/software/utility_programs#3DmodelsMeshes). We're almost done with this!
- [ ] **Well logs:** Readers for common formats (LAS) and easy ways to project well logs in XYZ space

<!---
- [ ] **ESRI Grid:** Details [here](https://en.wikipedia.org/wiki/Esri_grid) and [here](http://desktop.arcgis.com/en/arcmap/10.3/manage-data/raster-and-images/esri-grid-format.htm)
- [ ] **ESRI shape files:** Details [here](https://www.esri.com/library/whitepapers/pdfs/shapefile.pdf) and [here](https://en.wikipedia.org/wiki/Shapefile)
-->

### Filters
- [x] **Append Model to UBC Mesh:** This will load a model file and tag it on to vtkStructuredGrid loaded from a UBC Mesh reader. Think of it as appending models as attributes to the 3D mesh.
- [ ] **Extract Array:** This will allow you to extract any array from any data structure as vtkPolyData.
- [ ] **Transpose Grid:** Transpose or swap axii of grid data sets (vtkImageData and vtkRectilinearGrid)
- [x] **Reshape Table:** Adding ability to reshape using Fortran ordering on the currently available filter.
- [ ] **Make Cubes from Point Set:** This will take a point set and generate cube of some specified size at every point

<!---
**Structure Point Set:** This will take scattered point data and create connectivity/structure either in the form of hexahedrons or quads. More info to come.
-->
### Macros in `pvmacros`
- [x] Save screenshots in isometric views, side, top, etc. in an automated fashion
- [x] [Many Slices Along Points:](pvmacros/vis/Many-Slices-Along-Points.md) Export slices of dataset along polyline at every point on that line (normal is the vector from that point to the next)
- [x] [Export a scene](pvmacros/export/exportVTKjs.md) to a shareable 3D format

### Scripts
- [ ] How to start making your own scripts (tips, tricks, and general advice)
- [ ] A few sample scripts to set up tutorial environments.

### Examples and Other Docs
- Tutorials for each filter/reader/macro will be in their respective documentation.
- [ ] How to send data scenes made using the Readers, Filters, and Macros in this repository over to the Virtual Reality build of ParaView
- [ ] How to build your own plugins using this project's framework and build scripts
- [ ] Importing DEM topography (with/without satellite imagery)
- [ ] Slicing/cropping a data scene through all components/datasets (managing links)
- [x] [Slice Model Along PolyLine:](Examples/Slice-Model-Along-PolyLine.md) How to export a slice of a dataset projected on a vtkPolyLine (capabilities are currently present in ParaView)
