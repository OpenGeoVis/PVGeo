# ParaViewGeophysics
This repository contains plugins tailored to data visualization in geophysics for the application [ParaView by Kitware](https://www.paraview.org). These plugins are tailored to data visualization in the geosciences with a heavy focus on structured data sets like 2D or 3D time-varing grids.

Check out the [demo page](http://demo.pvgp.io/) for a synopsis of the project and some visualization examples. Then check out the [Docs pages](http://pvgp.io/) to explore the motivation for publishing this repo as well as to find all code documentation. This contains documentation for readers, filters, macros, and more as you need. **NOTE: These are currently out of date and will be updated and finished by May 2018**

## About the Author
Unless otherwise specified, all code and documentation distributed here were produced by [Bane Sullivan](http://banesullivan.com), undergraduate research assistant in the Geophysics Department at the Colorado School of Mines under Dr. Whitney J. Trainor-Guitton. Feel free to contact Bane for questions or for custom filters/readers to visualize geoscience data through the [Issues page](https://github.com/banesullivan/ParaViewGeophysics/issues)

### Acknowledgements
Thank you to [Gudni Karl Rosenkjaer](https://github.com/grosenkj) for implementing the UBC OcTree file format reader.

Thank you to [Daan van Vugt](https://github.com/Exteris) for helping me implement the ability to read file series and for developing a robust framework for making file readers found [here](https://github.com/Exteris/paraview-python-file-reader).

Thank you to Pat Marion for building the foundation of the Pyhton Programmable Filter/Reader generation script! See details on [this blog post](https://blog.kitware.com/easy-customization-of-the-paraview-python-programmable-filter-property-panel/).


-----
# More to come
Stay tuned; this project is in its early stages of development, so only a handful of the plugins are tested and published here. Also be sure to out the [Docs pages](http://pvgp.io/) (*currently being developed and proofed*) for detailed documentation on the filters and general use of this repository.

## Requesting Features, Reporting Issues, and Contributing
Please feel free to post features you would like to see from this repo on the [Issues page](https://github.com/banesullivan/ParaViewGeophysics/issues) as a feature request. If you stumble across any bugs or crashes while using code distributed here, please report it in the Issues section so we can promptly address it.

If you have your own plugins either developed in C++ or as python programmable filters for which you would like a nice GUI, please share it so this can be a one-stop place for geoscience plugins to ParaView!


-------
# How To Use the Plugins in this Repository
Here we will outline everything you need to do in one spot to quickly install these plugins and get working. If you encounter trouble *or you are a windows user, please read through the detailed explanation [here](http://pvgp.io/Getting-Started/#install-paraviewgeophysics).*

## Cloning the Repository
Clone the repository from your command line by navigating to the directory you would like to save all of the code from this repo.

From your command line:

```bash
# Clone this repository
$ git clone https://github.com/banesullivan/ParaViewGeophysics

# Go in the cloned repository
$ cd ParaViewGeophysics
```

### MacOS X Install
If you are on MacOS X, then your life is easy! Simply run the script `installMac.sh`.

```bash
$ sh ./installMac.sh
```

Now test that the install worked by opening ParaView (close it and reopen if needed). Check that the category **PVGP Filters** is in the **Filters** menu. Then open the **Python Shell** and import the `PVGPpy` and `pvmacros` modules by executing `import PVGPpy` and `import pvmacros`. Errors should not arise but if they do, post to the [issues page](https://github.com/banesullivan/ParaViewGeophysics/issues) and the errors will be *immediately* addressed.


-----
# Make Your Own Filters and Readers
A detailed explanation can be found in the [Docs](http://pvgp.io/PVGPpy/Build-Your-Own-Plugins/) but here is a quick run through:

To make a custom filter or reader, follow the outline in [src/example_filter.py](src/example_filter.py) or [src/example_reader.py](src/example_reader.py)and place your script in either the `src/filters/` or `src/readers/` directories with a meaningful name. *Note* that the script will only compile `.py` files that contain either `filter_` or `reader_` in the file name. This is so you can save other `.py` files in those directories without issues. Then re-run the script  [src/build_plugins.sh](src/build_plugins.sh) to wrap in XML and install to ParaView.

All of the distributed filters in this repo will appear in the menu category `PVGP Filters`. As you develop your own, it may be useful to specify your own menu category as the variable `FilterCategory` in your python file as shown in [src/example_filter.py](src/example_filter.py).

```py
FilterCategory = 'PVGP Filters'
```
