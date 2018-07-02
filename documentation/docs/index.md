# *PVGeo*

<script async defer src="http://slack.pvgeo.org/slackin.js?large"></script>

Welcome to the *PVGeo* website! Through visualization, we can bring value to data and hold the products of geoscience in a more intuitive light to interested parties. *PVGeo* is a code repository for visualizing geophysical data and this website documents the entire code base and includes several examples and tutorials of how to use the ParaView plugins delivered in this repo for common tasks in the visualization of geophysical data.


??? warning "Pre-Release Notice"
    This is a Beta release of the *PVGeo* code base and documentation. The plugins and Python modules might be changed in backward-incompatible ways and are not subject to any deprecation policy. The current documentation is a work in progress and we are trying our best to get everything fully documented by end of June 2018.

??? question "Suggestions?"
    If you have an idea for a macro, plugin, or would like to see how we would address a geoscientific visualization problem with ParaView, please post your thoughts on the [**issues page**](https://github.com/OpenGeoVis/PVGeo/issues).

??? tip "Where to get the code"
    All code is published on the GitHub repository *PVGeo* linked to this page. Click the 'PVGeo on GitHub' link on the right side of the menu bar at the top to find all of the code or you can follow [**this link**](https://github.com/OpenGeoVis/PVGeo).

??? tip "How to explore this documentation"
    *On a Desktop:* There are six main sections to this website shown in the navigation tab at the top of the page. Use these tabs to explore the different aspects of the project! Use the sidebar to the right to explore the contents of the current page and use the sidebar to the left to find all the different pages for this active section/tab. Here is an overview of each section:

    - **Overview:** An introduction to the project with installation details on how to get started.
    - **Plugin Suites:** A guide to all of the plugins we have implemented for use directly in ParaView. This section has all the information you will need to understand how to use our plugins and how we group them together into what we call *suites*. The code docs for the `PVGeo` module are included here.
    - **PV Macros:** A guide on how to use all of the macros developed in the `pvmacros` module. This section contains all of the code docs for the `pvmacros` module as well.
    - **Examples:** A series of exercises to demonstrate the use of different plugins and macros developed in `PVGeo` and `pvmacros` respectively.
    - **Resources:** A conglomerate of additional resources that are helpful when using ParaView for geoscientific applications.
    - **Development Guide:** This is an all encompassing guid on how to start making your own plugins as well as how to contribute to the *PVGeo* repository.


## Demo
Check out the [**Demo Page**](http://demo.pvgeo.org) to see video demos and interactive demos like the scene below. This is an example of three data sets visually integrated using our framework within ParaView then exported to a shareable format. Go ahead, click it and move it around!

<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="http://viewer.pvgeo.org?fileURL=https://dl.dropbox.com/s/6gxax6fp9muk65e/volc.vtkjs?dl=0" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>


-------

## About the Authors
The *PVGeo* code library is managed by [**Bane Sullivan**](http://banesullivan.com), graduate student in the Hydrological Science and Engineering interdisciplinary program at the Colorado School of Mines under Whitney Trainor-Guitton. If you have questions please inquire with [info@pvgeo.org](mailto:info@pvgeo.org) or join the *PVGeo* community on Slack: <script async defer src="http://slack.pvgeo.org/slackin.js"></script>


!!! info "Thank you to our contributors!"
    It is important to note the project is open source and that many features in this repository were made possible by contributors volunteering their time. Please take a look at the [**Contributors Page**](https://github.com/OpenGeoVis/PVGeo/graphs/contributors) to learn more about the developers of *PVGeo*.

------

## Documentation
All documentation for the code produced from this project is included on this website. The documentation contains an explanation of all of the produced plugins (filters, readers, sources, and sinks) and macros. Use the Sidebar to explore the documentation content and to find all documentation for plugins, macros, and more as you need. There are also details on how to [**build your own plugins**](./dev-guide/build-your-own-plugins.md), how to [**export data scenes**](./pvmacros/export/exportvtkjs.md), and transferring your complex data scenes into [**virtual reality**](./virtual-reality/entering-virtual-reality.md).

The purpose of including all this extra documentation is to provide a convenient location for geoscientists to learn how to tailor ParaView to their needs because data representation and communication are an integral part of success in science. To efficiently represent our spatial data is the first step to becoming successful and productive geoscientists. This is the principle behind why we are publishing this documentation along with the code in the repository. Not only do we want to communicate the effort and motivation for this project efficiently, but we want to empower others to communicate their scientific endeavors through spatial visualizations effectively.

<!--
### Plugin Documentation
There is a page dedicated to every plugin and on these pages, you will find implementation details, parameters, code quirks, and general usage information. We are working to have an example for every reader and filter so that users can get a feel for what is going on and how they might apply these plugins to address their needs. Since almost all geoscientific data is proprietary, these tutorials will likely come late so that we can find good open data sets and models that users can find outside of this repo for free.

### Macro documentation
Each macro produced in `pvmacros` will have a distinct purpose, be it to export isometric screenshots of any data scene or create various types of slices through a data volume. The macros will have broad applications and be formatted to work with generally any data scene or data of specific formats so that they can be easily expanded upon to complete specific tasks. For the macros, we will try to immediately have sample data and a tutorial upon publishing with documentation of what we are doing and why.

-->
