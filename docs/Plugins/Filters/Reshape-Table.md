More to come!

<!--- TODO --->

This filter will take a vtkTable object and reshape it. This filter essentially treats vtkTables as 2D matrices and reshapes them using numpy.reshape in a C contiguous manner. Unfortunately, data fields will be renamed arbitrarily because VTK data arrays require a name.
