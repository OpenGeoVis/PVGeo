# About Plugin Suites
We are deploying our ParaView plugins in various packages we call suites. These suites consists of a series of reader or filter plugins (or both) for a general area of geoscientific processing or visualization. For example, we have created a suite called *UBC Mesh Tools* which contains file readers for the UBC Mesh types and filters for processes related to the UBC mesh formats. Another example of a suite is *Model Building*; this is a suite of various plugins that allow a user to create various types of models interactively within ParaView. Take a look at the navigation pane to the left to explore the different plugin suites.


## The Plugin Framework

### Why Programmable Plugins?
The development of plugins for the ParaView software platform can seem like a daunting task at first. Creating CMakeLists, writing in C++ again for the first time in years, learning XML to create interactive GUI components, and integrating the plugins into the ParaView build is a major turnoff. To get around all that, we can use something Kitware has put into ParaView for the rapid development of plugins, Python Programmable Filters and Sources! Python is an incredibly easy language to learn and most if not all geoscientists have experience working in Python. In this repo, we aim to produce all plugins in the Python Programmable Filters and Sources format for the following reasons:

* **Rapid development:** Through the templates, shell scripts, and XML converters provided in this repo, it is easy to prototype and develop a plugin for your needs in a matter of minutes.
* **Computational power:** VTK has NumPy wrapping to allow for the use of Pythons complex numerical analysis libraries like SciPy and NumPy.
* **Easy customization by end user:** since most scientists know and use Python, they can easily dive into the source code delivered in this repo to tailor it to their needs.
* **Live source code editing in the ParaView program:** toggle the advanced button on the properties panel and the Python source code for that filter pops up in real time for editing on the pipeline.
* **Easy GUI component creation:** XML GUI elements can be easily produced through the build scripting included in this repo.

### Readers
A reader takes data from files and puts them into the proper VTK and ParaView data structures so that we can visualize that data on the ParaView pipeline. ParaView comes with a plethora of native data format readers but there are still many more formats in the geosciences that have not been implemented. By creating formats for common geoscientific formats, we hope to make the process of getting data into the ParaView pipeline as simple as possible.

We are doing this to show how easy it is to make custom readers and convey the message: *if you can dream it, we can code it!* Whatever your data format, there is likely a VTK data structure perfect for it which we will write a reader to get your data into while preserving data precision and integrity. We also want to strongly emphasize that there should be a data reader for your format needs because data can loose its integrity when you save out various static copies through conversion scripts. Our readers will read your working data sets and help you simplify your data management during visualization while maintaining data precision.



### Filters
A filter modifies, transforms, combines, analyses, etc. data on the ParaView pipeline. Filters provide a means for changing how we visualize data or create a means of taking some data and generating other data from that. For example we might have a series of scattered points that we know represent the center of a tunnel or tube that represents a well. We can use a filter to transform those points into a connected line that we then construct a cylinder around. This allows us to save out minimal data (just XYZ points as opposed to complex geometries that make up the tunnel) to our hard drive while still having complex visualizations from that data.


### Sources
A source creates simple synthetic data sources such as a sphere or cube with a specified attribute like a spatially varying density or electrical conductivity. Other sources might include using that synthetic sphere or cube to make a volumetric field of some response. These plugins will tailor to the educational needs in applications of this code base. More details to come!



### About `PVGPpy`
PVGPpy is a python module we are developing to modulize all functionality common throughout the plugins. This module will contain the bulk of our code for file readers and visual filters. We are publishing the plugins code base in this manner so that we can easily update/change the code with minor deprecation issues.
