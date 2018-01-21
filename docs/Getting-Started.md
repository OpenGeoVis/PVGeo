# A Brief Introduction to ParaView

ParaView is an open-source platform that can visualize 2D, 3D, and 4D (time-varying) datasets. ParaView can process multiple very large data sets in parallel then later collect the results to yield a responsive graphics environment with which a user can interact. The better the processor and graphics hardware the machine or machines hosting the software, the faster and better ParaView will run. However, it can run quite well on a laptop with a standard graphics card such as a MacBook Pro.

Since ParaView is an open source application, anyone can download the program and its source code for modifications. The easiest way to get started with ParaView is to download the compiled binary installers for your operating system from [here](https://www.paraview.org/download/).

For further help, check out the [documentation](https://www.paraview.org/documentation/) provided by Kitware. In particular, the two worth looking through for a quick tour of ParaView are the **The ParaView Guide** and **The ParaView Tutorial.** One is a tutorial of the ParaView software and shows the user how to create sources, apply filters, and more. The other is a guide on how to do scripting, macros, and more intense use of the application.

## Install ParaView
Open the downloaded installer and follow the prompts then drag the application into your applications folder.

Tour around software:
Take a look at Section 2.1 of **The ParaView Tutorial** for details of the application’s GUI environment. Chapter 2 of the tutorial as a whole does an excellent job touring the software and its workflow for those unfamiliar with the software and its general capabilities.

## Tips
* Enable Auto Apply in the preferences for interactive slicers and so you don't always have to click apply. (*Note:* sometimes you may want this off when working with large datasets)
* One convenient feature is to save the state of the ParaView environment. This saves all the options you selected for all the filters you applied to visualize some data. Select File->Save State… (*Note:* this saves the absolute path of the files loaded into ParaView, so be sure to select **Search for Files Under Directory...** when opening these state files)


----------


# Install ParaViewGeophysics

To clone and use the plugins distributed in the repo for ParaView, you'll need [Python 2](https://www.python.org/downloads/) with the SciPy and NumPy modules [installed](https://docs.python.org/2/installing/index.html), and [ParaView](https://www.paraview.org/download/) installed on your computer. Note that this repository will only work with builds of ParaView that have Python. Currently, the VR build of ParaView does not have Python included, and we will describe some workarounds for sending data to the VR version on under the Resources section in the [Docs pages](http://paraviewgeophysics.readthedocs.io/).

## Windows Users
If you're on Windows, see [this](https://git-for-windows.github.io) for GitHub and [this](https://devtidbits.com/2011/07/01/cygwin-walkthrough-and-beginners-guide-is-it-linux-for-windows-or-a-posix-compatible-alternative-to-powershell/) guide for using the Unix command line on windows.

Download and use [Cygwin](https://devtidbits.com/2011/07/01/cygwin-walkthrough-and-beginners-guide-is-it-linux-for-windows-or-a-posix-compatible-alternative-to-powershell/) for the command line operation of the scripts in this repo. When installing Cygwin, *make sure to install the `bash`, `dos2unix`, `git`, and `python2-setuptools` packages*. Now you can use the Cygwin terminal as the command line just like you are on a Unix based operating system! **Make sure the line endings for all of the shell scripts are LF and not CRLF after cloning.**

Also, be sure to place/install ParaView and this repository to a location that has general read/write privileges for all users such as on your `D:\\` drive. You will encounter all types of issues running the scripts and simply accessing the code via Cygwin if you need admin privileges to access where it is all saved. *Note: the install scripts will need access to the directory where ParaView is installed*


## Cloning the Repository
Clone the repository from your command line by navigating to the directory you would like to save all of the code from this repo.

**NOTE:** Windows users, you are going to want to clone to a folder/drive that has general read/write privileges such as your `D:\\` drive

From your command line:

```bash
# Clone this repository
$ git clone https://github.com/banesullivan/ParaViewGeophysics

# Go in the cloned repository
$ cd ParaViewGeophysics
```

## Installing the PVGP Repository
Now to get started using the plugins and python modules included in this repository, we need to set up some environmental variables. For Mac users this is a breeze but for windows users this is a bit more involved. Be sure to never move the directory containing ParaViewGeophysics code (if it is not in a convenient location then you must move it before continuing the install).

### MacOS X Paths
If you are on MacOS X, then your life is easy! Simply run the script `installMac.sh`.

```bash
$ sh ./installMac.sh
```

Now test that the install worked by opening ParaView (close it and reopen if needed). Check that the category **CSM Geophysics Filters** is in the **Filters** menu. Then open the **Python Shell** and import the `PVGPpy` module by executing `import PVGPpy`. Errors should not arise but if they do, post to the [issues page](https://github.com/banesullivan/ParaViewGeophysics/issues) and the errors will be *immediately* addressed.

### Windows Paths
Setting up environmental variables is a bit more involved for Windows. First you need to open **Control Center** and search for **Advanced system settings**. Click **Environment variables**. In the section **User variables for Name** add the following variable by clicking **New...**:

- Variable Name: `PV_PLUGIN_PATH` then select **Browse Directory...** and navigate to the directory where you cloned ParaViewGeophysics and select the `plugins` directory.

Now we need to edit the `PYTHONPATH` variable that should already exit in your environment. This can get messy/tricky so please strictly follow these instructions:

1. Copy the value in the `PV_PLUGIN_PATH` variable but **BE SURE NOT TO INCLUDE THE `plugins` DIRECTORY**. So basically this is the entire path leading up to the `plugins` directory.

2. Edit the `PYTHONPATH` variable by selecting it then click **Edit...**.

3. Pay attention to what that path Currently is because we need to reselect it. So if you path is currently `c:\python27\lib\site-packages` then click **Browse Directory...** and reselect that *exact* directory.

4. Append the **Variable value**. At the end of your re-selected path, type a semi-colon `;` and then add the path to the ParaViewGeophysics repository which you copied in the first step by clicking paste. This is critical to be able to import outside Python modules in `pvpython`.

5. Now test that the install worked by opening ParaView (close it and reopen if needed). Check that the category **CSM Geophysics Filters** is in the **Filters** menu. Then open the **Python Shell** and import the `PVGPpy` module by executing `import PVGPpy`. If an error arises please double check your paths.



## How to Update the PVGP Repository
We have included a script that will update the repository from GitHub, and since the repo is already linked to ParaView, all changes to the repo will be directory reflected in ParaView. This script is simply executed by:

```bash
# Run this to update ParaViewGeophysics in the future:
$ sh ./updatePVGP.sh
```

*Note: Windows users, be sure to run this in cygwin or a bash environment of your choice.*


--------------

# Using Outside Modules
ParaView's Python environment, `pvpython`, can be a bit tricky to start using outside Python modules like SciPy or SimPEG. On Mac OS X, using Python modules installed via pip or anaconda should work simply with an `import ...` statement if you have your Python paths set up well. (Mac users: if you have trouble importing SciPy or other modules used in this repo let me know and I will develop a solution). Windows users: this should have been resolved if you followed the install instructions outlined [above](#windows-paths).


## Modules Currently Needed for this Repo
These are all of the modules that filters, readers, and macros might use in this repo. We recommend opening the Python Shell from ParaView (Tools->Python Shell) and testing the import of each of these modules.

- [NumPy](http://www.numpy.org) (you may need to update ParaView's version to the latest version for SciPy to be happy)
- [SciPy](https://www.scipy.org/install.html)
- [VTK](https://www.vtk.org/download/)
- [datetime](https://docs.python.org/2/library/datetime.html)
- [struct](https://docs.python.org/2/library/struct.html)
- [csv](https://docs.python.org/2/library/csv.html)


--------------

# Documentation
All documentation for the code produced from this project will be included on this website. The documentation will contain an explanation of all of the produced plugins (filters and readers) and macros. Use the Sidebar to explore the documentation content and to find all documentation for readers, filters, macros, and more as you need. There are also details on how to [build your own plugins](./Plugins/Build-Your-Own-Plugins.md), how to [export data scenes](./PVGPpy/export/exportVTKjs.md), and transferring your complex data scenes into [virtual reality](./Virtual-Reality/Entering-Virtual-Reality.md).

The purpose of including all this extra documentation is to provide a convenient location for geoscientists to learn how to tailor ParaView to their needs because data representation and communication are an integral part of success in science. To efficiently represent our spatial data is the first step to becoming successful and productive geoscientists. This is the principle behind why we are publishing this documentation along with the code in the repository. Not only do we want to communicate the effort and motivation for this project efficiently, but we want to empower others to communicate their scientific endeavors through spatial visualizations effectively.

## Plugin Documentation
There is a page dedicated to every plugin in the respective readers and filters categories. On these pages, you will find implementation details, parameters, code quirks, and general usage information. As the project continues, we will also try to have an example for every reader and filter so that users can get a feel for what is going on and how they might apply these plugins to address their needs. Since almost all geoscientific data is proprietary, these tutorials will likely come late so that we can find good open data sets and models that users can find outside of this repo for free.

## Macro documentation
<!-- TODO: is this section consistent with PVGPpy? -->
Each macro produced for this repository will have a distinct purpose, be it to export isometric screenshots of any data scene or to batch load / convert specific data sets. The macros will have broad applications and be formatted to work with generally any data scene or data of specific formats so that they can be easily expanded upon to complete specific tasks. For the macros, we will try to immediately have sample data and a tutorial upon publishing with documentation of what we are doing and why. The Python scripts themselves will be heavily commented so that every user can tailor the scripts to their individual needs.

There is also a detailed page on how to easily start making your own macros/scripts. From the people that I have talked to, there tends to be quite a steep learning curve with ParaView scripting, so we want to compile our knowledge into one place for others to gain tips, tricks, and advice to start making their own macros.

Remember, if you have an idea for a macro, plugin, or would like to see how we would address a geoscientific visualization problem with ParaView, please post your thoughts on the [issues page](https://github.com/banesullivan/ParaViewGeophysics/issues).
