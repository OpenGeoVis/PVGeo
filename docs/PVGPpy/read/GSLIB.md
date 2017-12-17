# PVGPpy.read.gslib

```py
PVGPpy.read.gslib(FileName, deli=' ', useTab=False, numIgLns=0)
```

Description
-----------
Reads a GSLIB file format to a vtkTable. The GSLIB file format has headers lines followed by the data as a space delimited ASCI file (this filter is set up to allow you to choose any single character delimiter). The first header line is the title and will be printed to the console. This line may have the dimensions for a grid to be made of the data. The second line is the number (n) of columns of data. The next n lines are the variable names for the data in each column. You are allowed up to ten characters for the variable name. The data follow with a space between each field (column).

Parameters
----------
`FileName` : str

- The absolute file name with path to read.

`deli` : str

- The input files delimiter. To use a tab delimiter please set the `useTab`.

`useTab` : boolean

- A boolean that describes whether to use a tab delimiter

`numIgLns` : int

- The integer number of lines to ignore

Returns
-------
Returns a vtkTable of the input data file.
