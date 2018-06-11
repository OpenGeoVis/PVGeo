[format1]: https://cals.arizona.edu/PLP/GIS/Case_Study_Af/GeoEAS/fileformat.html
[format2]: http://www.gslib.com/gslib_help/format.html

# GSLIB Table

## About this Reader
The GSLIB file format has headers lines followed by the data as a space delimited ASCI file (this filter is set up to allow you to choose any single character delimiter: default is a space). The first header line contains the title or necessary information and will be printed to the console. This line may have the dimensions for a grid to be made of the data. The second line is the number (n) of columns of data. The next n lines are the variable names for the data in each column. You are allowed up to ten characters for the variable name. The data follow with a space between each field (column). The output of this reader is a vtkTable of the input data. The table will have all the same columns as the input file with the column/data names set to their respective names from the input file.

??? note "The GSLIB File Format"
    Check out [this site][format1] and [this site][format2] for more information on the specifics of the file format. The general format is as follows:

    ```txt
    Header
    numberOfColumns
    Col1_name
    Col2_name
    Col3_name
    dataCol1 dataCol2 dataCol3
    dataCol1 dataCol2 dataCol3
    dataCol1 dataCol2 dataCol3
    dataCol1 dataCol2 dataCol3
    dataCol1 dataCol2 dataCol3
    ...
    ```

    An example file might look something like this:

    ```txt
    Fun data set!
    3
    Variable1
    Variable2
    Variable3
    0.908793985844 -0.141859993339 0.76693302393
    0.909209012985 0.0264630001038 0.935671985149
    0.908389985561 -0.0224980004132 0.885891973972
    0.906355023384 -0.0762720033526 0.83008402586
    0.895779013634 0.0125150000677 0.908294022083
    0.876645028591 -0.0550080016255 0.821636974812
    0.856096029282 0.0719339996576 0.928031027317
    ...
    ```

## Down the Pipeline
- [Table to Uniform Grid](../pvgp-grids/table-to-uniform-grid.md)
- [Reshape Table](../filters-general/reshape-table.md)
- [Table to Points](https://www.paraview.org/Wiki/ParaView/Users_Guide/List_of_filters#Table_To_Points)
- [Table to Structured Grid](https://www.paraview.org/Wiki/ParaView/Users_Guide/List_of_filters#Table_To_Structured_Grid)
- [Normalize Array](../filters-general/normalize-array.md)

-----

## Code Docs

{def:PVGeo.read.gslib}
