"""PVGeo: an open-source python package for geoscientific visualization in VTK
and ParaView.
"""

import setuptools
import warnings
import platform
import sys
import os

__version__ = '2.0.0'

with open("README.md", "r") as f:
    long_description = f.read()
    # Remove the icon from the README (assumes it is on the first line)
    idx = long_description.find('\n')
    long_description = '# *PVGeo*\n\n' + long_description[idx::]


# Manage requirements
install_requires=[
    'numpy>=1.13',
    'scipy>=1.1',
    'colour-runner==0.0.5',
    'codecov==2.0.15',
    'pandas>=0.23.4',
    'mock>=2.0.0',
    'espatools>=0.0.8',
    'pyvista>=0.20.1'
]

# add vtk if not windows and (not Python 3.x or not x64)
if os.name == 'nt' and (int(sys.version[0]) < 3 or '64' not in platform.architecture()[0]):
    warnings.warn('\nYou will need to install VTK manually.' +
                  '  Try using Anaconda.  See:\n'
                  + 'https://anaconda.org/anaconda/vtk')
else:
    install_requires.append(['vtk>=8.1'])

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
    install_requires=install_requires,
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*',
    extras_require={
        'pyproj': ['pyproj>=1.9'],
        'omf': ['omf>=0.9.3', 'omfvista>=0.2.0'],
        'discretize': ['discretize>=0.3.8'],
    },
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
