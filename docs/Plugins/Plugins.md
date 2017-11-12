# The Argument for Using Python Programmable Filters
The development of plugins for the ParaView software platform can seem like a daunting task at first. Creating CMakeLists, writing in C++ again for the first time in years, learning XML to create interactive GUI components, and integrating the plugins into the ParaView build is a major turnoff. To get around all that, we can use something Kitware has put into ParaView for the rapid development of plugins, Python Programmable Filters and Sources! Python is an incredibly easy language to learn and most if not all geoscientists have experience working in Python. In this repo, we aim to produce all plugins in the Python Programmable Filters and Sources format for the following reasons:

* Rapid development: Through the templates, shell scripts, and XML converters provided in this repo, it is easy to prototype and develop a plugin for you needs in a matter of minutes
* Computational power: VTK has NumPy wrapping to allow for the use of Pythons complex numerical analysis libraries like SciPy and NumPy.
* Easy customization by end user: since most scientists know and use Python, they can easily dive into the source code delivered in this repo to tailor it to their needs
* Live source code editing in the ParaView program: toggle the advanced button on the properties panel and the Python source code for that filter pops up in real time for editing on the pipeline.
* Easy GUI component creation through the build scripting included in this repo

# Readers
A reader takes data from files and puts them into the proper VTK data structures so that we can make conversions and visualize on the ParaView pipeline. ParaView comes native with a plethora of data format readers but there are a million more formats out there in the world. So by creating formats for common geoscientific formats, we hope to make the process of getting data into the ParaView pipeline as simple as possible. We also are doing this to show how easy it is to make custom readers and convey the message that if you can dream it, we can code it! Whatever your data format, there is likely a VTK data structure perfect for it.


# Filters
A filter modifies, transforms, combines, analyses, etc. data on the ParaView pipeline. Filters provide a means for changing how we visualize data or create a means of taking some data and generating other data from that. For example we might have a series of scattered points that we know represent the center of a tunnel. We can use a filter to transform those points into a connected line that we then construct a tunnel around. This allows us to save out minimal data (just XYZ points as opposed to complex geometries that make up the tunnel) to our hard drive while still having complex visualizations from that data.
