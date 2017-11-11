# ParaView Geophysics Plugins
This repository contains plugins for the open-source, multi-platform data analysis, and visualization application [ParaView by Kitware](https://www.paraview.org). These plugins are tailored to data visualization in the geosciences with a heavy focus on structured data sets like 2D or 3D grids.

Check out the [Docs pages](http://paraviewgeophysics.readthedocs.io/) to explore the motivation for publishing this repo as well as to find all documentation and some visualization examples. This contains documentation for readers, filters, macros, and more as you need.

Also checkout [this PDF](https://drive.google.com/file/d/0B6v2US3m042-MFIwUy1uUTlfVHM/view?usp=sharing) standalone presentation about the project.

*NOTICE:* This repo is under development as the project just started! Consider everything here to be an Alpha (soon to be Beta) release.

## About the Author
Unless otherwise specified at the top of the file, all code and documentation distributed here were produced by [Bane Sullivan](https://github.com/banesullivan/), undergraduate research assistant in the Geophysics Department at the Colorado School of Mines under Dr. Whitney J. Trainor-Guitton. Feel free to contact Bane for questions or for custom filters/readers to visualize geoscience data through the [Issues page](https://github.com/banesullivan/ParaViewGeophysics/issues)


-----
# More to come
Stay tuned; this project is in its early stages of development, so only a handful of the plugins are tested and published here. Also be sure to out the [Docs pages](http://paraviewgeophysics.readthedocs.io/) (*currently being developed and proofed*) for detailed documentation on the filters and general use of this repository.

## Requesting Features, Reporting Issues, and Contributing
Please feel free to post features you would like to see from this repo on the [Issues page](https://github.com/banesullivan/ParaViewGeophysics/issues) as a feature request. If you stumble across any bugs or crashes while using code distributed here, please report it in the Issues section so we can promptly address it.

If you have your own plugins either developed in C++ or as python programmable filters for which you would like a nice GUI, please share it so this can be a one-stop place for geoscience plugins to ParaView!


-------
# How To Use the Plugins in this Repository
Here we will outline everything you need to do in one spot to quickly install these plugins and get working. If you encounter trouble or you are a windows user, please read through the detailed explanation [here](http://paraviewgeophysics.readthedocs.io/en/latest/Getting-Started/Install-Plugins/)

## Quick and Easy Unix Installation

First, declare a `PVPATH` variable in your your `~/.bash_profile`. This is the path to the installation of ParaView. We need this path so that the installation script can make symbolic links between this repository and your installation of ParaView.

```bash
# edit your ~/.bash_profile with vim or some text editor
$ vi ~/.bash_profile

# Be sure to check that this path matches yours... Odds are it's different!
# Path to the ParaView installation:
export PVPATH="/Applications/ParaView-5.4.0.app"
```

Now clone the repository and get to work using our code:

```bash
# Clone this repository
$ git clone https://github.com/banesullivan/ParaViewGeophysics
# Go into the repository
$ cd ParaViewGeophysics
# Install everything!
$ sh ./install.sh
```

After executing the above tasks, you should be ready to go. The most common issue is having the incorrect `PVPATH` variable in your `~/.bash_profile`, so be sure to check that if errors arise. A more step-by-step process is [here](http://paraviewgeophysics.readthedocs.io/en/latest/Getting-Started/Install-Plugins/).


-----
# Make Your Own Filters and Readers
A detailed explanation can be found in the [Docs](http://paraviewgeophysics.readthedocs.io/en/latest/Plugins/Build-Your-Own-Plugins/) but here is a quick run through:

To make a custom filter or reader, follow the outline in [src/example.py](src/example.py) and place your script in either the `src/filters/` or `src/readers/` directories with a meaningful name. *Note* that the script will only compile `.py` files that contain either `filter_` or `reader_` in the file name. This is so you can save other `.py` files in those directories without issues. Then re-run the script  [src/build_plugins.sh](src/build_plugins.sh) to wrap in XML and install to ParaView.

All of the distributed filters in this repo will appear in the menu category `CSM Geophysics Filters`. As you develop your own, it may be useful to specify your own menu category as the variable `FilterCategory` in your python file as shown in [src/example.py](src/example.py).

```py
FilterCategory = 'CSM Geophysics Filters'
```
