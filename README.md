# ParaView Geophysics Plugins
This repository contains plugins for the open-source, multi-platform data analysis and visualization application [ParaView by Kitware](https://www.paraview.org). These plugins are tailored to data visualization in the geosciences with a heavy focus on structured data sets like 2D or 3D grids.

## About the Author
Unless otherwise specified at the top of the file, all code and documentation distributed here was produced by [Bane Sullivan](https://github.com/banesullivan/), undergraduate research assistant in the Geophysics Department at the Colorado School of Mines. Feel free to contact for major questions or for custom filters/readers to visualize geoscience data.

## More to come!

Stay tuned, this project is in its early stages of development. Also be sure to check out the wiki page for detailed documentation on the filters and general use of this repository. *Currently being developed and proofed*


## Before You Do Anything!!

You *MUST* change the `PVPATH` variable in `src/install_plugins.sh` This variable is likely different depending on your OS and your version of ParaView. On MacOS, simply just replace `/ParaView-5.4.0.app/` with the name of your version of ParaView under `/Applications/`.


## To Build and Install the Filters in this Repository

### Building the Plugins

In the `src/` directory, there are two shell scripts. `build_plugins.sh` will build up the XML Server Manager Configuration filters from the `.py` scripts and install them. Only use this script if you are making your own filters or readers. If you run this script, it will build and install all filters and readers to ParaView.

### Installing the Plugins to ParaView

To simply install the distributed filters from this repo, run the `install_plugins.sh` script *but first you MUST change the `PVPATH` variable* (described above)! This script will simply copy over all the XML files from `build/` to the default directory for third party plugins in ParaView so that they will all load when ParaView launches.

To run these scripts on a Unix like system us the `sh` command: `sh src/install_plugins.py`


## Make Your Own Filters and Readers

To make a custom filter or reader, follow the outline in `src/example.py` and place your script in either the `src/filters/` or `src/readers/` directories with a meaningful name. *Note* that the script will only compile `.py` files that contain either `filter_` or `reader_` in the file name. This is so you can save other `.py` files in those directories without issues.

All of the distributed filters in this repo will appear in the menu category `CSM Geophysics Filters`. As you develop your own, it may be useful to specify your own menu category as outlined in the hints of the ExtraXml in `src/example.py`

## Requesting Features, Reporting Issues, and Contributing
Please feel free to post features you would like to see from this repo in the Issues section as a feature request. If you stumble across any bugs or crashes while using code distributed here, please report it in the Issues section so I can promptly address it.

If you have your own plugins either developed in C++ or as python programmable filters, please share it so this can be a one stop place for geoscience plugins to ParaView!
