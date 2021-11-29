Composite Data Writers
----------------------

.. _Bane Sullivan: http://banesullivan.com
.. _GitLab project snippets: https://gitlab.kitware.com/paraview/paraview/snippets/425

This snippet was written by `Bane Sullivan`_ and was originally posted on
ParaView's `GitLab project snippets`_.

The functionality using decorated ``VTKPythonAlgorithmBase`` classes as ParaView
plugins has a composite support option for the ``smdomain`` input property that is
incredibly simple to use with filter algorithms yet can be tricky to use for
writer algorithms.

.. code-block:: python

    @smproxy.writer(...)
    @smproperty.input(name="TableInput", port_index=0)
    @smdomain.datatype(dataTypes=["vtkTable"], composite_data_supported=True)
    class MyWriter(VTKPythonAlgorithmBase):
           ...


This solution handles altering the given filename to save out each object in
the composite dataset separately by saving each block out in
``perform_write_out``  method that is repeatedly called by ``RequestData``
explicitly.

Note that we must use the ``composite_data_supported=True`` flag for the
``@smproxy.writer(...)`` declaration as well as append allowable input types
within the algorithms ``FillInputPortInformation`` method.

.. code-block:: python

    # This is partially pseudo-code and is implemented in `WriterBase`

    @smproxy.writer(...)
    @smproperty.input(name="Input", port_index=0)
    @smdomain.datatype(dataTypes=["vtkDataSet"], composite_data_supported=True)
    class MyWriter(VTKPythonAlgorithmBase):
           ...

        def FillInputPortInformation(self, port, info):
            """Allows us to save composite datasets as well.
            NOTE: I only care about ``vtkMultiBlockDataSet``s
            """
            info.Set(self.INPUT_REQUIRED_DATA_TYPE(), self.InputType)
            info.Append(self.INPUT_REQUIRED_DATA_TYPE(), 'vtkMultiBlockDataSet')
            return 1

        def perform_write_out(self, inputDataObject, filename):
            """This method must be implemented. This is automatically called by
            ``RequestData`` for single inputs or composite inputs."""
            raise NotImplementedError('perform_write_out must be implemented!')

        def RequestData(self, request, inInfoVec, outInfoVec):
            """Subclasses must implement a ``perform_write_out`` method that takes an
            input data object and a filename. This method will automatically handle
            composite data sets.
            """
            inp = self.GetInputData(inInfoVec, 0, 0)
            # Handle composite datasets.
            # NOTE: This only handles 'vtkMultiBlockDataSet'
            if isinstance(inp, vtk.vtkMultiBlockDataSet):
                num = inp.GetNumberOfBlocks()
                # Create a list of filenames that vary by block index
                self.set_block_filenames(num)
                for i in range(num):
                    data = inp.GetBlock(i)
                    if data.IsTypeOf(self.InputType):
                        self.perform_write_out(data, self.get_block_filename(i))
                    else:
                        print('Invalid input block %d of type(%s)' % (i, type(data)))
            # Handle single input dataset
            else:
                self.perform_write_out(inp, self.get_file_name())
            return 1



Example
+++++++

