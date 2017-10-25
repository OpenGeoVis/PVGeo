# How to Use the Outside Modules
ParaView's Python environment, `pvpython`, can be a bit tricky to start using outside Python modules like SciPy or SimPEG. On Mac OS X, using Python modules installed via pip or anaconda should work simply with an `import ...` statement if you have your Python paths set up well. (Mac users: if you have trouble importing SciPy or other modules used in this repo let me know and I will develop a solution). Windows users on the other hand are going to have quite a bit of trouble as `pvpython` is its own environment nestled in the ParaView application. I have not been able to develop an elegant solution for Windows users to use 3rd party Python libraries other than a simple copy/paste of that module into the ParaView application contents.

## Windows Users:
To start using third party libraries, we are going to have copy over static versions of the modules into ParaView's `site-packages` directory. This folder should be under `.../ParaView/bin/site-packages/`. Effectively, we just perform a brute install of that module to `pvpython` on Windows so that when we make `import`s, the modules will be found in the `pvpython` environment.

### Modules Currently Needed for this Repo
These are all of the modules that filters, readers, and macros might use in this repo. We recommend opening the Python Shell from ParaView (Tools->Python Shell) and testing the import of each of these modules. Copy/Paste the modules that failed to import from wherever you have them installed into `.../ParaView/bin/site-packages/`:
- [NumPy](http://www.numpy.org) (you may need update ParaView's version to the latest version for SciPy to be happy)
- [SciPy](https://www.scipy.org/install.html)
- [VTK](https://www.vtk.org/download/)
- [datetime](https://docs.python.org/2/library/datetime.html)
- [struct](https://docs.python.org/2/library/struct.html)
- [csv](https://docs.python.org/2/library/csv.html)

I suspect there is a more elegant solution to setting up the Python environment for `pvpython` on Windows to use modules installed from pip or anaconda, however Windows is not my area of expertise and I have had much trouble attempting to figure this out. I encourage a Windows user of this repository to figure this out so we don't have to make static version of these modules to use in ParaView.

Someone *please* figure this out and post a more robust solution to the [Issues page](https://github.com/banesullivan/ParaViewGeophysics/issues).
