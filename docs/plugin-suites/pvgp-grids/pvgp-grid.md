# PVGP Grid

## About this Reader
The PVGP Grid Format is a custom format we have developed to easily save out gridded data to a file format that can fully ready by a plugin in ParaView for immediate viewing. This format consists of meta data describing a regularly sampled grid on which data attributes reside. The metadata is fully encompassed in a `.pvgp` file which is in JSON format with sub libraries containing model data attributes for that grid in an encoded format to save memory. A PVGP grid can have infinitely many data attributes.

We created this format for when we work with 1-3D numpy arrays that describe a regularly sampled model. If we pass that N-dimensional numpy array to the `:::py savePVGPGrid()` method with approppriate meta data, it will store a file that the PVGP format reader in ParaView can immediately read and render for easy/fast viewing.

## Example Use
Use the following script to construct to 3D numpy arrays with the same dimensionality that describe a model region. Pass those numpy arrays to the `:::py savePVGPGrid()` method and it will save a file that can be immediately read into ParaView for rendering.

??? note "Code to create an input file"
    ```py hl_lines="39"
    import py2PVGP
    import numpy as np

    #################
    # GENERATE DATA #
    #---------------#
    # The 3D space we are working with
    step = 5
    x = np.arange(0,95 + step, step)
    y = np.arange(0,55 + step, step)
    z = np.arange(0,25 + step, step)
    X, Y, Z = np.meshgrid(x,y,z, indexing='ij')

    def f1(x,y,z):
        if y == 25: return 1
        if x == 75: return 2
        else: return 0

    def f2(x,y,z):
        if y == 0: return 0
        if x == 0: return 0
        if z == 0: return 0
        return x**2 + y**2 + z**2

    # Compute the values in our space so we can test that this works
    dd1 = np.zeros(np.shape(X), dtype=np.float32)
    dd2 = np.zeros(np.shape(X), dtype=np.float32)
    for i in range(len(x)):
        for j in range(len(y)):
            for k in range(len(z)):
                dd1[i,j,k] = f1(X[i,j,k],Y[i,j,k],Z[i,j,k])
                dd2[i,j,k] = f2(X[i,j,k],Y[i,j,k],Z[i,j,k])

    #############
    # SAVE DATA #
    #-----------#
    path='/Users/bane/Documents/school/GPVR/data-testing/Readers/PVGP/'
    basename = 'test-data'
    py2PVGP.savePVGPGrid([dd1,dd2], path, basename, spacing=(step,step,step))

    ```


-----
## Code Docs

{def:py2PVGP.savePVGPGrid}

{def:PVGPpy.read.readPVGPGrid}
