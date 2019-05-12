"""
Export
======

On this page, we demonstrate how to quickly share a 3D rendering of your
ParaView visualizations with anyone who has access to the internet so that that
can explore the whole scene in a dynamic manner.

Motivation
----------
In order to effectively communicate our geoscientific findings, we often need to
share our 3D visualizations with interested stakeholders. These interested
parties are likely not going to have ParaView or other visualization software
at hand. Thus we desire to have a means to export our complex visualizations in
ParaView to a simple, shareable format that anyone can view. To accomplish this,
we will take advantage of vtk.js and its standalone web viewer for vtk.js
formats.

Would not it be great to send your client or interested parties an interactive
3D scene of your Geophysical findings like the example below?

.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
            <iframe src="http://tunnels.pvgeo.org/" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>



VTK.js
------

`vtk.js <https://kitware.github.io/vtk-js/>`_ is a rendering library made for
scientific visualization on the web. This code base brings high performance
rendering into anyone's web browser. This library allows us to export complex
scenes from ParaView and share them with anyone that has a web browser like
Safari or Google Chrome.

The vtk.js library has an open-source `standalone scene viewer <https://kitware.github.io/vtk-js/examples/StandaloneSceneLoader/StandaloneSceneLoader.html>`_
which they have a `nice demo <https://kitware.github.io/vtk-js/examples/StandaloneSceneLoader.html>`_.
The first link can either be downloaded as an HTML file to be ran locally, or
you can go to that link and run from the vtk.js server. vtk.js also published a
scene export macro for ParaView that compresses a data scene in ParaView to a
shareable format for viewing on the web. The `macro from the vtk.js library <https://raw.githubusercontent.com/Kitware/vtk-js/master/Utilities/ParaView/export-scene-macro.py>`_
can be used but we also deploy an updated (we think more robust) version of
this export macro in the sub-module `export` of our Python module `pvmacros`.

Demo Shareable Format
+++++++++++++++++++++

Here are some samples to demonstrate the web viewer which we host on
`viewer.pyvista.org <http://viewer.pyvista.org>`_. We have included a few of our
scenes and one of the vtk.js sample scenes for you to demo:

- `Fluvial Channels <http://viewer.pyvista.org/?fileURL=https://dl.dropbox.com/s/qnahdwedjwndo7t/fluvsim_channels.vtkjs?dl=0>`_
- `Volcano <http://volcano.pvgeo.org>`_
- `Ripple <http://ripple.pvgeo.org>`_
- `Tunnels <http://tunnels.pvgeo.org>`_
- `vtk.js Sample Scene <http://viewer.pyvista.org/?fileURL=https://data.kitware.com/api/v1/file/587003c38d777f05f44a5c93/download>`_



Example Use
-----------

First, make a complex scene in ParaView that you might like to share with someone.
Now that you have your scene loaded, open the python shell from'View->Python Shell'
(or 'Tools->Python Shell' depending on your ParaView version) within ParaView.
From here, import our Python module delivered in the repository called
``#!py pvmacros``. From the ``#!py export`` sub-module, there is a function called
``#!py def exportVTKjs()`` which takes two optional arguments (`FileName` string
and `compress` boolean). Execute this function and note the output text as it
will describe where the exported scene was saved.

.. code-block:: python

    ## Import our ParaView Macros module:
    import pvmacros as pvm

    ## Now run the exportVTKjs script from the export sub-module
    pvm.export.exportVTKjs(FileName='test_export')


Now open the standalone web viewer by opening `viewer.pyvista.org <http://viewer.pyvista.org>`_

Select the exported scene as the input file for the web viewer from where you
saved it (should be under ``~/Dropbox/PVGeo_vtkjs/``). The export macro should
have printed out the location of the saved scene in the Python Shell.

If you have trouble post on our `issues page <https://github.com/OpenGeoVis/PVGeo/issues>`_
or read the `vtk.js documentation <https://kitware.github.io/vtk-js/examples/StandaloneSceneLoader.html>`_


How to Share
------------

To share these exported scenes with non-technical stakeholders, we recommend the
following processes:

Quick and Easy
++++++++++++++

- Create your scene and export to the vtk.js format (follow process above)
- Quality control your visualization by viewing in web browser yourself (follow process above)
- Send an email with your visualization (``*.vtkjs`` file) and something along the lines of:

.. code-block:: text

    Check out the data scene/model by downloading the attached file.
    Then go to the link below and open that downloaded file.

    `http://viewer.pyvista.org/ <http://viewer.pyvista.org>`_


A Bit More Robust
+++++++++++++++++

Sometimes we might want to give someone a direct link to the web visualization
so all they have to do is open the link on any device and they can see our
visualization. Here is a method to share scenes that have a slightly easier
process of viewing the file for the end user and will handle the case for mobile
platforms.

Unfortunately, making the experience for the end user simple means making your
experience a bit more complicated. You will need to host your file on a web
service like GitHub or Dropbox *(we have been unsuccessful in getting Google
Drive to work)*. Then get a public link to the `*.vtkjs` file on that web
service and append it to the web viewer URL.

We have created a Python script to generate these links for you if you are
sharing your data file on either Dropbox or GitHub. The script is delivered
in the repository.

The easiest way that we have found is to share the files on Dropbox.
Use the desktop client for Dropbox and right-click your exported `*.vtkjs` file
and select "Copy Dropbox Link."

Once you have that link, use the this script on your URLs in this manner:


.. code-block:: bash

    ## Usage:
    python get_vtkjs_url.py <web file host> <file link>

    ## Dropbox example:
    python get_vtkjs_url.py dropbox "https://www.dropbox.com/s/6m5ttdbv5bf4ngj/ripple.vtkjs?dl=0"



.. raw:: html

    <iframe src="https://player.vimeo.com/video/257833915" width="640" height="360" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>
    <p><a href="https://vimeo.com/257833915">PVGeo Export Demo</a> from <a href="https://vimeo.com/user82050125">Bane Sullivan</a> on <a href="https://vimeo.com">Vimeo</a>.</p>

"""

from .vtkjs import *

__displayname__ = 'Export'
