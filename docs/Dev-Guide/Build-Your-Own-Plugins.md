[hierarchy]: https://en.wikipedia.org/wiki/Class_hierarchy
[pv-guide]: https://www.paraview.org/Wiki/Python_Programmable_Filter

!!! question "Questions or Concerns?"
    If you have any questions or concerns about how to make your own plugins, post a comment at the bottom of this page.

All of the plugins for ParaView that we develop in this repository are expansions of the **Programmable Source/Filter** native to ParaView. These are general purpose sources/filters that you can program using Python within the ParaView GUI. We are expanding these general purpose sources/filters to have more specific functionality, and thus we treat the native **Programmable Source/Filter** in a [**hierarchy**][hierarchy] manner such that our plugins inherit the functionality of those sources/filters then specialize that functionality to a specific task. Ways we specialize the plugins include added GUI parameters, specifying output data types, and designating input/output types.

Since a comprehensive guide on using the general purpose **Programmable Source/Filter** in ParaView can be found [**here**][pv-guide], we will focus on describing how you can use the build scripts and format of the *PVGeophysics* code base to build plugins like what we have developed.


## Plugin Components
First, let's take a look at the example plugins found under the `src/` directory. There are two example plugins here: a reader (`src/example_reader.py`) and a filter (`src/example_filter.py`). These two example plugins overall have the same structure with subtle differences for their respective functionality as a reader (no input data source) of data filter (has 1 or many data input sources). We have generated these two examples as templates for you when you decide to start coding up your own plugins as they outline all of the available features of our build scripts for what you can implement into your plugin. Let's start by taking a look at the example reader plugin.

### Plugin Attributes

Examine the table below to learn how to use each of the plugin attributes. Hover over the <a class="md-footer-social__link fa fa-info-circle" title="This is an example description"></a> icons to see a description of that attribute.



| Attribute               | Info | Example | Reader | Filter |
| :---------------------- |:--: |:------------------- | :-: | :-:|
| `Name` | <a class="md-footer-social__link fa fa-info-circle" title="Name of the plugin to be used for coding/macros or reference within ParaView. Think of this link a data object name. This cannot contain spaces."></a> | `:::py Name = 'ExamplePythonReader'`  | ✅ | ✅ |
| `Label` | <a class="md-footer-social__link fa fa-info-circle" title="Label for the reader in the menu. This is the name you will see appear in GUI menus. Make this label easy to read and concise."></a>| `:::py Label = 'Example Python Reader'`| ✅ | ✅ |
| `FilterCategory` | <a class="md-footer-social__link fa fa-info-circle" title="The menu category this plugin will appear in under the appropriate menu of Sources or Filters within ParaView."></a> | `:::py FilterCategory = 'PVGP Readers'`| ✅ | ✅ |
| `Extensions` | <a class="md-footer-social__link fa fa-info-circle" title="An attribute to contain possible file extensions for a reader plugin so ParaView can autodetect whether or not to use this plugin as a file reader when you open a file. The is a single str of extensions separated by spaces. Do not include the dot part of the extensions."></a> | `:::py Extensions = 'txt dat csv'` | ✅ | ❌ |
| `ReaderDescription` | <a class="md-footer-social__link fa fa-info-circle" title="This is a brief Description of the plugin that will appear in the ParaView GUI. Keep this to a small phrase."></a> | `:::py ReaderDescription = 'All Files: Example Python Reader'` | ✅ | ❌ |
| `Help` | <a class="md-footer-social__link fa fa-info-circle" title="A general overview of the plugin. This should be an encompassing description of the plugin's functionality, i.e. write a paragraph."></a> | `:::py Help = 'This reader provides a starting point for making a file reader in a Programmable Python Source.'` | ✅ | ✅ |
| `NumberOfInputs` | <a class="md-footer-social__link fa fa-info-circle" title="This is the number of inputs this plugin will have. For readers, it is necessary to specify this as ZERO! A filter can have many but we wouldn't advise going over three."></a> | `:::py NumberOfInputs = 1` | ✅ | ✅ |
| `InputDataType` | <a class="md-footer-social__link fa fa-info-circle" title="This is the type of VTK data object that this plugin will will take as an input from the upstream pipeline object. For a list of possible VTK data types, see this list below this table."></a> | `:::py InputDataType = 'vtkTable'` | ❌ | ✅ |
| `OutputDataType` | <a class="md-footer-social__link fa fa-info-circle" title="This is the type of VTK data object that this plugin will output on the pipeline. For a list of possible VTK data types, see this list below this table."></a> | `:::py OutputDataType = 'vtkUnstructuredGrid'`| ✅ | ✅ |
| `NumberOfInputArrayChoices` | <a class="md-footer-social__link fa fa-info-circle" title="Specify the number of input array choices you would like to have for the filter. This enables a drop-down menu for the user to select data arrays from the input data object."></a> | `:::py NumberOfInputArrayChoices = 1`| ❌ | ✅ |
| `InputArrayLabels` | <a class="md-footer-social__link fa fa-info-circle" title="This is an optional list of str display names for the input arrays if you specified to have one or more in NumberOfInputArrayChoices"></a>| `:::py InputArrayLabels = ['Input Array']`| ❌ | ✅ |
| `ExtraXml`  | <a class="md-footer-social__link fa fa-info-circle" title="Any extra XML GUI components you might like to add to the plugin that are not incorporated in the build script. See the link for more info on possible features to add."></a><a href="https://www.paraview.org/Wiki/ParaView/Plugin_HowTo" class="md-footer-social__link fa fa-link" title="See this webpage for more info on possible XML features to add."></a>| `:::py ExtraXml = ''`| ✅ | ✅ |
| `FileSeries` | <a class="md-footer-social__link fa fa-info-circle" title="A boolean to control whether or not you want to use file series on a reader plugin. Defaults to True"></a> | `:::py FileSeries = True` | ✅ | ❌ |


