# UBC OcTree Mesh

## About this Reader
!!! failure "More to come!"
    There are a lot of pages in the documentation and we are trying to fill all content as soon as possible. Stay tuned for updates to this page

<!--- TODO --->

We tested this model using the OcTree mesh found in [**this example**](http://giftoolscookbook.readthedocs.io/en/latest/content/AtoZ/DCIP/index.html) on the [**GIFtoolsCookbook website**](http://giftoolscookbook.readthedocs.io/en/latest/index.html):

- Mesh file: `CompleteTask/octree_mesh.txt`
- Model file: `CompleteTask/active_cells_topo.txt`

To use the plugin:

- Make sure to clone/update the *PVGeophysics* repo and [**install if you haven't already**](../../overview/getting-started.md)
- Select **File->Open...** in ParaView
- Choose the mesh file for your OcTree (we have enabled extensions: `.mesh` `.msh` `.dat` `.txt`)
- Select the **PVGP: UBC OcTree Mesh File Format** reader when prompted.
- *Optional:* Click the **...** button next to the **FileName Model** parameter field. You can select as many model files as you desire (each will be appended as separate attributes).
- Click **Apply** and wait... the load for larger OcTrees takes about 30 seconds.

!!! success "[Example Visualization](http://gpvis.org/?fileURL=https://dl.dropbox.com/s/qybpnsn11lghnq9/OcTree.vtkjs?dl=0)"
    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
            <iframe src="http://gpvis.org/?fileURL=https://dl.dropbox.com/s/qybpnsn11lghnq9/OcTree.vtkjs?dl=0" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>



## Code Docs

{def:PVGeo.ubc.ubcOcTree}
{def:PVGeo.ubc.ubcOcTreeMesh}
{def:PVGeo.ubc.placeModelOnOcTreeMesh}
{def:PVGeo.ubc.ubcExtent}
