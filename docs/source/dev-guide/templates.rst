Templates
=========

Here are a few templates for various types of algorithms to provide a place to
start developing your own readers, filters, writers, and sources!

Once you have your new algorithm implemented, head over to `this example`_ to learn
more about wrapping your algorithm for direct use in ParaView. Through decorating
a new subclass of your algorithm, you can define a user interface that ParaView
can easily yield to users!

.. _this example: ./snippets/composite-data-writers

Readers
-------

We've found that it is difficult to make generic templates for readers as there
are already so many reader base classes to choose from.
If you are developing a new reader, talk to one of the active developers on
[Slack](http://slack.pvgeo.org) and we can work with you to ensure you are using an appropriate base class.

Filters
-------

A filter that will preserve the input data type:

.. code-block:: python

    import vista
    # Import Helpers: TODO Check relativity
    from ..base import FilterPreserveTypeBase
    from .. import _helpers

    class FilterTemplate(FilterPreserveTypeBase):
        """A filter that preserves the input type template for you! Inheriting
        from ``FilterPreserveTypeBase`` allows your new filter to handle all
        the complicated processes necessary for making sure the pipeline properly
        sets up the output data object. All you have to so is appropriately fill
        out the ``RequestData`` method!
        """
        __displayname__ = 'Filter Template'
        __category__ = 'filter'
        def __init__(self, **kwargs):
            FilterPreserveTypeBase.__init__(self, **kwargs)
            self.__property = kwargs.get('property', None)

        def RequestData(self, request, inInfo, outInfo):
            """This is where you fill out your algorithm"""
            pdi = vista.wrap(self.GetInputData(inInfo, 0, 0)) # int args are port and index
            pdo = vista.wrap(self.GetOutputData(outInfo, 0)) # int arg is port
            # TODO: Perform your data processing here
            raise NotImplementedError('Code me up!')
            return 1 # ALWAYS return 1

        def set_property(self, prop):
            """A generic setter method for a private property"""
            if self.__property != prop:
                self.__property = prop
                self.Modified()



A filter that will alter the data type:

.. code-block:: python

    import vista
    # Import Helpers: TODO Check relativity
    from ..base import FilterBase
    from .. import _helpers

    class FilterTemplate(FilterBase):
        """A generic filter template for you! Inheriting from ``FilterBase``
        allows your new filter to be properly set up on the
        pipeline with ease. Be sure to properly set the input/output data object
        types and number of ports via the ``FilterBase`` super constructor.
        """
        __displayname__ = 'Filter Template'
        __category__ = 'filter'
        def __init__(self, **kwargs):
            FilterBase.__init__(self, nInputPorts=1, inputType='vtkDataSet',
                                nOutputPorts=1, outputType='vtkPolyData', **kwargs)
            self.__property = kwargs.get('property', None)

        def RequestData(self, request, inInfo, outInfo):
            """This is where you fill out your algorithm"""
            pdi = vista.wrap(self.GetInputData(inInfo, 0, 0)) # int args are port and index
            pdo = vista.wrap(self.GetOutputData(outInfo, 0)) # int arg is port

            # TODO: Perform your data processing here
            raise NotImplementedError('Code me up!')
            return 1 # ALWAYS return 1

        def set_property(self, prop):
            """A generic setter method for a private property"""
            if self.__property != prop:
                self.__property = prop
                self.Modified()



Need to include a data array selection in your filter? It's easy:


.. code-block:: python

    import vista
    # Import Helpers: TODO Check relativity
    from ..base import FilterBase
    from .. import _helpers

    class FilterTemplate(FilterBase):
        """A generic filter template with a data array selection for you!
        """
        __displayname__ = 'Filter Template'
        __category__ = 'filter'
        def __init__(self, **kwargs):
            FilterBase.__init__(self, nInputPorts=1, inputType='vtkDataSet',
                                nOutputPorts=1, outputType='vtkPolyData', **kwargs)
            self.__inputArray = [None, None]

        def RequestData(self, request, inInfo, outInfo):
            """This is where you fill out your algorithm"""
            pdi = vista.wrap(self.GetInputData(inInfo, 0, 0)) # int args are port and index
            pdo = vista.wrap(self.GetOutputData(outInfo, 0)) # int arg is port

            # Get input array in NumPy data structure
            field, name = self.__inputArray[0], self.__inputArray[1]
            arr =  pdi.get_scalar(name, field)

            # TODO: Perform your data processing here
            raise NotImplementedError('Code me up!')
            return 1 # ALWAYS return 1

        def SetInputArrayToProcess(self, idx, port, connection, field, name):
            """Used to set the input array(s)

            Args:
                idx (int): the index of the array to process
                port (int): input port (use 0 if unsure)
                connection (int): the connection on the port (use 0 if unsure)
                field (int): the array field (0 for points, 1 for cells, 2 for field, and 6 for row)
                name (int): the name of the array
            """
            if self.__inputArray[0] != field or self.__inputArray[1] != name:
                self.__inputArray[0] = field
                self.__inputArray[1] = name
                self.__filter.SetInputArrayToProcess(idx, port, connection, field, name)
                self.Modified()
            return 1


Writers
-------

.. code-block:: python

    # Import Helpers: TODO Check relativity
    from ..base import WriterBase
    from .. import _helpers

    class WriteTemplate(WriterBase):
        """A writer template for you! Write the overall description of this writer
        here. E.g. This writers takes ``XXX`` as and saves it to a file of the
        ``YYY`` format for use in software such as ZZZ.
        """
        __displayname__ = 'Write Template'
        __category__ = 'writer'
        def __init__(self, **kwargs):
            WriterBase.__init__(self, inputType='vtkDataSet', **kwargs)
            # Set private variables here!
            self.__foo = kwargs.get('foo', True)

        def perform_write_out(self, inputDataObject, filename):
            """Use ``inputDataObject`` and ``filename`` to save the VTK data object
            to your custom file type.

            Args:
                inputDataObject (vtkDataObject): This is guaranteed to be of the type specified by the ``inputType`` in your ``__init__`` unless you override ``FillInputPortInformation``.
                filename (str): A full filename with an index appended if needed. Use this string to save your data.

            Return:
            int: return 1 on success
            """
            raise NotImplementedError('Code me up!')
            # Always return 1
            return 1

        def set_foo(self, foo):
            """Set the foo variable"""
            if self.__foo != foo:
                self.__foo = foo
                self.Modified()




Sources
-------

.. code-block:: python

    import vista
    # Import Helpers: TODO: Check relativity
    from ..base import AlgorithmBase
    from .. import _helpers

    class TemplateSource(AlgorithmBase):
        """A source template for you! Write the overall description of this source
        here. E.g. This source produces a ``XXX`` object that describes some
        useful information.
        """
        __displayname__ = 'Template Source'
        __category__ = 'source'
        def __init__(self, **kwargs):
            AlgorithmBase.__init__(self,
                nInputPorts=0,
                nOutputPorts=1, outputType='vtkPolyData')
            # Set private variables here!
            self.__foo = kwargs.get('foo', True)

        def RequestData(self, request, inInfo, outInfo):
            """This is where you fill out your algorithm"""
            pdo = vista.wrap(self.GetOutputData(outInfo, 0))
            # TODO: Fill in the output data object: ``pdo``
            raise NotImplementedError('Code me up!')
            return 1

        def set_foo(self, foo):
            """Set the foo variable"""
            if self.__foo != foo:
                self.__foo = foo
                self.Modified()