??? info "VTK Data Types Implemented"
    Here is a list of the VTK data types you can specify for the `OutputDataType` attribute.

    - `:::py ''` (Empty string will have an output same as the input)
    - `'vtkPolyData'`
    - `'vtkStructuredPoints'`
    - `'vtkStructuredGrid'`
    - `'vtkRectilinearGrid'`
    - `'vtkUnstructuredGrid'`
    - `'vtkPiecewiseFunction'`
    - `'vtkImageData'`
    - `'vtkDataObject'`
    - `'vtkPointSet'`
    - `'vtkUniformGrid'`
    - `'vtkCompositeDataSet'`
    - `'vtkMultiBlockDataSet'`
    - `'vtkHyperOctree'`
    - `'vtkTable'`
    - `'vtkGraph'`
    - `'vtkTree'`


### Plugin Parameters
The next two things we specify are the parameters (`Properties`) and descriptions (`PropertiesHelp`) of those parameters for the plugin in key-value pair dictionaries. The key is the name of the parameter, and the value is the default value of the parameter or the description of that parameter. These values can be dynamically typed to one of the following: `bool`, `int`, `float`, or `str` (uniform lists/tuples of these types are also accepted). The following example demonstrates how we might declare several parameters:

```py
# These are the parameters/properties of the plugin:
Properties = dict(
    test_bool=True,
    test_int=123,
    test_int_vector=[1, 2, 3],
    test_double=1.23,
    test_double_vector=[1.1, 2.2, 3.3],
    test_string='string value',
    Time_Step=1.0, # This parameter should be present for READERS
)

# This is the description for each of the properties variable:
#- Include if you'd like. Totally optional.
#- The variable name (key) must be identical to the property described.
PropertiesHelp = dict(
    test_bool='This is a description of the test_bool property!'
)
```


### Plugin Processing Scripts

Now that we have declared all of the attributes and parameters of this plugin, it is time to write the code and implement the functionality of this plugin! There are two types of scripts that we need to fill out for out plugins: `:::py def RequestData(self)` and `:::py def RequestInformation(self)`. It is important to note that any of the parameters specified in the `Properties` attribute are accessible in these scripts. For example, we specified the `test_bool` parameter, and we can simply access it by assuming it is in our namespace: `:::py if test_bool: print('We accessed test_bool')`.

#### RequestData
This method is where all of the main processing should occur. It constructs the VTK output given the parameters specified and the input data. For readers, the variable `FileNames` (index-able list of files) is accessible in the namespace. It is essential that you grab the pointers to the input and output of your plugin through the `:::py self` object.