.. code-block:: python

    import PVGeo
    from PVGeo.base import WriterBase
    # This is module to import. It provides VTKPythonAlgorithmBase, the base class
    # for all python-based vtkAlgorithm subclasses in VTK and decorators used to
    # 'register' the algorithm with ParaView along with information about UI.
    from paraview.util.vtkAlgorithm import *
    from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase

    import vtk
    import numpy as np
    from vtk.numpy_interface import dataset_adapter as dsa

    ###############################################################################
    ## Now lets use ``WriterBase`` to make a writer algorithm that ParaView can use

    class WriteCellCenterData(WriterBase):
        """This writer will save a file of the XYZ points for an input dataset's
        cell centers and its cell data. Use in tandom with ParaView's native CSV
        writer which saves the PointData. This class was originally
        implemented in `PVGeo`_ by `Bane Sullivan`_.

        .. _PVGeo: http://pvgeo.org
        .. _Bane Sullivan: http://banesullivan.com
        """
        def __init__(self):
            WriterBase.__init__(self, inputType='vtkDataSet')
            self.__delimiter = ','


        def PerformWriteOut(self, input_data_object, filename, object_name):
            # Find cell centers
            filt = vtk.vtkCellCenters()
            filt.SetInputDataObject(input_data_object)
            filt.Update()
            centers = dsa.WrapDataObject(filt.GetOutput(0)).Points
            # Get CellData
            wpdi = dsa.WrapDataObject(input_data_object)
            celldata = wpdi.CellData
            keys = celldata.keys()
            # Save out using numpy
            arr = np.zeros((len(centers), 3 + len(keys)))
            arr[:,0:3] = centers
            for i, name in enumerate(keys):
                arr[:,i+3] = celldata[name]
            # Now write out the data
            # Clean data titles to make sure they do not contain the delimiter
            repl = '_' if self.__delimiter != '_' else '-'
            for i, name in enumerate(keys):
                keys[i] = name.replace(self.__delimiter, repl)
            header = ('%s' % self.__delimiter).join(['X', 'Y', 'Z'] + keys)
            np.savetxt(filename, arr,
                       header=header,
                       delimiter=self.__delimiter,
                       fmt=self.get_format(),
                       comments='')
            # Success for pipeline
            return 1

        def set_delimiter(self, deli):
            """The string delimiter to use"""
            if self.__delimiter != deli:
                self.__delimiter = deli
                self.Modified()


    ###############################################################################
    ## Now lets use ``WriterBase`` to make a writer algorithm for image data


    @smproxy.writer(extensions="imgfmt", file_description="Write Custom ImageData", support_reload=False)
    @smproperty.input(name="Input", port_index=0)
    @smdomain.datatype(dataTypes=["vtkImageData"], composite_data_supported=True)
    class WriteCustomImageData(WriterBase):
        """This is an example of how to make your own file writer!

        .. _PVGeo: http://pvgeo.org
        .. _Bane Sullivan: http://banesullivan.com
        """
        def __init__(self):
            WriterBase.__init__(self, inputType='vtkImageData')
            self.__delimiter = ','


        def PerformWriteOut(self, input_data_object, filename, object_name):
            """Perform the file write to the given FileName with the given data
            object. The super class handles all the complicated stuff.
            """
            filename = filename.split('.')
            filename = '.'.join(filename[0:-1]) + '_%s.%s' % (object_name, filename[-1])
            writer = vtk.vtkXMLImageDataWriter()
            writer.SetFileName(filename)
            writer.SetInputDataObject(input_data_object)
            writer.Write()
            # Success for pipeline
            return 1

        @smproperty.stringvector(name="FileName", panel_visibility="never")
        @smdomain.filelist()
        def SetFileName(self, filename):
            """Specify filename for the file to write."""
            WriterBase.SetFileName(self, filename)




    ###############################################################################
    ## Now wrap the cell centers writer for use in ParaView!

    @smproxy.writer(extensions="dat", file_description="Cell Centers and Cell Data", support_reload=False)
    @smproperty.input(name="Input", port_index=0)
    @smdomain.datatype(dataTypes=["vtkDataSet"], composite_data_supported=True)
    class PVWriteCellCenterData(WriteCellCenterData):
        """The ``WriteCellCenterData`` class wrapped for use as a plugin in ParaView.
        Be sure that the ``composite_data_supported`` flag is set to ``True``.
        """
        def __init__(self):
            WriteCellCenterData.__init__(self)


        @smproperty.stringvector(name="FileName", panel_visibility="never")
        @smdomain.filelist()
        def SetFileName(self, filename):
            """Specify filename for the file to write."""
            WriteCellCenterData.SetFileName(self, filename)

        @smproperty.stringvector(name="Format", default_values='%.9e')
        def set_format(self, fmt):
            """Use to set the ASCII format for the writer default is ``'%.9e'``"""
            WriteCellCenterData.set_format(self, fmt)

        @smproperty.stringvector(name="Delimiter", default_values=',')
        def set_delimiter(self, deli):
            """The string delimiter to use"""
            WriteCellCenterData.set_delimiter(self, deli)
