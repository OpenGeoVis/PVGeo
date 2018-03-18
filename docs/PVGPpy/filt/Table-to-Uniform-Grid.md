## About this Filter

!!! bug
    This filter has some quirks and we are working to completely overhaul it to have correct SEPlib axial conventions (d1=z, d2=x, d3=y) and to be more robust. This documentation is very deprecated.

This filter takes a vtkTable object with columns that represent data to be translated (reshaped) into a 3D grid (2D also works, just set the third dimensions extent to 1). The grid will be a n1 by n2 by n3 vtkImageData structure and an origin (south-west bottom corner) can be set at any xyz point. Each column of the vtkTable will represent a data attribute of the vtkImageData formed (essentially a uniform mesh). The SEPlib option allows you to unfold data that was packed in the SEPlib format where the most important dimension is z and thus the z data is d1 (d1=z, d2=y, d3=x). When using SEPlib, specify n1 as the number of elements in the Z-direction, n2 as the number of elements in the X-direction, and n3 as the number of elements in the Y-direction (and so on for other parameters).


## Parameters
- Order: The contiguity or indexing of the data array stored in memory. Default is Fortran like.
- Extent: The number of elements in each of the three axial directions (element 0 (n1) corresponds to x, element 1 (n2) corresponds to y, and element 2 (n3) corresponds to z)
- Use SEPlib: a boolean for if you want to use the SEPlib axial conventions that n1 corresponds to z, n2 corresponds to y, and n3 corresponds to x.
- Spacing: the spacing along each axial direction. Usually we specify a consistent spacing across all axial directions, but you can specify to have unique spacings along each axial direction.
- Origin: the d1, d2, and d3 (x,y,z) coordinates for the south-west bottom corner of the data set. This is the corner from which we build the volume out. Note that you can translate this specification using the [Translate Origin of Grid](Translate-Origin-of-Grid.md) filter.

## Down the Pipeline
- [Translate Origin of Grid](Translate-Origin-of-Grid.md)
- [Flip Grid Axii](Flip-Grid-Axii.md)
- [Normalize Array](Normalize-Array.md)
- [Contour](https://www.paraview.org/Wiki/ParaView/Users_Guide/List_of_filters#Contour)
- [Threshold](https://www.paraview.org/Wiki/ParaView/Users_Guide/List_of_filters#Threshold)

## Example Use
Say we have some data in 1D format or a series of 1D data sets, like a vtkTable where we have columns of data which we know can be restructured into a 2D or 3D volume. One great example is the the table made in the example for using the [Read Binary Packed Data](../read/Binary-Packed-Data.md) reader. Follow the instructions to read in that data to a vtkTable. Once you have sample data in a vtkTable, we can apply a the 'Table to Uniform Grid' Filter and specify the shape of our volumetric data (for 2D data like this example, specify n1 and n2 accordingly and leave n3 as 1). The script provided in the example will output the extent, origin, and spacing parameters for you to use (best to copy/paste from that output into the parameter fields). This example will produce the 2D grid depicted on the [Read Binary Packed Data](../read/Binary-Packed-Data.md) page (that image adds the 'Warp by Scalar' filter).

Another example is to use one of the data files from [this website](http://www.trainingimages.org/training-images-library.html) and load it in using the [GSLIB File to Table](../read/GSLIB.md) reader. These files are in the SGeMS file format but can also be read by the GSLIB file reader. Through loading this data into a table and then applying a Table to Uniform Grid Filter, we are effectively mimicking what the [SGeMS Grid](../read/SGeMS-Grid.md) reader is doing behind the scenes. These SGeMS files make great example because they outline how we can transfer any data with any number of data arrays to a uniform grid (each data array in the input table will represent a different attribute of the space made up by the vtkImageData grid). The GSLIB reader will print out the dimensions of the grid to the Output Messages console (to see this, select View->Output Messages). Use those dimensions for the n1, n2, and n3 parameters. Play around with the other parameters to get a feel for how this filter behaves.
