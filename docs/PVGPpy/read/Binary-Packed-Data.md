# PVGPpy.read.packedBinaries

```py
PVGPpy.read.packedBinaries(FileName, dblVals=False, dataNm='')
```

Description
-----------
This filter reads in float or double data that is packed into a binary file format. It will treat the data as one long array and make a vtkTable with one column of that data. The reader uses big endian and defaults to import as floats. Use the Table to Uniform Grid or the Reshape Table filters to give more meaning to the data. We chose to use a vtkTable object as the output of this reader because it gives us more flexibility in the filters we can apply to this data down the pipeline and keeps thing simple when using filters in this repository.

Parameters
----------
`FileName` : str

- The absolute file name with path to read.

`dblVals` : boolean, optional

- A boolean flag to chose to treat the binary packed data as doubles instead of the default floats.

`dataNm` : str, optional

- A string name to use for the constructed vtkDataArray

Returns
-------
Returns a vtkTable of the input data file with a single column being the data read.
