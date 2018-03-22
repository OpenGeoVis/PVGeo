!!! warning "Pre-Release Notice"
    This is a Beta release of the ParaViewGeophysics code base and documentation. The plugins and Python modules might be changed in backward-incompatible ways and are not subject to any deprecation policy. The current documentation is a work in progress and may fall behind.

Welcome to the ParaViewGeophysics (PVGP) documentation! This website documents the code base we are making for data visualization in geophysics on the application ParaView by Kitware. Through visualization, we can bring value to data and hold the products of geoscience in a new light to interested parties.

This repository was produced from the work of an undergraduate research project at the Colorado School of Mines titled: Illuminating the Value of Geophysical Imaging through Visualization and Virtual Reality. Checkout [this PDF](https://drive.google.com/file/d/0B6v2US3m042-MFIwUy1uUTlfVHM/view?usp=sharing) standalone presentation to learn more about the project.


??? tip "How to explore this documentation"
    On a Desktop: Use the sidebar to the right to explore the contents of the current page and use the sidebar to the left to find all the different pages for this websote (readers & filters for ParaView are under 'Plugins & PVGPpy' while macros and code documentation for the `pvmacros` module are under the 'ParaView Macros' category). Explore around!

??? tip "Where to get the code"
    All code is published on the GitHub repository 'ParaViewGeophysics' linked to this page. Click the 'PVGP on GitHub' link on the right side of the menu bar at the top to find all of the code.


## Demo
Check out the data scene below. This is an example of three data sets visually integrated using our framework and exported to a shareable format. Go ahead, click it and move it around!

<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="https://rawgit.com/banesullivan/PVGPvtk.js/master/StandaloneSceneLoader.html?fileURL=https://dl.dropbox.com/s/6gxax6fp9muk65e/volc.vtkjs?dl=0" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>


-------

## About the Project
The primary goal of this project is to build plugins for the open-source, multi-platform, data analysis, and visualization application [ParaView](https://www.paraview.org) by Kitware. These plugins are tailored to the visualization of spatially referenced data in the geosciences. The overarching  goal of this project is to develop a framework to funnel geophysical data/models into virtual reality for the purpose of:

- Extracting Value of Information (VOI)
- User/Stakeholder engagement with geophysical findings
- Communicating uncertainty in an useable way

Our specific goal is to develop a heavily documented library of plugins, macros, and examples of how to view standard formats of geoscientific and geophysical data on the ParaView software platform. These plugins will provide tools to perform post-processing visual analysis and interpretation of geoscientific data and models.

Through the deployment of this software, geophysicists will gain an ability to represent their 3D spatially referenced data intuitively to interested parties and stakeholders. By integrating the visualization of various data, interested parties will gain insight into the value of the information in the models. A spatially defined 3D model yields minimal value to an outside party unless they can relate that model to other spatial features. For example, a 3D model of faults in the subsurface is unhelpful unless the location of known features to interested parties can be displayed simultaneously. To give a value of information, we must be able to show where the spatially referenced data is in relation to intuitive features like topography, well locations, survey points, or other known features. Through visual integration, we try to mimic the reality of the space in which data was acquired so that it will hold meaning to anyone that immerses into the visualization regardless of background.

??? abstract "SAGEEP 2018 Abstract"
    The results of geophysical imaging techniques often hold high significance to stakeholders in the problems addressed yet the effective perception of those results remains a dynamic challenge for all. To illuminate the value of geophysical imaging techniques, we are developing a framework to visually integrate geophysical data and models in 3D which extends into Virtual Reality (VR) as well as statistically analyzing interpretation advantages in VR. The motivation for this effort comes from a desire to directly engage stakeholders with geophysical data gaining Value of Information (VOI) and de-risking decision making in project planning. This framework is a code base that extends the functionality of the open-source visualization platform ParaView by Kitware. These extensions make it possible to visually integrate geophysical data in a multidimensional rendering space so that the end product is interpretable to non-geoscientists and that all parties can gain insight and VOI from geophysical imaging techniques. To show value in the VR presentation of multi-dimensional visualizations, we aim to develop metrics that will analyze the effectiveness of visual analysis in VR compared to traditional methods. We will evaluate these metrics through statistical gaming type protocol, where we will task subjects with making spatial decisions and finding features of interest in complex geoscientific scenes. We hypothesize that VR will bring the needed perception to most efficiently make spatial decisions and detect features of interest as well as convey information such as uncertainty in a usable manner. We will have preliminary results of the gaming protocol by March 2018 as well as share our visual framework along that journey in the form of a GitHub repository titled “ParaViewGeophysics.” Our goal in sharing the repository is to deliver a toolset that enables geophysicists to rapidly visualize their data and models as well as effectively communicate their findings to interested stakeholders.


### About the Author
<script type="text/javascript" src="https://platform.linkedin.com/badges/js/profile.js" async defer></script>

<div style="float: left; margin:10px 10px 10px 10px"" class="LI-profile-badge"  data-version="v1" data-size="large" data-locale="en_US" data-type="horizontal" data-theme="light" data-vanity="bane-sullivan"><a class="LI-simple-link" href='https://www.linkedin.com/in/bane-sullivan?trk=profile-badge'>Linkedin: Bane Sullivan</a></div>

Unless otherwise specified, all code and documentation distributed here were produced by [Bane Sullivan](http://banesullivan.com), undergraduate research assistant in the Geophysics Department at the Colorado School of Mines under Dr. Whitney J. Trainor-Guitton. Feel free to contact Bane for questions or for custom filters/readers to visualize geoscience data through the [Issues page](https://github.com/banesullivan/ParaViewGeophysics/issues)

<div style="float: left; margin:10px 10px 10px 10px"" </div>


## Outline of Goals
These are the goals to achieve through publishing this repository but not necessarily the goals of the research project from which this repository was developed.

* Develop and document geoscientific plugins for ParaView. These plugins will take advantage of ParaView and VTK’s Python wrapping and use the Python Programmable Filter in ParaView. The advantage to using Python Programmable filters is that they are easily modified by the end user and can be wrapped in XML to create a GUI for its use in ParaView while having the option to directly edit the source code live in ParaView.

    * **Readers:** Plugins that read common geoscientific and geophysical spatial data files (GSLIB, UBC mesh, ESRI grid, etc.). Also make readers that read common raw data files (packed binary floats, delimited ASCII, etc.)

    * **Filters:** Plugins that perform post-processing analysis of geoscientific data for visualization. For example, filters that build tubes from a series of points that represent a tunnel or filters that take a 1D array, reshape it to 2D or 3D, and make a volumetric model ready for visualization all while adding spatial reference for visual integration.  

    * **Sources:** Plugins that create simple synthetic data sources such as a sphere or cube with a specified attribute like a spatially varying density or electrical conductivity. Other sources might include using that synthetic sphere or cube to make a volumetric field of some response.

* Develop and document the `PVGPpy` and `pvmacros` Python modules for use in ParaView's Python Shell. These modules will contain all of the macros, batch processing tasks, and common codes to apply to 3D data scenes.

* Make tutorials on the use of ParaView's native features and the plugins distributed in this repository on open source data (for example):

    * Document explanations of how to get sophisticated geoscientific data formats like topography DEMs into a format ParaView can read.

     * Document how to use ParaView’s native filters to complete common tasks in the visualization of geoscientific data. For example, applying satellite imagery to a surface that represents topography.

* Develop customizable scripts for the visualization of common data formats. This will include developing scripts on an individual basis to help others quickly visualize their data and models for quality assessment and unique research needs.



-------


## Features to Come

Here is a list of features that are shortly coming to this repo. This list will be regularly updated. More documentation is soon to come. We want to do it right: with tutorials, example data, and detailed justification for need and use of each reader, filter, and macro.

!!! help "Suggestions?"
    Post on the [Issues page](https://github.com/banesullivan/ParaViewGeophysics/issues) as a feature request.

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

### Macros and Scripts
- [ ] How to start making your own scripts (tips, tricks, and general advice)
- [x] Save screenshots in isometric views, side, top, etc. in an automated fashion
- [x] [Many Slices Along Points:](pvmacros/vis/Many-Slices-Along-Points.md) Export slices of dataset along polyline at every point on that line (normal is the vector from that point to the next)
- [x] [Export a scene](pvmacros/export/exportVTKjs.md) to a shareable 3D format

### Examples and Other Docs
- Tutorials for each filter/reader/macro will be in their respective documentation.
- [ ] How to send data scenes made using the Readers, Filters, and Macros in this repository over to the Virtual Reality build of ParaView
- [ ] How to build your own plugins using this project's framework and build scripts
- [ ] Importing DEM topography (with/without satellite imagery)
- [ ] Slicing/cropping a data scene through all components/datasets (managing links)
- [x] [Slice Model Along PolyLine:](Examples/Slice-Model-Along-PolyLine.md) How to export a slice of a dataset projected on a vtkPolyLine (capabilities are currently present in ParaView)
