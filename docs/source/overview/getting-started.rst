Getting Started
===============

Using PVGeo in a Python Environment
-----------------------------------

If you'd like to use PVGeo in Python (>=3.6), then simply
install PVGeo to your active Python environment with ``pip``
or ``conda``

Install PVGeo via `pip <https://pypi.org/project/PVGeo/>`_::

    pip install PVGeo

Or with conda::

    conda install -c conda-forge pvgeo

Required dependencies
+++++++++++++++++++++

* `vtk <https://pypi.org/project/vtk/>`_
* `pyvista <https://pypi.org/project/pyvista/>`_
* `numpy <https://pypi.org/project/numpy/>`_
* `scipy <https://pypi.org/project/scipy/>`_
* `pandas <https://pypi.org/project/pandas/>`_
* `espatools <https://pypi.org/project/espatools/>`_


Optional dependencies
+++++++++++++++++++++

PVGeo has a few non-required dependencies that enable more algorithms and
features when available. All requirements can be found in the
`requirements.txt <https://github.com/OpenGeoVis/PVGeo/blob/main/requirements.txt>`_
file in the repo but the needed requirements for PVGeo to work will be installed
with PVGeo. Some useful dependencies:

- `discretize <https://pypi.org/project/discretize/>`_: Adds algorithms that harnesses ``discretize``'s finite volume code and file IO methods.
- `pyproj <https://pypi.org/project/pyproj/>`_: Adds algorithms that can perform coordinate transformations
- `omf <https://pypi.org/project/omf/>`_ and `omfvista <https://pypi.org/project/omfvista/>`_: Provides support for the Open Mining Format (OMF)
