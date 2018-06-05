Here is a list of features that are shortly coming to this repo.We will try to regularly update this page; for a more update view of our activity, please check out the different projects on the GitHub page [**here**](https://github.com/OpenGeoVis/PVGeophysics/projects).

More documentation is soon to come. We want to do it right: with tutorials, example data, and detailed justification for need and use of each reader, filter, and macro.

!!! info "Suggestions?"
    We need **your** suggestions for what kinds of file format readers to make as well as ideas for filters to meet your data needs. Post on the [Issues page](https://github.com/OpenGeoVis/PVGeophysics/issues) on GitHub as a feature request.

    Don't have a GitHub account but still have ideas or questions? Post a comment at the [bottom of this page](#comments)!

### Readers
- [ ] **Open Mining Format:** All file types and data types found [**here**](https://github.com/GMSGDataExchange/omf)
- [x] [**UBC Tensor Meshes**](plugin-suites/ubc/tensor-grids.md): both 2D and 3D implemented
- [x] [**UBC OcTree Mesh**](plugin-suites/ubc/octree.md): fully implemented but we need test mesh-model file pairs
- [ ] **Well logs:** Readers for common formats (LAS) and easy ways to project well logs in XYZ space. [Details here](http://www.cwls.org/las/)

<!---
- [ ] **ESRI Grid:** Details [**here**](https://en.wikipedia.org/wiki/Esri_grid) and [**here**](http://desktop.arcgis.com/en/arcmap/10.3/manage-data/raster-and-images/esri-grid-format.htm)
- [ ] **ESRI shape files:** Details [**here**](https://www.esri.com/library/whitepapers/pdfs/shapefile.pdf) and [**here**](https://en.wikipedia.org/wiki/Shapefile)
-->

### Filters
- [x] **Append Model to UBC Mesh:** This will load a model file and tag it on to vtkStructuredGrid loaded from a UBC Mesh reader. Think of it as appending models as attributes to the 3D mesh.
- [ ] **Extract Array:** This will allow you to extract any array from any data structure as vtkPolyData.
- [ ] **Transpose Grid:** Transpose or swap axii of grid data sets (vtkImageData and vtkRectilinearGrid)
- [x] **Reshape Table:** Adding ability to reshape using Fortran ordering on the currently available filter.
- [ ] **Make Cubes from Point Set:** This will take a point set and generate cube of some specified size at every point

<!---
**Structure Point Set:** This will take scattered point data and create connectivity/structure either in the form of hexahedrons or quads. More info to come.
-->
### Macros in `pvmacros`
- [x] Save screenshots in isometric views, side, top, etc. in an automated fashion
- [x] [Many Slices Along Points:](pvmacros/vis/many-slices-along-points.md) Export slices of dataset along polyline at every point on that line (normal is the vector from that point to the next)
- [x] [Export a scene](pvmacros/export/exportvtkjs.md) to a shareable 3D format

### Scripts
- [ ] How to start making your own scripts (tips, tricks, and general advice)
- [ ] A few sample scripts to set up tutorial environments.

### Examples and Other Docs
- Tutorials for each filter/reader/macro will be in their respective documentation.
- [ ] How to send data scenes made using the Readers, Filters, and Macros in this repository over to the Virtual Reality build of ParaView
- [ ] How to build your own plugins using this project's framework and build scripts
- [ ] Importing DEM topography (with/without satellite imagery)
- [ ] Slicing/cropping a data scene through all components/datasets (managing links)
- [x] [Slice Model Along PolyLine:](examples/slice-model-along-polyline.md) How to export a slice of a dataset projected on a vtkPolyLine (capabilities are currently present in ParaView)
