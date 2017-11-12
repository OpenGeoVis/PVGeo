# PVGPpy.export.exportVTKjs

```py
PVGPpy.export.exportVTKjs(FileName='', compress=False)
```

Description
-----------
This function will execute a script to export the current scene from your rendering into the VTKjs shareable file format.

Parameters
----------
`FileName` : string, optional

- Use to specify the basename of the output file. Extension will always be '.vtkjs'

`compress` : boolean, optional

- Declares a preference to compress the data arrays.
- Default False

Returns
-------
- No return type, but it will print the path to the saved '.vtkjs' file.

Notes
-----
- To view, open the file in the VTKjs standalone web viewer found here: https://kitware.github.io/vtk-js/examples/StandaloneSceneLoader/StandaloneSceneLoader.html
- Use the get_vtkjs_url.py script in the PVGP repository to get a shareable link for the exported file.
