# UBC Tensor Meshes

## About this Reader
UBC Tensor Mesh 2D/3D models are defined using a 2-file format. The "mesh" file describes how the data is discretized. The "model" file lists the physical property values for all cells in a mesh. A model file is meaningless without an associated mesh file. The reader will automatically detect if the mesh is 2D or 3D and read the remainder of the data with that dimensionality assumption. If the mesh file is 2D, then then model file must also be in the 2D format (same for 3D). Full details for the UBC Tensor Mesh formats can be found [**here**](http://giftoolscookbook.readthedocs.io/en/latest/content/fileFormats/format_index.html#meshes)

!!! note "The UBC Tensor Mesh 2D/3D File Format"
    A full explanation of the 2D mesh format can be found [**here**](http://giftoolscookbook.readthedocs.io/en/latest/content/fileFormats/mesh2Dfile.html) and a full explanation of the 2D model format can be found [**here**](http://giftoolscookbook.readthedocs.io/en/latest/content/fileFormats/model2Dfile.html).

    A full explanation of the 3D mesh format can be found [**here**](http://giftoolscookbook.readthedocs.io/en/latest/content/fileFormats/mesh3Dfile.html) and a full explanation of the 3D model format can be found [**here**](http://giftoolscookbook.readthedocs.io/en/latest/content/fileFormats/modelfile.html).


## Down the Pipeline
- [UBC Add Model](../filt/UBC-Add-Model.md)
- [Normalize Array](../filt/Normalize-Array.md)
- [Contour](https://www.paraview.org/Wiki/ParaView/Users_Guide/List_of_filters#Contour)
- [Threshold](https://www.paraview.org/Wiki/ParaView/Users_Guide/List_of_filters#Threshold)
- [Cell Data to Point Data](https://www.paraview.org/ParaView/Doc/Nightly/www/py-doc/paraview.simple.CellDatatoPointData.html)


## Example Use
For example files to use with this reader, download the example from [the GIFtools Cookbook website](http://giftoolscookbook.readthedocs.io/en/latest/content/AtoZ/NS/index.html) and load the 3D mesh model into ParaView by selecting **File->Open...** and choose `TKC_finermesh.msh` as the mesh file to open using the **Read UBC Mesh 2D/3D Two-File Format** reader. Once the reader is on the pipeline, edit the FileName Model Parameter by choosing `CompleteTask/TKCgeologyImage_mod_sus.mod` as the model file. A 3D volume of data should automatically be built and visualized of the model from this example. Go ahead and slice through the model.


## Code Docs

{def:PVGPpy.read.ubcExtent}

{def:PVGPpy.read.ubcTensorMesh}

{def:PVGPpy.read.placeModelOnMesh}

### 3D

{def:PVGPpy.read.ubcMesh3D}

{def:PVGPpy.read.ubcModel3D}

### 2D

{def:PVGPpy.read.ubcMesh2D}

{def:PVGPpy.read.ubcModel2D}
