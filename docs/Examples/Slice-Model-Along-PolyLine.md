!!! failure "Description to come!"
    There are a lot of pages in the documentation and we are trying to fill all content as soon as possible. Stay tuned for updates to this page


<!--- TODO --->

What if we have a series of points and we desire to create one slice of a data set along the entirety of those points? Then we need to create connectivity between those points and use the native 'Slice Along Poly Line' filter.

First, make a data source that is point data. Maybe you have x,y,z points in a CSV file, read in the file and perform a 'Table to Points' filter. Now add cell connectivity between the points in the form of a poly line by using the 'Add Cell Connectivity to Points' filter delivered in this repository.

Once you have points will poly line connectivity, then apply the 'Slice Along Poly Line' filter that is native to ParaView. Specify the connected points as the polyline source and your data to be sliced as the data input to that filter.
