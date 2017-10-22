# ParaView Geophysics Plugins
This repository contains plugins for the open-source, multi-platform data analysis, and visualization application [ParaView by Kitware](https://www.paraview.org). These plugins are tailored to data visualization in the geosciences with a heavy focus on structured data sets like 2D or 3D grids.

Check out the [Wiki page](https://github.com/banesullivan/ParaViewGeophysics/wiki) to explore the motivation for publishing this repo as well as to find all documentation and some visualization examples. Use the [Wiki Contents](https://github.com/banesullivan/ParaViewGeophysics/wiki/Wiki-Contents) to navigate the Wiki and to see all documentation for readers, filters, macros, and more as you need.

Also checkout [this PDF](https://drive.google.com/file/d/0B6v2US3m042-dzBSR1laSXdiYlU/view?usp=sharing) standalone presentation about the project.

##### *NOTICE:* This repo is under development as the project just started! Consider everything here to be an Alpha (soon to be Beta) release.

## About the Author
Unless otherwise specified at the top of the file, all code and documentation distributed here were produced by [Bane Sullivan](https://github.com/banesullivan/), undergraduate research assistant in the Geophysics Department at the Colorado School of Mines under Dr. Whitney J. Trainor-Guitton. Feel free to contact Bane for questions or for custom filters/readers to visualize geoscience data through the [Issues page](https://github.com/banesullivan/ParaViewGeophysics/issues)

## More to come

Stay tuned; this project is in its early stages of development, so only a handful of the plugins are tested and published here. Also be sure to check out the [Wiki page](https://github.com/banesullivan/ParaViewGeophysics/wiki) (*currently being developed and proofed*) for detailed documentation on the filters and general use of this repository.

## How To Use the Plugins in this Repository

To clone and use the plugins distributed in the repo for ParaView, you'll need [Python 2](https://www.python.org/downloads/) with the SciPy and NumPy modules [installed](https://docs.python.org/2/installing/index.html), and [ParaView](https://www.paraview.org/download/) installed on your computer. Note that this repository will only work with builds of ParaView that have Python. Currently, the VR build of ParaView does not have Python included, and we will describe some workarounds for sending data to the VR version on [these wiki pages](https://github.com/banesullivan/ParaViewGeophysics/wiki/Wiki-Contents#virtual-reality).

From your command line:

```bash
# Clone this repository
$ git clone https://github.com/banesullivan/ParaViewGeophysics

# Go into the repository
$ cd ParaViewGeophysics

```

### Windows Users:
If you're on Windows, see [this](https://git-for-windows.github.io) for GitHub and [this](https://devtidbits.com/2011/07/01/cygwin-walkthrough-and-beginners-guide-is-it-linux-for-windows-or-a-posix-compatible-alternative-to-powershell/) guide for using the Unix command line on windows.

Download and use [Cygwin](https://devtidbits.com/2011/07/01/cygwin-walkthrough-and-beginners-guide-is-it-linux-for-windows-or-a-posix-compatible-alternative-to-powershell/) for the command line operation of the scripts in this repo. When installing Cygwin, *make sure to install the `bash`, `dos2unix`, `git`, and `python2-setuptools` packages*. Now you can use the Cygwin terminal as the command line just like you are on a Unix based operating system! **Make sure the line endings for all of the shell scripts are LF and not CRLF after cloning.**

Also, be sure to place/install ParaView and this repository to a location that has general read/write privileges for all users such as on your `D:\\` drive. You will encounter all types of issues running the scripts and simply accessing the code via Cygwin if you need admin privileges to access where it is all saved. *Note: the install scripts will need access to the directory where ParaView is installed*

### Before You Do Anything!

You *MUST* add a `PVPLUGINPATH` variable in your bash profile! This variable will describe the plugin path within ParaView's application content. It is likely different depending on your OS and your version of ParaView. On MacOS, simply just replace `/ParaView-5.4.0.app/` with the name of your version of ParaView under `/Applications/`. To double check the correct path for filter installation, open ParaView and select Tools->Manage Plugins... and copy/paste the path at the top of the window where it says "Local plugins are automatically searched for in ..."

Add the `PVPLUGINPATH` variable to your environment through your `~/.bash_profile` by executing:
```bash
# ParaViewPlugins on Unix:
# Be sure to check that this path matches yours... Odds are it's different!
$ echo "\n# Path for ParaView Plugins for the ParaViewGeophysics Repo: \nexport PVPLUGINPATH=\"/Applications/ParaView-5.4.0.app/Contents/MacOS/plugins/\"" >> ~/.bash_profile
```

Windows users, open Cygwin and edit your `~/.bash_profile` by executing this command to place a `PVPLUGINPATH` variable in your environment. Be sure to replace the path to ParaView with your path to ParaView (e.g. `/cygdrive/d/ParaView/...` to `/cygdrive/d/ParaView-5.4.0/...`)

```bash
# ParaViewPlugins on Windows via Cygwin
# Be sure to check that this path matches yours... Odds are it's different!
$ echo "\n# Path for ParaView Plugins for the ParaViewGeophysics Repo: \nexport PVPLUGINPATH=\"/cygdrive/d/ParaView/bin/plugins/\"" >> ~/.bash_profile
```

### Installing the Plugins to ParaView
In the `src/` directory, there are four shell scripts. Be careful executing these unless you know what they are doing. No severe damage can be done by running any of these scripts by accident; you might just get weird errors or accidentally uninstall everything.

To simply install the distributed filters from this repo, run the [src/install_plugins.sh](src/install_plugins.sh) script *but first you MUST add the `PVPLUGINPATH` variable to your environment* (described above)! This script will simply copy over all the XML files from `build/` to the default directory for third-party plugins in ParaView so that they will all load when ParaView launches.

To run these scripts on a Unix like system us the `sh` command: `sh src/install_plugins.sh`

```bash
$ sh src/install_plugins.sh
```

### Building the Plugins
To rebuild the plugins after you made changes or made your own plugins, run the [src/build_plugins.sh](src/build_plugins.sh) script which will build up the XML Server Manager Configuration filters from the `.py` scripts and install them to ParaView. Only use this script if you are making your own filters or readers (or changing what is delivered in this repo). If you run this script, it will build and install all filters and readers to ParaView. This is not necessary as the repo contains a stable build of all the plugins upon cloning.

```bash
$ sh src/build_plugins.sh
```

## Make Your Own Filters and Readers

To make a custom filter or reader, follow the outline in [src/example.py](src/example.py) and place your script in either the `src/filters/` or `src/readers/` directories with a meaningful name. *Note* that the script will only compile `.py` files that contain either `filter_` or `reader_` in the file name. This is so you can save other `.py` files in those directories without issues. Then re-run the script  [src/build_plugins.sh](src/build_plugins.sh) to wrap in XML and install to ParaView.

All of the distributed filters in this repo will appear in the menu category `CSM Geophysics Filters`. As you develop your own, it may be useful to specify your own menu category as the variable `FilterCategory` in your python file as shown in [src/example.py](src/example.py).

```py
FilterCategory = 'CSM Geophysics Filters'
```

## Requesting Features, Reporting Issues, and Contributing
Please feel free to post features you would like to see from this repo on the [Issues page](https://github.com/banesullivan/ParaViewGeophysics/issues) as a feature request. If you stumble across any bugs or crashes while using code distributed here, please report it in the Issues section so I can promptly address it.

If you have your own plugins either developed in C++ or as python programmable filters for which you would like a nice GUI, please share it so this can be a one-stop place for geoscience plugins to ParaView!
