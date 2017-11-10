*DEPRECATED. We will update soon*

# Slicing Data Along a Series of Points
Sometimes we might have a model, some input data, that we would like to have numerous slices of along a series of points, a path of points per say. These points might represent some travel path through the model where we would like to have a slice of the model at each point so that we can make spacial decisions and share this information of flat documents.

## Goal:
Create a customizable macro that uses a series of points to create a path through a dataset that can then be sliced at every point (or customized to every ten points per say). The points will be converted into a sorted polyline using a nearest neighbor approximation so that we can have a coherent travel path through the model. The order in the poly line will be used to determine a normal vector for each slice.

# How to Use this Macro
*Note: You will need the SciPy module in `pvpython` for this macro to work. [See details](../../Getting-Started/Using-Outside-Python-Modules.md).*

Take a look at the macro `norm_slices_along_points.py` under the `macros/` directory in the repository. This macro takes two data sources, some data containing the points for our travel path and some data that can be sliced.

## Set the inputs
Change the variable names in the script for the `line` and `data` input sources to set the points to use for our travel path and the data/model to be sliced respectively.

Change the input source for the point data by replacing `'TableToPoints2'` with the name of the source on the pipeline that contains your point information:
```py
# Specify Points for the Line Source:
line = servermanager.Fetch(FindSource('TableToPoints2'))
```

Change the input source for the data to be slice by changing the name `'Delaunay3D1'` to the name of the source that you desire to be sliced. If errors arise, make sure this data set is slice-able by applying a simple slice filter from the Filters->Common->Slice.
```py
# Specify data set to be sliced
data = FindSource('Delaunay3D1')
```

You should be good to go to use the macro at this point! Go ahead and run the macro by opening the Python Shell from Tools->Python Shell then click Run Script and open this script form the repository.

## Saving Out the Slices
If you desire to save out the slices, you just made with this macro, then set the output path at the top of the file and play around with this part of the code around line 50. Give the files meaningful names like the example in the macro (we name the file based on an attribute of the point where the slice was taken from the line source). Simply uncomment the last line there -> `#SaveData(filename, proxy=slc)` and maybe change the extension from `.csv` to whatever format you desire.

Change the output path for where to save the slices:
```py
# Where to save data. Absolute path:
path = '/Users/bane/school/GPVR/closed_data/jacob/slices/'
```

Give the slices meaningful names and uncomment the line to save out the data:
```py
    # save out slice with good metadata: TODO: change name
    # This will use a value from the point data to add to the name
    num = wpdi.PointData['Advance LL (S-558)'][ptsi[i]]
    filename = path + 'Slice_Advance' + str(num) + '.csv'
    print(filename)
    #SaveData(filename, proxy=slc)
```

## Notes:
<!--- TODO --->
If you want to make tons of slices of a model, the outputs of this macro WILL get messy if used in the ParaView GUI. I recommend using the `pvpython` module on the command line to perform large batch processing like this. More details to come... stay tuned.
