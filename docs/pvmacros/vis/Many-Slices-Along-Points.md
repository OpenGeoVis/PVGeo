!!! info "Purpose"
    This macro will use a series of points as a path to cut many slices through a given data set.

!!! note
    You will need the SciPy module in `pvpython` for this macro to work. [See details](../../Getting-Started.md#using-outside-modules).


## Motivation
Sometimes we might have a model, some input data, that we would like to have numerous slices of along a series of points, a path of points per say. These points might represent some travel path through the model where we would like to have a slice of the model at each point so that we can make spacial decisions and share this information of flat documents.

## Goal
Create a macro that uses a series of points to create a path through a dataset that can then be sliced at many points (or customized to select ten or twenty points to slice on). The points will be converted into a sorted polyline using a nearest neighbor approximation so that we can have a coherent travel path through the model. The order in the poly line will be used to determine a normal vector for each slice.

## Example Use

### Set the inputs
This macro takes two data sources, some data containing the points for our travel path and some data that can be sliced. The function calls for the string name of both of those datasets as specified above.

The `pointsNm` variable will be the string name of the data source that has the point data you would like to use. Think of these points as a travel path, as we will perform a nearest neighbor route between all of the points to create a polyline. A scattered point dataset will not work well for the macro as the slices will have seemingly random orientations.

The `dataNm` variable will be the string name of the data source or model of which you desire to have interior slices. It is important that this data source is 'slice-able,' as some data types in VTK may not be sliceable (such as a point set). If errors arise, make sure this data set is slice-able by applying a simple slice filter from the Filters->Common->Slice.


<!-- TODO provide a pointset and a 3D model for an example -->

If you have a series of points and a data set, go ahead and run this macro in the Python Shell (Tools->Python Shell):

```py
import pvmacros as pvm
pvm.vis.manySlicesAlongPoints('Points', 'Data')
```

### Saving
If you desire to save out the slices, you just made with this macro, then set the `exportpath` optional variable when calling the method. Be sure to give that directory a meaningful name and use that directory only for these slices as the slices will be saved out as 'slice0.csv', 'slice1.csv', and so on.


## Batch Processing
<!--- TODO --->
If you want to make tons of slices of a model, the outputs of this macro WILL get messy if used in the ParaView GUI. We recommend using the `pvpython` module on the command line to perform large batch processing like this. More details to come... stay tuned.


--------

## pvmacros.vis.manySlicesAlongPoints

```py
pvmacros.vis.manySlicesAlongPoints(pointsNm, dataNm, numSlices=10, exportpath='', ext='.csv')
```

### Description
This macro takes a series of points and a data source to be sliced. The points are used to construct a path through the data source and a slice is added at intervals of that path along the vector of that path at that point. This constructs `numSlices` slices through the dataset `dataNm`.

### Parameters
`pointsNm` : string

- The string name of the points source to construct the path.

`dataNm` : string

- The string name of the data source to slice.
- Make sure this data source is slice-able.

`numSlices` : int, optional

- The number of slices along the path.

`exportpath` : string, optional

- The absolute file path of where to save each slice

`ext` : string, optional

- The file extension for saving out the slices.
- Default to '.csv'


### Notes
- Make sure the input data source is slice-able.
- The SciPy module is required for this macro.
