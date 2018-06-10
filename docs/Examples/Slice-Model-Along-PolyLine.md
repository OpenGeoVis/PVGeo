[filter]: ../plugin-suites/filters-general/add-cell-connectivity-to-points.md
[macro]: ../pvmacros/vis/many-slices-along-points.md
[reader]: ../plugin-suites/gslib/sgems-grid.md
[getstart]: ../overview/getting-started.md#using-outside-modules

!!! info
    This example will demonstrate how to slice a 3D data source along some arbitrary line or sequence of points specified in another data source to have many slices of the 3D data perpendicular to that travel path.

    PVGP features demonstrated:

    - Filter [Add Cell Connectivity to Points][filter]
    - Macro [`manySlicesAlongPoints()`][macro]


Sometimes, we desire to take a path through a model and construct various slices along that path. This example will outline a macro we have developed to take some 3D data set on the pipeline and construct various slices of that model along a path. The slices will be perpendicular to that path at specified intervals. We also play with a filter that comes native in ParaView to slice that entire model along the travel path to have a single warped slice.


First, lets load some data onto the ParaView pipeline. For this example, we want to use a 3D model of rock density in a homogeneous layer of a carbonate reservoir found on [this website](http://www.trainingimages.org/training-images-library.html). You can download the model in the [SGeMS gridded data format][reader] in the link below this paragraph.

{btn:https://dl.dropbox.com/s/87izk92h49jzrli/PVGP-Example.zip?dl=0}

??? example "Data Description"
    Data File 1: 'topexample.sgems'

    - **Original source:** http://www.trainingimages.org/training-images-library.html
    - **Reader to Use:** *SGeMS Grid* from the PVGP repo found [**here**][reader]
    - **Description:** This data file is the 3D model that we will slice through

    Data File 2: 'points.csv'

    - **Reader to Use:** *Delimited Text* reader native to ParaView
    - **Description:** You will perform a *Table to Points* filter on this data source and it holds the points for which we will construct a path to slice the 3D model.

Now that you have the two data files loaded onto the pipeline in ParaView, lets add connectivity to the points so that they form a continuous poly line. To do this, first select the points table on the pipeline that you loaded directly from the data file and apply a **Table to Points** filter on this data source. Select the proper parameters and apply this filter. Now display these points in the render view by clicking the render view then enabling the eyeball icon next to this filter on the pipeline. The points should appear. Now we need to add connectivity to these points such that they form a poly line by applying an [**Add Cell Connectivity to Points**][filter] filter which is in the *PVGP Filters* menu. Make sure the **Poly Line** option is selected for the **Cell Type** parameter and click apply. You can zoom into the line in the render view and see a small line connecting all the points.

??? tip "Filters applied to the points"
    **Table to Points:**

    - Match the columns to the appropriate fields in the parameters.

    **Add Cell Connectivity to Points:**

    - *Cell Type* is *Poly Line*
    - Uncheck *Use nearest nbr*

!!! warning
    The [**Add Cell Connectivity to Points**][filter] filter uses the SciPy python module. You may get an error if you do not have SciPy linked to ParaView Python. To work around this, make sure the **Use nearest nbr** parameter is not checked. Since the points file we give you in this example is in sequential order, this will not matter.  [**See details**][getstart] to learn more about enabling the SciPy module in `pvpython`.


Once you have points will poly line connectivity, then we can use the [`:::py manySlicesAlongPoints()`][macro] macro to complete the task. First, open the Python Shell in ParaView and import the `pvmacros` module and use the macro in the following manner making sure that the data names on the pipeline match what is in the function call.

??? tip "Opening the ParaView Python Shell"
    Open the Python Shell in ParaView from **View->Python Shell** (or **Tools->Python Shell** depending on your ParaView version).

```py
import pvmacros as pvm
pvm.vis.manySlicesAlongPoints('AddCellConnectivityToPoints1', 'topexample.sgems', numSlices=5)

```

Now we can also apply a **Slice Along Poly Line** filter that is native to ParaView to have one warped slice of the model along the poly line we created.  Specify the 'topexample.sgems' source as the **Dataset** input and the connected points 'AddCellConnectivityToPoints1' as the **Poly Line** input to that filter and click apply.

!!! success "Final Data Scene"
    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
            <iframe src="http://gpvis.org/?fileURL=https://dl.dropbox.com/s/c32rkvo05b4a8wl/Slice-Model-Along-PolyLine.vtkjs?dl=0" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>
