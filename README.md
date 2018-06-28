**WARNING: We are completely rebuilding the repository to be encapsulated in a single Python Module called `PVGeo`. This is in accordance with the new Python capabilities of ParaView outlined in [Merge Request !2516](https://gitlab.kitware.com/paraview/paraview/merge_requests/2516/) for ParaView. The current structure of the project with the `src/` directory and XML plugin files in the `plugins/` directory will be deprecated when that merge request is complete. If you would like to help develop please feel free to work off of the `develop` branch but be sure to keep an eye on the active branch `rebuild-pvpy` as this will reflect the future structure of the project. If you develop plugins in the current framework on `develop`, it will be an easy conversion to the new framework on `rebuild-pvpy`.**

**Proceed with caution until next minor release: *0.8.0***


# *PVGeo*

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/46d8b98101d44fb286420e7289611205)](https://app.codacy.com/app/banesullivan/PVGeo?utm_source=github.com&utm_medium=referral&utm_content=OpenGeoVis/PVGeo&utm_campaign=badger) [![Slack Bage](http://slack.pvgeo.org/badge.svg)](http://slack.pvgeo.org)

This repository contains plugins tailored to data visualization in geophysics for the application [ParaView by Kitware](https://www.paraview.org). These plugins are tailored to data visualization in the geosciences with a heavy focus on structured data sets like 2D or 3D time-varing grids.

Check out the [demo page](http://demo.pvgeo.org/) for a synopsis of the project and some visualization examples. Then check out the [Docs pages](http://pvgeo.org/) to explore the motivation for publishing this repo as well as to find all code documentation. This contains documentation for readers, filters, macros, and more as you need. **NOTE: These are currently out of date and will be updated and finished by end of July 2018**

## About the Authors
The *PVGeo* code library is managed by [**Bane Sullivan**](http://banesullivan.com), graduate student in the Hydrological Science and Engineering interdisciplinary program at the Colorado School of Mines under Whitney Trainor-Guitton. If you have questions please inquire with [info@pvgeo.org](mailto:info@pvgeo.org) or join the [***PVGeo* community on Slack**](http://slack.pvgeo.org).

It is important to note the project is open source and that many features in this repository were made possible by contributors volunteering their time. Please take a look at the contributors page to learn more about the developers of *PVGeo*.

### Acknowledgements
It is important to note the project is open source and that many features in this repository were made possible by contributors volunteering their time. Please take a look at the [**Contributors Page**](https://github.com/OpenGeoVis/PVGeo/graphs/contributors) to learn more about the developers of *PVGeo*.


-----
# More to come
Stay tuned; this project is in its early stages of development, so only a handful of the plugins are tested and published here. Also be sure to out the [Docs pages](http://pvgeo.org/) (*currently being developed and proofed*) for detailed documentation on the filters and general use of this repository.

## Requesting Features, Reporting Issues, and Contributing
Please feel free to post features you would like to see from this repo on the [Issues page](https://github.com/OpenGeoVis/PVGeo/issues) as a feature request. If you stumble across any bugs or crashes while using code distributed here, please report it in the Issues section so we can promptly address it.


-------
# How To Use the Plugins in this Repository
Here we will outline everything you need to do in one spot to quickly install these plugins and get working. If you encounter trouble *or you are a windows user, please read through the detailed explanation [here](http://pvgeo.org/overview/getting-started/#install-PVGeo).*

## Cloning the Repository
Clone the repository from your command line by navigating to the directory you would like to save all of the code from this repo.

From your command line:

```bash
# Clone this repository
$ git clone https://github.com/OpenGeoVis/PVGeo

# Go in the cloned repository
$ cd PVGeo
```

### MacOS X Install
If you are on MacOS X, then your life is easy! Simply run the script `installMac.sh`.

```bash
$ sh ./installMac.sh
```

Now test that the install worked by opening ParaView (close it and reopen if needed). Check that the various **PVGeo** categories are in the **Filters** menu. Then open the **Python Shell** and import the `PVGeo` and `pvmacros` modules by executing `import PVGeo` and `import pvmacros`. Errors should not arise but if they do, post to the [issues page](https://github.com/OpenGeoVis/PVGeo/issues) and the errors will be *immediately* addressed.


-----
# Make Your Own Filters and Readers
A detailed explanation can be found in the [Docs](http://pvgeo.org/dev-guide/build-your-own-plugins/).
