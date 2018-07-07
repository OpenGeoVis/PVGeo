[reader]: ../gslib/sgems-grid.md
[getstart]: ../../overview/getting-started.md#using-outside-modules

!!! info
    This example will demonstrate how to slice a 3D data source along some arbitrary line or sequence of points specified in another data source to have many slices of the 3D data perpendicular to that travel path.

!!! warning
    The **Many Slices Along Points** filter uses the SciPy python package. You may get an error if you do not have SciPy linked to ParaView Python. To work around this, make sure the **Use nearest nbr** parameter is not checked. Since the points file we give you in this example is in sequential order, this will not matter.  [**See details**][getstart] to learn more about enabling the SciPy package in `pvpython`.

## Overview
Sometimes, we desire to take a path through a model and construct various slices along that path. This example will outline a filter we have developed to take some 3D data set on the pipeline and construct various slices of that model along an input path. The slices will be perpendicular to that path at specified intervals. In this example, we also demonstrate a filter that comes native in ParaView to slice that entire model along the travel path to have a single warped slice.

## Load the Data
First, lets load some data onto the ParaView pipeline. For this example, we want to use a 3D model of rock density in a homogeneous layer of a carbonate reservoir found on [this website](http://www.trainingimages.org/training-images-library.html). You can download the model in the [SGeMS gridded data format][reader] in the link below this paragraph.

{btn:https://dl.dropbox.com/s/87izk92h49jzrli/PVGP-Example.zip?dl=0}

??? example "Data Description"
    Data File 1: 'topexample.sgems'

    - **Original source:** http://www.trainingimages.org/training-images-library.html
    - **Reader to Use:** *SGeMS Grid* from the PVGeo repo found [**here**][reader]
    - **Description:** This data file is the 3D model that we will slice through

    Data File 2: 'points.csv'

    - **Reader to Use:** *Delimited Text* reader native to ParaView
    - **Description:** You will perform a *Table to Points* filter on this data source and it holds the points for which we will construct a path to slice the 3D model.

## Prepare the Data
Now that you have the two data files loaded onto the pipeline in ParaView. First, select the points table on the pipeline that you loaded directly from the data file and apply a **Table to Points** filter on this data source. Select the proper parameters and apply this filter. Now display these points in the render view by clicking the render view then enabling the eyeball icon next to this filter on the pipeline. The points should appear inside of the data volume from the 'topexample.sgems' source.

??? tip "Filters applied to the points"
    **Table to Points:**

    - Match the columns to the appropriate fields in the parameters.

## Apply the Filter
Now we can use the **Many Slices Along Points** filter by clicking on one of the data objects on the pipeline and selecting **Many Slices Along Points** from the *Filters -> PVGeo: General Filters -> Many Slices Along Points*. A dialog should appear prompting you to select the two inputs for the filter: specify the 'topexample.sgems' source as the **Dataset** input and the points 'TableToPoints1' as the **Points** input to that filter and click apply. That's it! The filter should be applied and you can fine tune the number of slices using the slider bar next to the *Number of Slices* property on the filter properties panel.

### Going a Step Further
We can also apply a **Slice Along Poly Line** filter that is native to ParaView to have one warped slice of the model along the poly line we created.  Specify the 'topexample.sgems' source as the **Dataset** input and the points 'TableToPoints1' as the **Poly Line** input to that filter and click apply.


## Result

!!! success "Final Data Scene"
    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
            <iframe src="http://viewer.pvgeo.org/?fileURL=https://dl.dropbox.com/s/c32rkvo05b4a8wl/Slice-Model-Along-PolyLine.vtkjs?dl=0" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
    </div>




--------

## Code Docs

{class:PVGeo.filters_general.ManySlicesAlongPoints}
