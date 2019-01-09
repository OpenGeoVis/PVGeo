"""This file can be loaded as a plugin for ParaView >= 5.6

Author: Bane Sullivan <banesulli@gmail.com>
"""

# This is module to import. It provides VTKPythonAlgorithmBase, the base class
# for all python-based vtkAlgorithm subclasses in VTK and decorators used to
# 'register' the algorithm with ParaView along with information about UI.
from paraview.util.vtkAlgorithm import *
from vtk.util.vtkAlgorithm import VTKPythonAlgorithmBase

import vtk
import numpy as np
from vtk.numpy_interface import dataset_adapter as dsa

class WriterBase(VTKPythonAlgorithmBase):
    """This is a writer base class to add convienace methods to the
    ``VTKPythonAlgorithmBase`` for writer algorithms and was originally
    implemented in `PVGeo`_ by `Bane Sullivan`_.

    .. _PVGeo: http://pvgeo.org
    .. _Bane Sullivan: http://banesullivan.com

    For more information on what functionality is available, check out the VTK
    Docs for the `vtkAlgorithm`_ and then check out the following blog posts:

    * `vtkPythonAlgorithm is great`_
    * A VTK pipeline primer `(part 1)`_, `(part 2)`_, and `(part 3)`_
    * `ParaView Python Docs`_

    .. _vtkAlgorithm: https://www.vtk.org/doc/nightly/html/classvtkAlgorithm.html
    .. _vtkPythonAlgorithm is great: https://blog.kitware.com/vtkpythonalgorithm-is-great/
    .. _(part 1): https://blog.kitware.com/a-vtk-pipeline-primer-part-1/
    .. _(part 2): https://blog.kitware.com/a-vtk-pipeline-primer-part-2/
    .. _(part 3): https://blog.kitware.com/a-vtk-pipeline-primer-part-3/
    .. _ParaView Python Docs: https://www.paraview.org/ParaView/Doc/Nightly/www/py-doc/paraview.util.vtkAlgorithm.html
    """
    def __init__(self, nInputPorts=1, inputType='vtkPolyData', **kwargs):
        VTKPythonAlgorithmBase.__init__(self, nInputPorts=nInputPorts,
                                              inputType=inputType,
                                              nOutputPorts=0)
        self.__filename = kwargs.get('filename', None)
        self.__fmt = '%.9e'
        # For composite datasets: not always used
        self.__blockfilenames = None
        self.__composite = False


    def FillInputPortInformation(self, port, info):
        """Allows us to save composite datasets as well.
        NOTE: I only care about ``vtkMultiBlockDataSet``s but you could hack
        this method and ``RequestData`` to handle ``vtkMultiBlockDataSet``s for
        a general use case.
        """
        info.Set(self.INPUT_REQUIRED_DATA_TYPE(), self.InputType)
        info.Append(self.INPUT_REQUIRED_DATA_TYPE(), 'vtkMultiBlockDataSet') # 'vtkCompositeDataSet'
        return 1


    def SetFileName(self, fname):
        """Specify the filename for the output.
        This will be appended if saving composite datasets.
        """
        if not isinstance(fname, str):
            raise RuntimeError('File name must be string. Only single file is supported.')
        if self.__filename != fname:
            self.__filename = fname
            self.Modified()

    def GetFileName(self):
        """Get the set filename."""
        return self.__filename

    def Write(self, inputDataObject=None):
        """A Python focused conveinance method to perform the write out."""
        if inputDataObject:
            self.SetInputDataObject(inputDataObject)
        self.Modified()
        self.Update()

    def PerformWriteOut(self, inputDataObject, filename, objectName):
        """This method must be implemented. This is automatically called by
        ``RequestData`` for single inputs or composite inputs."""
        raise NotImplementedError('PerformWriteOut must be implemented!')

    def Apply(self, inputDataObject):
        """A convienace method if using these algorithms in a Python environment.
        """
        self.SetInputDataObject(inputDataObject)
        self.Modified()
        self.Update()

    def SetFormat(self, fmt):
        """Use to set the ASCII format for the writer default is ``'%.9e'``
        """
        if self.__fmt != fmt and isinstance(fmt, str):
            self.__fmt = fmt
            self.Modified()

    def GetFormat(self):
        return self.__fmt

    #### Following methods are for composite datasets ####

    def UseComposite(self):
        """True if input dataset is a composite dataset"""
        return self.__composite

    def SetBlockFileNames(self, n):
        """Gets a list of filenames based on user input filename and creates a
        numbered list of filenames for the reader to save out. Assumes the
        filename has an extension set already.
        """
        number = n
        count = 0
        while (number > 0):
            number = number // 10
            count = count + 1
        count = '%d' % count
        identifier = '_%.' + count + 'd'
        blocknum = [identifier % i for i in range(n)]
        # Check the file extension:
        ext = self.GetFileName().split('.')[-1]
        basename = self.GetFileName().replace('.%s' % ext, '')
        self.__blockfilenames = [basename + '%s.%s' % (blocknum[i], ext) for i in range(n)]
        return self.__blockfilenames

    def GetBlockFileName(self, idx):
        """Get the filename for a specific block if composite dataset.
        """
        return self.__blockfilenames[idx]


    def RequestData(self, request, inInfoVec, outInfoVec):
        """Subclasses must implement a ``PerformWriteOut`` method that takes an
        input data object and a filename. This method will automatically handle
        composite data sets.
        """
        inp = self.GetInputData(inInfoVec, 0, 0)
        if isinstance(inp, vtk.vtkMultiBlockDataSet):
            self.__composite = True
        # Handle composite datasets. NOTE: This only handles vtkMultiBlockDataSet
        if self.__composite:
            num = inp.GetNumberOfBlocks()
            self.SetBlockFileNames(num)
            for i in range(num):
                data = inp.GetBlock(i)
                name = inp.GetMetaData(i).Get(vtk.vtkCompositeDataSet.NAME())
                if data.IsTypeOf(self.InputType):
                    self.PerformWriteOut(data, self.GetBlockFileName(i), name)
                else:
                    warnings.warn('Input block %d of type(%s) not saveable by writer.' % (i, type(data)))
        # Handle single input dataset
        else:
            self.PerformWriteOut(inp, self.GetFileName(), None)
        return 1



