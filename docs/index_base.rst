#############################
Welcome to PVGeo's code docs!
#############################


.. image:: http://joss.theoj.org/papers/10.21105/joss.01451/status.svg
   :target: https://doi.org/10.21105/joss.01451


.. image:: https://img.shields.io/badge/demos-grey.svg?logo=vimeo
   :target: https://vimeo.com/user82050125)
   :alt: Vimeo

.. image:: https://img.shields.io/pypi/v/PVGeo.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/PVGeo/
   :alt: PyPI

.. image:: https://api.codacy.com/project/badge/Grade/4b9e8d0ef37a4f70a2d02c0d53ed096f
   :target: https://www.codacy.com/app/banesullivan/PVGeo?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=OpenGeoVis/PVGeo&amp;utm_campaign=Badge_Grade
   :alt: Codacy Badge

.. image:: https://img.shields.io/badge/Slack-PVGeo-4B0082.svg?logo=slack
   :target: http://slack.pvgeo.org
   :alt: Slack

.. image:: https://github.com/OpenGeoVis/PVGeo/actions/workflows/test.yml/badge.svg
   :target: https://github.com/OpenGeoVis/PVGeo/actions/workflows/test.yml
   :alt: Testing Status

.. image:: https://codecov.io/gh/OpenGeoVis/PVGeo/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/OpenGeoVis/PVGeo/branch/main
   :alt: Code Coverage

.. image:: https://img.shields.io/github/contributors/OpenGeoVis/PVGeo.svg?logo=github&logoColor=white
   :target: https://GitHub.com/OpenGeoVis/PVGeo/graphs/contributors/
   :alt: GitHub Contributors

.. image:: https://img.shields.io/badge/docs%20by-gendocs-blue.svg
   :target: https://gendocs.readthedocs.io/en/latest/?badge=latest)
   :alt: Documentation Built by gendocs


The ``PVGeo`` Python package contains VTK powered tools for data visualization
in geophysics which are wrapped for direct use within the application
`ParaView by Kitware`_ or directly in a Python >=3.6 environment when paired
with the `PyVista Python package`_.
These tools are tailored to data visualization in the geosciences with a heavy
focus on structured data sets like 2D or 3D time-varying grids.

This website hosts the documentation for the ``PVGeo`` Python package found
on `GitHub`_ and `PyPI`_.

For a quick overview of how ``PVGeo`` can be used in a Python environment or
directly within ParaView, please checkout the code snippets and videos on the
:ref:`About Examples Page`.


.. _ParaView by Kitware: https://www.paraview.org
.. _GitHub: https://github.com/OpenGeoVis/PVGeo\
.. _PyPI: https://pypi.org/project/PVGeo/
.. _PyVista Python package: http://docs.pyvista.org


Connections
-----------

This package provides many VTK-like algorithms designed for geoscientific data
formats and types to perform data integration and analysis.
To ensure our users have powerful and easy to use tools that can visualize the
results of PVGeo algorithms, we are actively involved in the development of
PyVista_: a toolset for easy access to
VTK data objects and 3D visualization in Python.
To learn more about pairing PVGeo with `PyVista`, please check out the
`example Jupyter notebooks`_.


.. _PyVista: https://github.com/pyvista/pyvista
.. _example Jupyter notebooks: https://github.com/OpenGeoVis/PVGeo-Examples


Requesting Features, Reporting Issues, and Contributing
-------------------------------------------------------

Please feel free to post features you would like to see from this package on the
`issues page`_ as a feature request. If you stumble across any bugs or crashes
while using code distributed here, please report it in the issues page so we can
promptly address it. For other questions please join the
`PVGeo community on Slack`_.

.. _issues page: https://github.com/OpenGeoVis/PVGeo/issues
.. _PVGeo community on Slack: http://slack.pvgeo.org

About the Authors
-----------------

The ``PVGeo`` code library was created and is managed by `Bane Sullivan`_,
graduate student in the Hydrological Science and Engineering interdisciplinary
program at the Colorado School of Mines under Whitney Trainor-Guitton.
If you would like to contact us, please inquire with `info@pvgeo.org`_.

.. _Bane Sullivan: http://banesullivan.com
.. _info@pvgeo.org: mailto:info@pvgeo.org

It is important to note the project is open source and that many features in
this repository were made possible by contributors volunteering their time.
Please take a look at the `Contributors Page`_ to learn more about the
developers of ``PVGeo``.

.. _Contributors Page: https://github.com/OpenGeoVis/PVGeo/graphs/contributors

.. include:: ../../CITATION.rst

Getting Started
---------------

To begin using the ``PVGeo`` Python package, create/activate your Python virtual
environment (we highly recommend using anaconda) and install ``PVGeo`` through
pip:

.. code-block:: bash

    pip install PVGeo


Now ``PVGeo`` is ready for use in your standard python environment. To use the
*PVGeo* library as plugins in `ParaView`_, please see the
`detailed explanation here`_.

.. _ParaView: https://paraview.org
.. _detailed explanation here: http://pvgeo.org/overview/getting-started/
