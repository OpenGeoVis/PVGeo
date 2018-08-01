"""PVGeo: an open-source python package for geoscientific visualization in VTK
and ParaView.
"""

import setuptools

__version__ = '1.1.11'

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="PVGeo",
    version=__version__,
    author="Bane Sullivan",
    author_email="info@pvgeo.org",
    description="Geoscientific visualization tools for VTK and ParaView",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OpenGeoVis/PVGeo",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy>=1.10',
        'scipy>=1.1',
        #'vtk>=8.1',
        'colour-runner==0.0.5',
        'codecov==2.0.15',
    ],
    classifiers=(
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Scientific/Engineering :: GIS',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
    ),
)
