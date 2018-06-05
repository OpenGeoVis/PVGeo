# Madagascar SSRSF

!!! warning
    This file format reader is not fully implemeted but a working quick fix has been published so that Madagascar SSRSF data files can be imported to the ParaView pipeline.

## About this Reader
This reads in float or double data that is packed into a Madagascar Single Stream RSF binary file format with a leader header. The reader ignores all of the ascii header details by searching for the sequence of three special characters: EOL EOL EOT (\014\014\004) and it will treat the following binary packed data as one long array and make a `vtkTable` with one column of that data. The reader defaults to import as floats with native endianness. Use the **Table to Uniform Grid** or the **Reshape Table** filters to give more meaning to the data. We will later implement the ability to create a gridded volume from the header info. We chose to use a vtkTable object as the output of this reader because it gives us more flexibility in the filters we can apply to this data down the pipeline and keeps thing simple when using filters in this repository.

??? note "Madagascar SSRST Format"
    Go [**here**](http://www.ahay.org/wiki/RSF_Comprehensive_Description#Single-stream_RSF) to learn more about the Madagascar Single Stream RSF file format. ASCII header details are followed by data seperated by a sequence of three special characters: EOL EOL EOT (\014\014\004).


## Down the Pipeline
- [Table to Uniform Grid](../pvgp-grids/table-to-uniform-grid.md)
- [Reshape Table](../filters-general/reshape-table.md)
- [Table to Points](https://www.paraview.org/Wiki/ParaView/Users_Guide/List_of_filters#Table_To_Points)
- [Table to Structured Grid](https://www.paraview.org/Wiki/ParaView/Users_Guide/List_of_filters#Table_To_Structured_Grid)
- [Normalize Array](../filters-general/normalize-array.md)


## Code Docs

{def:PVGPpy.read.madagascar}
