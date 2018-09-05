.. PVGeo documentation master file, created by
   sphinx-quickstart on Tue Jul 10 19:56:04 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PVGeo's code docs!
=============================


.. image:: https://img.shields.io/travis/OpenGeoVis/PVGeo-Website/master.svg?label=website
   :target: http://pvgeo.org
   :alt: Website

.. image:: https://img.shields.io/pypi/v/PVGeo.svg?logo=python
   :target: https://pypi.org/project/PVGeo/
   :alt: PyPI

.. image:: https://api.codacy.com/project/badge/Grade/4b9e8d0ef37a4f70a2d02c0d53ed096f
   :target: https://www.codacy.com/app/banesullivan/PVGeo?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=OpenGeoVis/PVGeo&amp;utm_campaign=Badge_Grade
   :alt: Codacy Badge

.. image:: https://img.shields.io/badge/Slack-PVGeo-4B0082.svg?logo=slack
   :target: http://slack.pvgeo.org
   :alt: Slack

.. image:: https://img.shields.io/travis/OpenGeoVis/PVGeo/master.svg?label=build&logo=travis
   :target: https://travis-ci.org/OpenGeoVis/PVGeo
   :alt: Build Status

.. image:: https://codecov.io/gh/OpenGeoVis/PVGeo/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/OpenGeoVis/PVGeo/branch/master
   :alt: Code Coverage

.. image:: https://img.shields.io/github/contributors/OpenGeoVis/PVGeo.svg
   :target: https://GitHub.com/OpenGeoVis/PVGeo/graphs/contributors/
   :alt: GitHub Contributors

.. image:: https://img.shields.io/badge/docs%20by-gendocs-blue.svg
   :target: https://gendocs.readthedocs.io/en/latest/?badge=latest)
   :alt: Documentation Built by gendocs


The ``PVGeo`` python package contains VTK powered tools for data visualization in geophysics which are wrapped for direct use within the application `ParaView by Kitware`_. These tools are tailored to data visualization in the geosciences with a heavy focus on structured data sets like 2D or 3D time-varying grids.

This website hosts the code documentation for the ``PVGeo`` python package found
on `GitHub`_ and `PyPI`_. This website strictly documents the code so that users have a convenient and familiar means of searching through the library to understand the backend of the features they are using.
If you are searching for examples and demonstrations on how to use the ``PVGeo`` library, then head over to the `full website`_ where you can find tutorials with sample data sets and links to many other helpful resources.

For a quick overview of how ``PVGeo`` can be used in a Python environment or directly within ParaView, please checkout the code snippets and videos on the `About Examples Page`_.


.. _ParaView by Kitware: https://www.paraview.org
.. _GitHub: https://github.com/OpenGeoVis/PVGeo\
.. _PyPI: https://pypi.org/project/PVGeo/
.. _full website: http://pvgeo.org
.. _About Examples Page: http://pvgeo.org/examples/about-examples/



Requesting Features, Reporting Issues, and Contributing
-------------------------------------------------------

Please feel free to post features you would like to see from this package on the `issues page`_ as a feature request. If you stumble across any bugs or crashes while using code distributed here, please report it in the issues page so we can promptly address it. For other questions please join the `PVGeo community on Slack`_.

.. _issues page: https://github.com/OpenGeoVis/PVGeo/issues
.. _PVGeo community on Slack: http://slack.pvgeo.org

About the Authors
-----------------

The ``PVGeo`` code library is managed by `Bane Sullivan`_, graduate student in the Hydrological Science and Engineering interdisciplinary program at the Colorado School of Mines under Whitney Trainor-Guitton. If you would like to contact us, please inquire with `info@pvgeo.org`_.

.. _Bane Sullivan: http://banesullivan.com
.. _info@pvgeo.org: mailto:info@pvgeo.org

It is important to note the project is open source and that many features in this repository were made possible by contributors volunteering their time. Please take a look at the `Contributors Page`_ to learn more about the developers of ``PVGeo``.

.. _Contributors Page: https://github.com/OpenGeoVis/PVGeo/graphs/contributors

Getting Started
---------------

To begin using the ``PVGeo`` python package, create a new virtual environment and install ``PVGeo`` through pip.

.. code-block:: bash

    $ conda create -n PVGeoEnv27 python=2.7

    # Activate the virtual environment
    $ conda activate PVGeoEnv27

    # Install PVGeo
    (PVGeoEnv27) $ pip install PVGeo

    # Now install VTK>=8.1.0
    (PVGeoEnv27) $ pip install vtk

.. warning::

    Windows users: Please see installation instructions on `GitHub README`_.

.. _GitHub README: https://github.com/OpenGeoVis/PVGeo/#getting-started


Now ``PVGeo`` is ready for use in your standard python environment. To use the *PVGeo* library as plugins in `ParaView`_, please see the `detailed explanation here`_.

.. _ParaView: https://paraview.org
.. _detailed explanation here: http://pvgeo.org/overview/getting-started/
