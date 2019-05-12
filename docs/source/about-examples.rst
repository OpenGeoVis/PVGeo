.. _About Examples Page:

About Examples
==============

`PVGeo` is deployed in various sub-packages called *suites*. These *suites*
consist of a set of reader, filter, source, or writer algorithms (or any
combination of those) for a general area of geoscientific processing and
visualization.
The following sections on this page demonstrate general procedures and syntax to
use each type of algorithm within ParaView or directly in a Python environment.

Take a look at the :ref:`ref_examples` for an outline of all the available
examples at this time.

If you think there may be a serious problem with an example, please open an
issue on the `issues page`_ so that we can promptly fix it.

.. _issues page: https://github.com/OpenGeoVis/PVGeo/issues


Typical Usage
-------------

All algorithms deployed in *PVGeo* are useable in the following manners in a
Python environment where the algorithm can be called and instantiated with
keyword arguments for its parameters and then applied on some input data set.

.. code-block:: python

    import PVGeo
    # PSEUDOCODE: Typical use of a PVGeo algorithm:
    output = PVGeo.suite.Algorithm(**kwargs).apply(input)


Or we can instantiate the algorithm for repetitive calls if, for example, we
need to request varying time steps.

.. code-block:: python

    import PVGeo
    # PSEUDOCODE: Typical use of a PVGeo algorithm:
    alg = PVGeo.suite.Algorithm(**kwargs)
    # Grab the output data object
    output = alg.apply(input)
    # Update the output to a desired time step
    alg.UpdateTimeStep(6.0)


Reader Algorithms
-----------------

A reader takes data from files and puts them into the proper VTK
data structures so that we can visualize that data on the VTK or ParaView
pipeline.
ParaView and `pyvista` come with a plethora of native data format readers but
there are still many more formats in the geosciences that have not been
implemented. By creating formats for common geoscientific formats, we hope to
make the process of getting data into the ParaView pipeline or into `pyvista`
data structures as simple as possible.


The file readers in *PVGeo* are available for use in the same manner as all
algorithms in *PVGeo*. Readers are typically used in a manner that allows the
reader algorithm to be repetitively called to request various time steps:

.. code-block:: python

    import PVGeo
    # PSEUDOCODE: Typical use of a PVGeo reader:
    reader = PVGeo.suite.Reader(**kwargs)
    reader.AddFileName(['file%.2d' % i for i in range(20)])

    # Grab the output data object
    output = reader.apply() # NOTE: Readers have no input for the `apply()` call

    # Update the output to a desired time step
    reader.UpdateTimeStep(6.0)


It is worth noting that if you have only one file (one time step) to read, then
readers can be used to immediately produce a data object:

.. code-block:: python

    import PVGeo
    # PSEUDOCODE: Typical use of a PVGeo reader:
    output = PVGeo.suite.Reader(**kwargs).apply('fname.txt')




ParaView Usage
++++++++++++++

The *PVGeo* readers aren't directly available in the GUI menus of ParaView but
rather a dialog will appear for you to select the desired file reader when
selecting **File -> Open...** within ParaView like the screen recording below:

.. raw:: html

    <iframe src="https://player.vimeo.com/video/281726394?loop=1&autoplay=0" width="640" height="400" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>



Filter Algorithms
-----------------

A filter modifies, transforms, combines, analyses, processes, etc. data in VTK
data structures on either a VTK or ParaView pipeline. Filters provide a means
for changing how we visualize data or create a means of generating topology for
an input data source to better represent that data in a 3D rendering environment.

For example, we have developed a filter called Voxelize Points
which takes a set of scattered points sampled on a rectilinear reference frame
and generates voxels for every point such that the volume of data made by the
points is filled with topologically connected cells.
Or for another filter, maybe we might have a series of scattered points that we
know represent the center of a tunnel or tube that represents a well. We can use
a filter to transform those points into a connected line that we then construct
a cylinder around. This allows us to save out minimal data (just XYZ points as
opposed to complex geometries that make up the tunnel) to our hard drive
while still having complex visualizations from that data.


Filters are typically used in a manner that parameters are set and an input
dataset is provided to immediately produce an output. The parameters/options of
the filter are set via the `**kwargs` upon construction and the input(s) is/are
given to the `apply()` call:



.. code-block:: python

    import PVGeo
    # PSEUDOCODE: Typical use of a PVGeo filter:
    output = PVGeo.suite.Filter(**kwargs).apply(inputDataObject)

.. code-block:: python

    import PVGeo
    # PSEUDOCODE: Typical use of a PVGeo filter with multiple inputs:
    output = PVGeo.suite.Filter(**kwargs).apply(input0, input1)


It is also worth noting that filter algorithms can be used as their own entities
to make repetitive calls on them much like we showed with readers:

.. code-block:: python

    import PVGeo
    # PSEUDOCODE: Typical use of a PVGeo filter:
    filt = PVGeo.suite.Filter(**kwargs)
    output = filt.apply(inputDataObject)

    # Change a parameter of the filter
    filt.set_parameter(True) # PSEUDOCODE
    filt.update() # Make sure to update the output after changing a parameter

    # Request a different time step
    filt.UpdateTimeStep(6.0)



ParaView Usage
++++++++++++++

Within ParaView, filters are available for selection directly from the GUI menus
when an input data source is selected on the pipeline. All of the *PVGeo*
filters  are available under their own categories in the **Filters** menu.

.. raw:: html

    <iframe src="https://player.vimeo.com/video/282010041?loop=1&autoplay=0" width="640" height="400" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>


Source Algorithms
-----------------

A source takes input parameters from a user and generates a data object for
visualization or export. In *PVGeo*, we have implemented the *Model Building*
suite with many sources that allow for a user to specify attributes of a data
set such as a model discretization and have a data source appear in the
rendering environment alongside their other data for that scene.


Sources can be used like any algorithm in *PVGeo* and are typically called to
immediately produce an output like below:

.. code-block:: python

    import PVGeo
    # PSEUDOCODE: Typical use of a PVGeo source:
    output = PVGeo.suite.Source(**kwargs).apply()



ParaView Usage
++++++++++++++

Within ParaView, sources are available for selection directly from the GUI
menus. All of the *PVGeo* sources are available under their own categories in
the **Sources** menu.

.. raw:: html

    <iframe src="https://player.vimeo.com/video/281726486?loop=1&autoplay=0" width="640" height="400" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>

Writer Algorithms
-----------------

*PVGeo* writers take VTK data structures and write them out to the disk in a
non-VTK formats that might be a standard for geoscientific data.
PVGeo readers are often deployed with their complimentary writer equivalents
such that data can be imported to the pipeline using readers, transformed using
filters, then output to the same format in memory for use in an external
processing library.

Writers can be used like any algorithm in *PVGeo* and are typically called to
immediately write out a data object like below.

.. code-block:: python

    import PVGeo
    # PSEUDOCODE: Typical use of a PVGeo writer:
    writer = PVGeo.suite.Writer(**kwargs)
    filename = 'test-writer.grd'
    writer.SetFileName(filename)
    writer.Write(inputDataObject)



ParaView Usage
++++++++++++++

Demonstrated in the following video, a user can select *File -> Save Data* in
ParaView with a selected dataset then choose one of *PVGeo*'s writers.
The first *1 minute* in the video demonstrates the *Extract Topography* then the
video shows how to save a ``vtkRectilinearGrid`` and its attributes to the UBC
Tensor Mesh/Model formats using a PVGeo writer.


.. raw:: html

    <iframe src="https://player.vimeo.com/video/284294249?loop=1&autoplay=0" width="640" height="480" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>