################################################################################
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


    def PerformWriteOut(self, inputDataObject, filename, objectName):
        # Find cell centers
        filt = vtk.vtkCellCenters()
        filt.SetInputDataObject(inputDataObject)
        filt.Update()
        centers = dsa.WrapDataObject(filt.GetOutput(0)).Points
        # Get CellData
        wpdi = dsa.WrapDataObject(inputDataObject)
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
                   fmt=self.GetFormat(),
                   comments='')
        # Success for pipeline
        return 1

    def SetDelimiter(self, delimiter):
        """The string delimiter to use"""
        if self.__delimiter != delimiter:
            self.__delimiter = delimiter
            self.Modified()


################################################################################
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


    def PerformWriteOut(self, inputDataObject, filename, objectName):
        """Perfrom the file write to the given FileName with the given data
        object. The super class handles all the complicated stuff.
        """
        fname = filename.split('.')
        fname = '.'.join(fname[0:-1]) + '_%s.%s' % (objectName, fname[-1])
        writer = vtk.vtkXMLImageDataWriter()
        writer.SetFileName(fname)
        writer.SetInputDataObject(inputDataObject)
        writer.Write()
        # Success for pipeline
        return 1

    @smproperty.stringvector(name="FileName", panel_visibility="never")
    @smdomain.filelist()
    def SetFileName(self, fname):
        """Specify filename for the file to write."""
        WriterBase.SetFileName(self, fname)




################################################################################
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
    def SetFileName(self, fname):
        """Specify filename for the file to write."""
        WriteCellCenterData.SetFileName(self, fname)

    @smproperty.stringvector(name="Format", default_values='%.9e')
    def SetFormat(self, fmt):
        """Use to set the ASCII format for the writer default is ``'%.9e'``"""
        WriteCellCenterData.SetFormat(self, fmt)

    @smproperty.stringvector(name="Delimiter", default_values=',')
    def SetDelimiter(self, delimiter):
        """The string delimiter to use"""
        WriteCellCenterData.SetDelimiter(self, delimiter)
