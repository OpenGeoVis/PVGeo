# Features on their way:

Here is a list of features that are shortly coming to this repo. This list will be regularly updated

Documentation is soon to come. We want to do it right: with tutorials, examples, and detailed justification for need and use of each reader and filter.


Suggestions? Post on the [Issues page](https://github.com/banesullivan/ParaViewGeophysics/issues) as a feature request.

## General Features:
- [ ] How to send data scenes made using the Readers, Filters, and Macros in this repository over to the Virtual Reality build of ParaView
- [ ] How to build your own plugins using this project's framework and build scripts

## Readers:
- [ ] **UBC Mesh:** both 2D and 3D. Details [here](https://www.eoas.ubc.ca/ubcgif/iag/sftwrdocs/technotes/faq.htm#mesh) and [here](https://gif.eos.ubc.ca/software/utility_programs#3DmodelsMeshes).
- [ ] **ESRI Grid:** Details [here](https://en.wikipedia.org/wiki/Esri_grid) and [here](http://desktop.arcgis.com/en/arcmap/10.3/manage-data/raster-and-images/esri-grid-format.htm)
- [ ] **ESRI shape files:** Details [here](https://www.esri.com/library/whitepapers/pdfs/shapefile.pdf) and [here](https://en.wikipedia.org/wiki/Shapefile)
- [ ] **Well logs:** Readers for common formats and easy ways to project well logs in XYZ space

## Filters:
- [ ] **Extract Array:** This will allow you to extract any array from any data structure as vtkPolyData.
- [ ] **Transpose Grid:** Transpose or swap axii of grid data sets (vtkImageData and vtkRectilinearGrid)
- [ ] **Reshape Table:** Adding ability to reshape using fortran ordering on the currently available filter.
- [ ] **Make Cubes from Point Set:** This will take a point set and generate cube of some specified size at every point

<!---
**Structure Point Set:** This will take scattered point data and create connectivity/structure either in the form of hexahedrons or quads. More info to come.
-->

## Macros:
- [ ] How to start making your own macros (tips, tricks, and general advice)
- [ ] Save screenshots in isometric views, side, top, etc. views
- [ ] Coming to all macros: ability to use a file selection prompt instead of hardcoding file names into the scripts.
- [x] [Many Slices Along Points:](Macros/ours/Many-Slices-Along-Points.md) Export slices of data set along poly line at every point on that line (normal is the vector from that point to the next)

## Examples:
- [ ] Tutorials for each filter / reader will be in their documentation.
- [ ] How to export a scene to a shareable 3D format
- [ ] Importing DEM topography (with/without satellite imagery)
- [ ] Slicing/cropping a data scene through all components/datasets
- [x] [Slice Model Along PolyLine:](Examples/Slice-Model-Along-PolyLine.md) How to export a slice of a data set projected on a vtkPolyLine (capabilities are currently present in ParaView)


# Features eventually coming (long run):
Plan in the works, we will update this list soon. Let us know if you have ideas on the [Issues page](https://github.com/banesullivan/ParaViewGeophysics/issues).