??? example "Example `:::py def RequestData(self)` for a READER"
    ```py
    # Example for a READER
    def RequestData(self):
        from PVGPpy.read import getTimeStepFileIndex

        # This finds the index for the FileNames for the requested timestep
        i = getTimeStepFileIndex(self, FileNames, dt=Time_Step)

        """If you specifically do not want the ability to read time series
        Then delete the above code know that a list of file names will be given in the parameter `FileNames` which you can iterate over. """
        # --------------------- #
        pdo = self.GetOutput() # VTK Data Type specified in `OutputDataType`
        # Generate Output Below
        if Print_File_Names:
            # NOTE: FileNames is accessible here for READERS
            print(FileNames[i])

    ```

??? example "Example `:::py def RequestData(self)` for a FILTER"
    ```py
    # Example for a FILTER
    def RequestData(self):
        import PVGPpy.helpers as inputhelp
        # Here we grab the input and output data objects.
        pdi = self.GetInput() # VTK Data Type specified in `InputDataType`
        pdo = self.GetOutput() # VTK Data Type specified in `OutputDataType`

        # --------------------- #
        # Now fill in your processing for what you would like to do
        if test_bool:
            print(name)
        else:
            print(field)

    ```

#### RequestInformation
This method is where we set metadata about the output of the plugin. Use if you need to set output extents or number of time steps.

??? example "Example `:::py def RequestInformation(self)` for a READER"
    ```py
    # Example for a READER
    def RequestInformation(self):
        from paraview import util
        from PVGPpy.read import setOutputTimesteps
        # This is necessary to set time steps
        setOutputTimesteps(self, FileNames, dt=Time_Step)
        # Here's an example of setting extents that might be necessary for plugin to function correctly:
        # Get nx,ny,nz from input file somehow
        util.SetOutputWholeExtent(self, [0,nx-1, 0,ny-1, 0,nz-1])
    ```

??? example "Example `:::py def RequestInformation(self)` for a FILTER"
    ```py
    # Example for a FILTER
    def RequestInformation(self):
        from paraview import util
        # This script is usually not necessary for FILTERS
        # Here's an example of setting extents that might be necessary for plugin to function correctly:
        #util.SetOutputWholeExtent(self, [0,nx-1, 0,ny-1, 0,nz-1])

    ```

## Make Your Own
We think the best way to demonstrate how to do this is for you to check out a plugin already developed in the PVGP repository. For an example reader, check out the **Read Delimited Text File To Table** reader in `src/readers/read_delimited_file_to_table.py`. For an example filter, check out the **Normalize Array** filter in `src/filters/filter_normalize_array.py` which demonstrates how to add custom XML and how to specify input arrays to process.

!!! warning
    Note how that in our plugins, the bulk of the VTK data object construction occurs in a call to the `PVGPpy` module. We do this so that we can version control the backend functionality of these plugins. This is necessary to implement in this manner as ParaView state files will save the scripts specified in the plugin at a given time, and if a bug in that functionality is fixed and you update PVGP, it might not reflect in some of your saved projects unless we abstract the functionality the way we do. Think of plugins built in the `src/` directory as abstractions or high level instructions whereas the bulk functionality and processing of these plugins occur in the `PVGPpy` package which we modulize and version control.


Now that you have an idea of how to construct plugins so that our build scripts will add GUI parameters and install the plugin to ParaView, let's get started describing how to make a plugin! First, make a copy of either the example reader or filter template and rename it to something meaningful and place that file in either the `src/readers/` or `src/filters/` directory appropriately. Then go ahead and change all of the attributes specified [**above**](#plugin-attributes) to declare the metadata for your new plugin. Then add the necessary parameters for your plugin like shown [**above**](#plugin-parameters) and decide what kind of action you plugin will take given its input and parameters to construct the `:::py def RequestData(self)` script. Once you think you are done creating the plugin, run the `src/build_plugins.sh` script through your terminal by executing `:::bash sh src/build_plugins.sh` and make sure no red errors output when building your plugin. If the build was successful, restart ParaView and try using your new plugin!
