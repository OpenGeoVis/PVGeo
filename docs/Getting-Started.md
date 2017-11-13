# A Brief Introduction to ParaView

ParaView is an open-source platform that can visualize 2D, 3D, and 4D (time varying) datasets. ParaView can process multiple very large data sets in parallel then later collect the results to yield a responsive graphics environment with which a user can interact. The better the processor and graphics hardware the machine or machines hosting the software, the faster and better ParaView will run, however it can run quite well on a laptop with a standard graphics card such as a MacBook Pro.

Since ParaView is an open source application, anyone can download the program and its source code for modifications. The easiest way to get started with ParaView is to download the compiled binary installers for your operating system from [here](https://www.paraview.org/download/).

For further help, check out the [documentation](https://www.paraview.org/documentation/) provided by Kitware. In particular, the two worth looking through for a quick tour of ParaView are the 'The ParaView Guide' and 'The ParaView Tutorial.' One is a tutorial of the ParaView software and shows the user how to create sources, apply filters, and more. The other is a guide on how to do scripting, macros, and more intense use of the application.

## Install ParaView
Open the downloaded binary installer and follow the prompts then drag the application into your applications folder.

Tour around software:
Take a look at Section 2.1 of 'The ParaView Tutorial' for details of the application’s GUI environment. Chapter 2 of the tutorial as a whole does an excellent job touring the software and its workflow for those unfamiliar with the software and its general capabilities.

## Notes
* Enable Auto Apply in the preferences for interactive slicers and so you don't always have to click apply. (*Note:* sometimes you may want this off when working with large datasets)
* One convenient feature is to save the state of the ParaView environment. This saves all the options you selected on all the filters you applied to visualize some data. Select File->Save State… (*Note:* this saves the absolute path of the files loaded into ParaView, so be sure to select 'Search for Files Under Directory...' when opening these state files)


----------


# Install ParaViewGeophysics

To clone and use the plugins distributed in the repo for ParaView, you'll need [Python 2](https://www.python.org/downloads/) with the SciPy and NumPy modules [installed](https://docs.python.org/2/installing/index.html), and [ParaView](https://www.paraview.org/download/) installed on your computer. Note that this repository will only work with builds of ParaView that have Python. Currently, the VR build of ParaView does not have Python included, and we will describe some workarounds for sending data to the VR version on under the Resources section in the [Docs pages](http://paraviewgeophysics.readthedocs.io/).

## Windows Users
If you're on Windows, see [this](https://git-for-windows.github.io) for GitHub and [this](https://devtidbits.com/2011/07/01/cygwin-walkthrough-and-beginners-guide-is-it-linux-for-windows-or-a-posix-compatible-alternative-to-powershell/) guide for using the Unix command line on windows.

Download and use [Cygwin](https://devtidbits.com/2011/07/01/cygwin-walkthrough-and-beginners-guide-is-it-linux-for-windows-or-a-posix-compatible-alternative-to-powershell/) for the command line operation of the scripts in this repo. When installing Cygwin, *make sure to install the `bash`, `dos2unix`, `git`, and `python2-setuptools` packages*. Now you can use the Cygwin terminal as the command line just like you are on a Unix based operating system! **Make sure the line endings for all of the shell scripts are LF and not CRLF after cloning.**

Also, be sure to place/install ParaView and this repository to a location that has general read/write privileges for all users such as on your `D:\\` drive. You will encounter all types of issues running the scripts and simply accessing the code via Cygwin if you need admin privileges to access where it is all saved. *Note: the install scripts will need access to the directory where ParaView is installed*


## Before You Do Anything!

You *MUST* add a `PVPATH` variable in your bash environment! This variable will describe the path to ParaView's installation. It is likely different depending on your OS and your version of ParaView. On MacOS, simply just replace `/ParaView-5.4.0.app` with the name of your version of ParaView under `/Applications/`.

Add the `PVPATH` variable to your environment through this export expression:
```bash
# Be sure to check that this path matches yours... Odds are it's different!
# Path to the ParaView installation:
export PVPATH="/Applications/ParaView-5.4.0.app"
```

Windows users, open Cygwin and add a `PVPATH` variable in your environment in the same manner. Its a bit trickier for you because we need the path on cygwin's map of your drive. Be sure to replace the path to ParaView with your path to ParaView (e.g. `/cygdrive/d/ParaView...` to `/cygdrive/d/ParaView-5.4.0...`)

```bash
# Be sure to check that this path matches yours... Odds are it's different!
# Make sure there are NO SPACES in your path.
# Path to the ParaView installation:
#- If ParaView were installed at D:\\ParaView-version-something then you export looks like this:
export PVPATH="/cygdrive/d/ParaView-version-something"
```

## Cloning the Repository
Clone the repository from your command line by navigating to the directory you would like to save all of the code from this repo.

**NOTE:** Windows users, you are going to want to clone to a folder/drive that has general read/write privileges such as your `D:\\` drive

From your command line:

```bash
# Clone this repository
$ git clone https://github.com/banesullivan/ParaViewGeophysics

# Go into the repository
$ cd ParaViewGeophysics
```

## Installing to ParaView
Now to get started using the plugins and python modules included in this repository, we need to create links between your installation of ParaView and this repository. That's why we need a `PVPATH` variable to be set in your environment (above).

To create these links, run the installation script at the top of the repository called `installMac.sh` or `installWin.sh` for your operating system. If errors arise, they will be printed in red. The most common cause of error is having an incorrect `PVPATH` variable.

*Note: Windows users, when running the `installWin.sh` script there will be some yellow outputs. Make sure they are just announcing successful links and not errors/permission denied.*

```bash
# Install our repository to ParaView:
#- Note: There are two install scripts. One for Mac/Linux and one for Windows
#- Mac:
$ sh ./installMac.sh
#- Windows via Cygwin:
$ sh ./installWin.sh
```

<!--
ÂIn the `src/` directory, there are four shell scripts. Be careful executing these unless you know what they are doing. No severe damage can be done by running any of these scripts by accident; you might just get weird errors or accidentally uninstall everything.

To simply install the distributed filters from this repo, run the `src/install_plugins.sh` script *but first you MUST add the `PVPLUGINPATH` variable to your environment* (described above)! This script will simply copy over all the XML files from `build/` to the default directory for third-party plugins in ParaView so that they will all load when ParaView launches.

To run these scripts on a Unix like system us the `sh` command: `sh src/install_plugins.sh`

```bash
$ sh src/install_plugins.sh
```

### Building the Plugins
To rebuild the plugins after you made changes or made your own plugins, run the `src/build_plugins.sh` script which will build up the XML Server Manager Configuration filters from the `.py` scripts and install them to ParaView. Only use this script if you are making your own filters or readers (or changing what is delivered in this repo). If you run this script, it will build and install all filters and readers to ParaView. This is not necessary as the repo contains a stable build of all the plugins upon cloning.


```bash
$ sh src/build_plugins.sh
```
-->

## How to Update
We have included a script that will update the repository from GitHub and since the repo is already linked to ParaView, all changes to the repo will be directory reflected in ParaView. This script is simply executed by:

```bash
# Run this to update ParaViewGeophysics in the future:
$ sh ./updatePVGP.sh
```


--------------

# Using Outside Modules
ParaView's Python environment, `pvpython`, can be a bit tricky to start using outside Python modules like SciPy or SimPEG. On Mac OS X, using Python modules installed via pip or anaconda should work simply with an `import ...` statement if you have your Python paths set up well. (Mac users: if you have trouble importing SciPy or other modules used in this repo let me know and I will develop a solution). Windows users on the other hand are going to have quite a bit of trouble as `pvpython` is its own environment nestled in the ParaView application. I have not been able to develop an elegant solution for Windows users to use 3rd party Python libraries other than a simple copy/paste of that module into the ParaView application contents.

*Note: Advanced users, try a symbolic link between ParaView's python library and the libraries you have installed. This is how we are installing our module so that it stays updated.*

## Windows Users
To start using third party libraries, we are going to have copy over static versions of the modules into ParaView's `site-packages` directory. This folder should be under `.../ParaView/bin/site-packages/`. Effectively, we just perform a brute install of that module to `pvpython` on Windows so that when we make `import`s, the modules will be found in the `pvpython` environment.

## Modules Currently Needed for this Repo
These are all of the modules that filters, readers, and macros might use in this repo. We recommend opening the Python Shell from ParaView (Tools->Python Shell) and testing the import of each of these modules. Copy/Paste the modules that failed to import from wherever you have them installed into `.../ParaView/bin/site-packages/`:

- [NumPy](http://www.numpy.org) (you may need update ParaView's version to the latest version for SciPy to be happy)
- [SciPy](https://www.scipy.org/install.html)
- [VTK](https://www.vtk.org/download/)
- [datetime](https://docs.python.org/2/library/datetime.html)
- [struct](https://docs.python.org/2/library/struct.html)
- [csv](https://docs.python.org/2/library/csv.html)

I suspect there is a more elegant solution to setting up the Python environment for `pvpython` on Windows to use modules installed from pip or anaconda, however Windows is not my area of expertise and I have had much trouble attempting to figure this out. I encourage a Windows user of this repository to figure this out so we don't have to make static version of these modules to use in ParaView.

Someone *please* figure this out and post a more robust solution to the [Issues page](https://github.com/banesullivan/ParaViewGeophysics/issues).

--------------

# Documentation
All documentation for the code produced from this project will be included in this website. The documentation will contain an explanation of all of the produced plugins (filters and readers) and macros. Use the Sidebar to explore the documentation content and to find all documentation for readers, filters, macros, and more as you need. There are also details on how to [build your own plugins](./Plugins/Build-Your-Own-Plugins.md), how to [export data scenes](./PVGPpy/export/exportVTKjs.md), and transferring your complex data scenes into [virtual reality](./Virtual-Reality/Entering-Virtual-Reality.md).

The purpose to including all this extra documentation is to provide a convenient location for geoscientists to learn how to tailor ParaView to their needs because data representation and communication are an integral part of success in science. To effectively represent our spatial data is the first step to becoming successful and effective geoscientists. This is the principle behind why we are publishing this documentation along with the code in the repository. Not only do we want to effectively communicate the effort and motivation for this project, but we want to empower others to effectively communicate their scientific endeavors through spatial visualizations.

## Plugin Documentation
There is a page dedicated to every plugin in the respective readers and filters categories. On these pages, you will find implementation details, parameters, code quirks, and general usage information. As the project continues, we will also try to have an example for every reader and filter so that users can really get a feel for what is going on and how they might apply these plugins to address their needs. Since almost all geoscientific data is proprietary, these tutorials will likely come late so that we can find good open data sets and models that users can find outside of this repo for free.

## Macro documentation
<!-- TODO: is this section consistent with PVGPpy? -->
Each macro produced for this repository will have a distinct purpose, be it to export isometric screenshots of any data scene or to batch load / convert specific data sets. The macros will have broad applications and be formatted to work with generally any data scene or data of specific formats so that they can be easily expanded upon to complete specific tasks. For the macros we will try to immediately have sample data and a tutorial upon publishing with documentation of what we are doing and why. The Python scripts themselves will be heavily commented, so that every user can tailor the scripts to their individual needs.

There is also a detailed page on how to easily start making your own macros/scripts. From the people that I have talked to, there tends to be quite a steep learning curve with ParaView scripting, so we want to compile our knowledge into one place for others to gain tips, tricks, and advice to start making their own macros.

Remember, if you have an idea for a macro, plugin, or would like to see how we would address a geoscientific visualization problem with ParaView, please post your thoughts on the [issues page](https://github.com/banesullivan/ParaViewGeophysics/issues).


--------------
