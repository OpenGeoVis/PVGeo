!!! info "Purpose"
    The main advantage of having this reader and using it over the default delimited text reader is that we can specify to use tab (`\t`) delimiters and that we deliver to the users of this repo a delimited text reader that they manipulate to work for their file format needs.

## About this Reader
This reader will take in any delimited text file and make a vtkTable from it. This is not much different than the default .txt or .csv reader in ParaView, however it gives us room to use our own extensions and a little more flexibility in the structure of the files we import.

## Down the Pipeline
- [Table to Uniform Grid](../filt/Table-to-Uniform-Grid.md)
- [Reshape Table](../filt/Reshape-Table.md)
- [Table to Points](https://www.paraview.org/Wiki/ParaView/Users_Guide/List_of_filters#Table_To_Points)
- [Table to Structured Grid](https://www.paraview.org/Wiki/ParaView/Users_Guide/List_of_filters#Table_To_Structured_Grid)
- [Normalize Array](../filt/Normalize-Array.md)

-----

## PVGPpy.read.delimitedText

```py
PVGPpy.read.delimitedText(FileName, deli=' ', useTab=False, hasTits=True, numIgLns=0)
```

### Description
This reader will take in any delimited text file and make a vtkTable from it. This is not much different than the default .txt or .csv reader in ParaView, however it gives us room to use our own extensions and a little more flexibility in the structure of the files we import.


### Parameters

`FileName` : str

- The absolute file name with path to read.

`deli` : str

- The input files delimiter. To use a tab delimiter please set the `useTab`.

`useTab` : boolean

- A boolean that describes whether to use a tab delimiter

`numIgLns` : int

- The integer number of lines to ignore

### Returns
Returns a vtkTable of the input data file.
