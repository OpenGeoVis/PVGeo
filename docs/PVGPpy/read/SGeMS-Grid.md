# PVGPpy.read.sgemsGrid

```py
PVGPpy.read.sgemsGrid(FileName, deli=' ', useTab=False)
```

Description
-----------
Generates vtkImageData from the uniform grid defined in the inout file in the SGeMS grid format. This format is simply the GSLIB format where the header line defines the dimensions of the uniform grid.

Parameters
----------
`FileName` : str

- The file name / absolute path for the input file in SGeMS grid format.

`deli` : str, optional

- The input files delimiter. To use a tab delimiter please set the `useTab`.

`useTab` : boolean, optional

- A boolean that describes whether to use a tab delimiter.

Returns
-------
Returns vtkImageData


# PVGPpy.read.sgemsExtent

```py
PVGPpy.read.sgemsExtent(FileName, deli=' ', useTab=False)
```

Description
-----------
Reads the input file for the SGeMS format to get output extents. Computationally inexpensive method to discover whole output extent.

Parameters
----------
`FileName` : str

- The file name / absolute path for the input file in SGeMS grid format.

`deli` : str, optional

- The input files delimiter. To use a tab delimiter please set the `useTab`.

`useTab` : boolean, optional

- A boolean that describes whether to use a tab delimiter.

Returns
-------
This returns a tuple of the whole extent for the uniform grid to be made of the input file (0,n1-1, 0,n2-1, 0,n3-1). This output should be directly passed to util.SetOutputWholeExtent() when used in programmable filters or source generation on the pipeline.
