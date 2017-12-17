# PVGPpy.read.ubcGridData

```py
PVGPpy.read.ubcGridData(FileName_Mesh, FileName_Model, deli=' ', useTab=False, dataNm='')
```

Description
-----------
UBC Mesh 3D models are defined using a 2-file format. The "mesh" file describes how the data is descritized. The "model" file lists the physical property values for all cells in a mesh. A model file is meaningless without an associated mesh file. Default file delimiter is a space character.


Parameters
----------
`FileName_Mesh` : str

- The mesh filename as an absolute path for the input mesh file in UBCMesh Format

`FileName_Model` : str

- The model filename as an absolute path for the input model file in UBCMesh Format.

`deli` : str, optional

- The delimiter field used in the input file. Default is a space character.

`useTab` : boolean, optional

- An optional flag to use a tab delimiter in the input file.

`dataNm` : str, optional

- The name of the model data array once placed on the vtkRectilinearGrid.

Returns
-------
Returns a vtkRectilinearGrid generated from the UBCMesh grid. Mesh is defined by the input mesh file. Cell data is defined by the input model file.


# PVGPpy.read.ubcMeshExtnet

```py
PVGPpy.read.ubcMeshExtnet(FileName_Mesh, deli=' ', useTab=False)
```

Description
-----------
Reads the mesh file for the UBCMesh format to get output extents. Computationally inexpensive method to discover whole output extent.

Parameters
----------
`FileName_Mesh` : str

- The mesh filename as an absolute path for the input mesh file in UBCMesh Format.

`deli` : str, optional

- The delimiter field used in the input file. Default is a space character.

`useTab` : boolean, optional

- An optional flag to use a tab delimiter in the input file.

Returns
-------
This returns a tuple of the whole extent for the rectilinear grid to be made of the input mesh file (0,n1-1, 0,n2-1, 0,n3-1). This output should be directly passed to util.SetOutputWholeExtent() when used in programmable filters or source generation on the pipeline.



# PVGPpy.read.placeModelOnMesh

```py
PVGPpy.read.placeModelOnMesh(mesh, model, dataNm='Data')
```

Description
-----------
Places model data onto a mesh. This is for the UBC Grid data reaers to associate model data with the mesh grid.

Parameters
----------
`mesh` : vtkRectilinearGrid

- The vtkRectilinearGrid that is the mesh to place the model data upon.

`model` : NumPy float array

- A NumPy float array that holds all of the data to place inside of the mesh's cells.

`dataNm` : str, optional

- The name of the model data array once placed on the vtkRectilinearGrid.

Returns
-------
Returns the input vtkRectilinearGrid with model data appended.


# PVGPpy.read.ubcMesh

```py
PVGPpy.read.ubcMesh(FileName_Mesh, deli=' ', useTab=False)
```

Description
-----------
This method reads a UBC Mesh file and builds an empty vrtkRectilinearGrid for data to be inserted into. Default file delimiter is a space character.

Parameters
----------
`FileName_Mesh` : str

- The mesh filename as an absolute path for the input mesh file in UBCMesh Format.

`deli` : str, optional

- The delimiter field used in the input file. Default is a space character.

`useTab` : boolean, optional

- An optional flag to use a tab delimiter in the input file.

Returns
-------
Returns a vtkRectilinearGrid generated from the UBCMesh grid. Mesh is defined by the input mesh file. No data attributes here, simply an empty mesh. Use the placeModelOnMesh() method to associate with model data.



# PVGPpy.read.ubcModel

```py
PVGPpy.read.ubcModel(FileName_Model, deli=' ', useTab=False)
```

Description
-----------
Reads the model file and returns a 1D NumPy float array. Use the placeModelOnMesh() method to associate with a grid.

Parameters
----------
`FileName_Model` : str

- The model filename as an absolute path for the input model file in UBCMesh Format.

`deli` : str, optional

- The delimiter field used in the input file. Default is a space character.

`useTab` : boolean, optional

- An optional flag to use a tab delimiter in the input file.

Returns
-------
Returns a NumPy float array that holds the model data read from the file. Use the placeModelOnMesh() method to associate with a grid.
