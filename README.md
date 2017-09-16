# ParaView Geophysics Plugins
This repository contains plugins for the open-source, multi-platform data analysis, and visualization application [ParaView by Kitware](https://www.paraview.org). These plugins are tailored to data visualization in the geosciences with a heavy focus on structured data sets like 2D or 3D grids.

## *NOTICE:* This repo is under development as the project just started! Consider everything here to be an Alpha (soon to be Beta) release.

## About the Author
Unless otherwise specified at the top of the file, all code and documentation distributed here was produced by [Bane Sullivan](https://github.com/banesullivan/), undergraduate research assistant in the Geophysics Department at the Colorado School of Mines. Feel free to contact for major questions or for custom filters/readers to visualize geoscience data.

## More to come

Stay tuned, this project is in its early stages of development so only a handful of the plugins are tested and published here. Also be sure to check out the [wiki page](https://github.com/banesullivan/ParaViewGeophysics/wiki) (*currently being developed and proofed*) for detailed documentation on the filters and general use of this repository.

## How To Use the Plugins in this Repository

To clone and use the plugins distributed in the repo for ParaView, you'll need [Git](https://git-scm.com), [Python 2](https://www.python.org/downloads/) with the SciPy and NumPy modules [installed](https://docs.python.org/2/installing/index.html), and [ParaView](https://www.paraview.org/download/) installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/banesullivan/ParaViewGeophysics

# Go into the repository
$ cd ParaViewGeophysics

```

Note: If you're on Windows, [see this guide](https://devtidbits.com/2011/07/01/cygwin-walkthrough-and-beginners-guide-is-it-linux-for-windows-or-a-posix-compatible-alternative-to-powershell/)

### Before You Do Anything!

You *MUST* change the `PVPATH` variable in [src/install_plugins.sh](src/install_plugins.sh) This variable is likely different depending on your OS and your version of ParaView. On MacOS, simply just replace `/ParaView-5.4.0.app/` with the name of your version of ParaView under `/Applications/`. To double check the correct path for filter installation, open ParaView and select Tools->Manage Plugins... and copy/paste the path at the top of the window where it says "Local plugins are automatically searched for in ..."

Change this variable in [src/install_plugins.sh](src/install_plugins.sh):
```bash
# NOTE: Change this path if needed:
PVPATH="/Applications/ParaView-5.4.0.app/Contents/MacOS/plugins/"
```


### Building the Plugins

In the `src/` directory, there are two shell scripts. [src/build_plugins.sh](src/build_plugins.sh) will build up the XML Server Manager Configuration filters from the `.py` scripts and install them. Only use this script if you are making your own filters or readers. If you run this script, it will build and install all filters and readers to ParaView.

```bash
$ sh src/build_plugins.sh
```

### Installing the Plugins to ParaView

To simply install the distributed filters from this repo, run the [src/install_plugins.sh](src/install_plugins.sh) script *but first you MUST change the `PVPATH` variable* (described above)! This script will simply copy over all the XML files from `build/` to the default directory for third party plugins in ParaView so that they will all load when ParaView launches.

To run these scripts on a Unix like system us the `sh` command: `sh src/install_plugins.py`

```bash
$ sh src/install_plugins.sh
```


## Make Your Own Filters and Readers

To make a custom filter or reader, follow the outline in [src/example.py](src/example.py) and place your script in either the `src/filters/` or `src/readers/` directories with a meaningful name. *Note* that the script will only compile `.py` files that contain either `filter_` or `reader_` in the file name. This is so you can save other `.py` files in those directories without issues. Then re-run the script  [src/build_plugins.sh](src/build_plugins.sh) to wrap in XML and install to ParaView.

All of the distributed filters in this repo will appear in the menu category `CSM Geophysics Filters`. As you develop your own, it may be useful to specify your own menu category as outlined in the hints of the ExtraXml in [src/example.py](src/example.py)

```python
ExtraXml = '''\
<Hints>
    <ShowInMenu category="Your filter category" />
</Hints>
'''
```

## Requesting Features, Reporting Issues, and Contributing
Please feel free to post features you would like to see from this repo on the [Issues page](https://github.com/banesullivan/ParaViewGeophysics/issues) as a feature request. If you stumble across any bugs or crashes while using code distributed here, please report it in the Issues section so I can promptly address it.

If you have your own plugins either developed in C++ or as python programmable filters, please share it so this can be a one stop place for geoscience plugins to ParaView!
