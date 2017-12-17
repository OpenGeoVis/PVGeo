# PVGPpy.read.delimitedText

```py
PVGPpy.read.delimitedText(FileName, deli=' ', useTab=False, hasTits=True, numIgLns=0)
```

Description
-----------
This reader will take in any delimited text file and make a vtkTable from it. This is not much different than the default .txt or .csv reader in ParaView, however it gives us room to use our own extensions and a little more flexibility in the structure of the files we import.


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
