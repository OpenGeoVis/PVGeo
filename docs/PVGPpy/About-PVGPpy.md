!!! warning "This page is incomplete"
    There are a lot of pages in the documentation and we are trying to fill all content as soon as possible. Stay tuned for updates to this page

## The Argument for Using Python Programmable Filters
The development of plugins for the ParaView software platform can seem like a daunting task at first. Creating CMakeLists, writing in C++ again for the first time in years, learning XML to create interactive GUI components, and integrating the plugins into the ParaView build is a major turnoff. To get around all that, we can use something Kitware has put into ParaView for the rapid development of plugins, Python Programmable Filters and Sources! Python is an incredibly easy language to learn and most if not all geoscientists have experience working in Python. In this repo, we aim to produce all plugins in the Python Programmable Filters and Sources format for the following reasons:

* Rapid development: Through the templates, shell scripts, and XML converters provided in this repo, it is easy to prototype and develop a plugin for you needs in a matter of minutes
* Computational power: VTK has NumPy wrapping to allow for the use of Pythons complex numerical analysis libraries like SciPy and NumPy.
* Easy customization by end user: since most scientists know and use Python, they can easily dive into the source code delivered in this repo to tailor it to their needs
* Live source code editing in the ParaView program: toggle the advanced button on the properties panel and the Python source code for that filter pops up in real time for editing on the pipeline.
* Easy GUI component creation through the build scripting included in this repo

## Readers
A reader takes data from files and puts them into the proper VTK data structures so that we can make conversions and visualize on the ParaView pipeline. ParaView comes native with a plethora of data format readers but there are a million more formats out there in the world. So by creating formats for common geoscientific formats, we hope to make the process of getting data into the ParaView pipeline as simple as possible. We also are doing this to show how easy it is to make custom readers and convey the message that if you can dream it, we can code it! Whatever your data format, there is likely a VTK data structure perfect for it.


## Filters
A filter modifies, transforms, combines, analyses, etc. data on the ParaView pipeline. Filters provide a means for changing how we visualize data or create a means of taking some data and generating other data from that. For example we might have a series of scattered points that we know represent the center of a tunnel. We can use a filter to transform those points into a connected line that we then construct a tunnel around. This allows us to save out minimal data (just XYZ points as opposed to complex geometries that make up the tunnel) to our hard drive while still having complex visualizations from that data.


## PVGPpy
PVGPpy is a python module we are developing for direct use of our macros in the ParaView shell. This module will contain the bulk of our macros for your use. We are publishing our macros in this manner to:

1. Streamline their use by allowing users to call the macros like python functions directly from the ParaView shell.
2. Easily update/change the macros without constant merge conflictions as users will need to input specific parameters for their use. This is much easier to do with function calls than overwriting the macro files.


-------


## Macros vs. Scripts
<!--- TODO: we need more info here --->
We will from now on refer to macros as a set of standard codes that can be used regardless of data sets or scenes in ParaView. ParaView's sense of macro is not robust enough for us so that we will be referring to traditional macros in ParaView as 'scripts' from here on. Scripts will be used on specific sets of data whereas macros can be used on any set of data.

### Macros
Macros are Python codes that complete tedious or recurring tasks either in ParaView's GUI or ParaView's batch processing environment. We will use macros to complete everyday tasks like saving screenshots of isometric views of a data scene or tedious tasks like making many slices of a single data set along a line.

### Scripts
Scripts are Python codes we will use for tasks like loading scenes and for applying several macros at once. It is often helpful to set up a script for a project so that you can quickly run all the visualization processing at once each time you update your model files or create new versions of your data.


-------


## How to Run Scripts
Use the Python Shell from 'Tools->Python Shell' in the ParaView GUI. Do not import scripts as macros in ParaView as they become static in the ParaView GUI and make managing/changing quite difficult. To use scripts in the batch processing environment, use the `pvpython` program delivered in ParaView. On my OS X operating system it is under the `Applications/ParaView/Contents/bin/pvpython`. More info on all of this to come! <!-- TODO -->

To simply run the scripts in this repo, edit the script files under the `scripts/` directory for your use, then run them in ParaView by selecting 'Tools->Python Shell' then click 'Run Script'. Navigate to the `scripts/` directory in this repo and select the script you desire to use.


-------


## Make Your Own Scripts
!!! failure "Description to come!"
    There are a lot of pages in the documentation and we are trying to fill all content as soon as possible. Stay tuned for updates to this page
<!--- TODO --->

### Using the Trace Tool
<!--- TODO: how to make meaning of the trace output --->
!!! failure "Description to come!"
    There are a lot of pages in the documentation and we are trying to fill all content as soon as possible. Stay tuned for updates to this page

### Using PVPython
<!--- TODO: Batch processing --->
!!! failure "Description to come!"
    There are a lot of pages in the documentation and we are trying to fill all content as soon as possible. Stay tuned for updates to this page
