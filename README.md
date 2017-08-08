# ParaView Geophysics Plugins
This repository contains plugins for the open-source, multi-platform data analysis and visualization application ParaView by Kitware (https://www.paraview.org). These plugins are tailored to data visualization in the geosciences with a heavy focus on structured data sets like 2D or 3D grids.

**More to come!**
Stay tuned, this project is in its early stages of development.


**Before You Do Anything!!**

You *MUST* change the `PVPATH` variable in `plugins/install_plugins.sh` This variable is likely different depending on you OS and your version of ParaView. On MacOS, simply just replace `/ParaView-5.4.0.app/` with the name of your version of ParaView under `/Applications/`.


**To Install XML Filters and to Build XML Filters to ParaView**

In the `plugins/` directory, there are two shell scripts. `build_plugins.sh` will build up the XML Server Manager Configuration filters from the `.py` scripts and install them. Only use this script if you are making your own filters or readers. If you run this script, it will build and install all filters and readers to ParaView.

To simply install the distributed filters from this repo, run the `install_plugins.sh` script *but first you MUST change the `PVPATH` variable* (described above)! This script will simply copy over all the XML files from `plugins/xml_plugins` to the default directory for third paty plugins in ParaView so that they will all load when ParaView launches.


**To Make Your Own Filters and Readers**

To make a custom filter or reader, follow the outline in `plugins/example.py` and place your script in either the `filters_source_code/` or `readers_source_code/` directories with a meaningful name. *Note* that the script will only compile `.py` files that contain either `filter_` or `reader_` in the file name. This is so you can save other `.py` files in those directories without issues.

All of the distributed filters in this repo will appear in the menu category `CSM Geophysics Filters`. As you develop your own, it may be useful to specify your own menu category as outlined in the hints of the ExtraXml in `example.py`
