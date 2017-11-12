# PVGPpy.macros.manySlicesAlongPoints

```py
PVGPpy.macros.manySlicesAlongPoints(pointsNm, dataNm, numSlices=10, exportpath='', ext='.csv')
```

## Description
This macro takes a series of points and a data source to be sliced. The points are used to construct a path through the data source and a slice is added at intervals of that path along the vector of that path at that point. This constructs `numSlices` slices through the dataset `dataNm`.

## Parameters
`pointsNm` : string
* The string name of the points source to construct the path.

`dataNm` : string
* The string name of the data source to slice.
* Make sure this data source is slice-able.

`numSlices` : int, optional

- The number of slices along the path.

`exportpath` : string, optional

- The absolute file path of where to save each slice

`ext` : string, optional

- The file extension for saving out the slices.
- Default to '.csv'


## Notes
- Make sure the input data source is slice-able.
- The SciPy module is required for this macro.
