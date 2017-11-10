# Installing the Plugins in this Repo

## Detailed Explanation of How to Install

To clone and use the plugins distributed in the repo for ParaView, you'll need [Python 2](https://www.python.org/downloads/) with the SciPy and NumPy modules [installed](https://docs.python.org/2/installing/index.html), and [ParaView](https://www.paraview.org/download/) installed on your computer. Note that this repository will only work with builds of ParaView that have Python. Currently, the VR build of ParaView does not have Python included, and we will describe some workarounds for sending data to the VR version on under the Resources section in the [Docs pages](http://paraviewgeophysics.readthedocs.io/).

### Windows Users:
If you're on Windows, see [this](https://git-for-windows.github.io) for GitHub and [this](https://devtidbits.com/2011/07/01/cygwin-walkthrough-and-beginners-guide-is-it-linux-for-windows-or-a-posix-compatible-alternative-to-powershell/) guide for using the Unix command line on windows.

Download and use [Cygwin](https://devtidbits.com/2011/07/01/cygwin-walkthrough-and-beginners-guide-is-it-linux-for-windows-or-a-posix-compatible-alternative-to-powershell/) for the command line operation of the scripts in this repo. When installing Cygwin, *make sure to install the `bash`, `dos2unix`, `git`, and `python2-setuptools` packages*. Now you can use the Cygwin terminal as the command line just like you are on a Unix based operating system! **Make sure the line endings for all of the shell scripts are LF and not CRLF after cloning.**

Also, be sure to place/install ParaView and this repository to a location that has general read/write privileges for all users such as on your `D:\\` drive. You will encounter all types of issues running the scripts and simply accessing the code via Cygwin if you need admin privileges to access where it is all saved. *Note: the install scripts will need access to the directory where ParaView is installed*


### Before You Do Anything!

You *MUST* add a `PVPATH` variable in your bash profile! This variable will describe the path to ParaView's installation. It is likely different depending on your OS and your version of ParaView. On MacOS, simply just replace `/ParaView-5.4.0.app` with the name of your version of ParaView under `/Applications/`.

Add the `PVPATH` variable to your environment through your `~/.bash_profile` by adding this expression:
```bash
# edit your ~/.bash_profile with vim or some text editor
$ vi ~/.bash_profile

# Be sure to check that this path matches yours... Odds are it's different!
# Path to the ParaView installation:
export PVPATH="/Applications/ParaView-5.4.0.app"
```

Windows users, open Cygwin and edit your `~/.bash_profile` through `vim` to place a `PVPATH` variable in your environment. Be sure to replace the path to ParaView with your path to ParaView (e.g. `/cygdrive/d/ParaView...` to `/cygdrive/d/ParaView-5.4.0...`)

```bash
## Be sure to check that this path matches yours... Odds are it's different!
# Path to the ParaView installation:
export PVPATH="/cygdrive/d/ParaView"
```

Remember to source your edited `~/.bash_profile`:

```bash
# Resource your profile to export the new variable
$ source ~/.bash_profile
```

### Cloning the Repository
Clone the repository from your command line by navigating to the directory you would like to save all of the code from this repo.

**NOTE:** Windows users, you are going to want to clone to a folder/drive that has general read/write privileges such as your `D:\\` drive

From your command line:

```bash
# Clone this repository
$ git clone https://github.com/banesullivan/ParaViewGeophysics

# Go into the repository
$ cd ParaViewGeophysics
```

### Installing the Plugins to ParaView
Now to get started using the plugins and python modules included in this repository, we need to create links between your installation of ParaView and this repository. That's why we need a `PVPATH` variable to be set in your environment (above).

To create these links, run the installation script at the top of the repository called `install.sh`. If errors arise, they will be printed in red. The most common cause of error is having an incorrect `PVPATH` variable.

```bash
# Install our repository to ParaView
$ sh ./install.sh
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

# How to Update After Installation
We have included a script that will update the repository from GitHub and re-install everything. This script is simply executed by:

```bash
$ sh ./updatePVGP.sh
```
