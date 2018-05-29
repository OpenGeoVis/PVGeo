"""
Example python file reader demonstrating some of the features available for
python programmable file readers.
This file reader simply lists the file name at the requested time step
Credit for implementing time series goes to: Daan van Vugt <daanvanvugt@gmail.com>
"""
# Name to be used for coding/macros
Name = 'ExamplePythonReader'
# Label for the reader in the menu
Label = 'Example Python Reader'
# The source menu category
FilterCategory = 'PVGP Readers'

Extensions = ''
ReaderDescription = 'All Files: Example Python Reader'

# A general overview of the plugin
Help = 'This reader provides a starting point for making a file reader in a Programmable Python Source.'

# Specify zero for readers
NumberOfInputs = 0
# No input data type
# NEED to specify output type!
OutputDataType = 'vtkUnstructuredGrid'

# Any extra XML GUI components you might like:
ExtraXml = ''

# These are the parameters/properties of the plugin:
Properties = dict(
    Print_File_Names=True,
    Time_Step=1.0 # This parameter should be present for all READERS that have `FileSeries` set to True. It will show up as an advanced parameter in the GUI. This will not work for FILTERS.
)

# This is the description for each of the properties variable:
#- Include if you'd like. Totally optional.
#- The variable name (key) must be identical to the property described.
PropertiesHelp = dict(
    Print_File_Names='This is a description about the Print_File_Names property! This will simple print the file name at the current time step if set to true.',
    Time_Step='An advanced property for the time step in seconds.'
)

# from paraview import vtk is done automatically in the reader
def RequestData(self):
    """Create a VTK output given the list of FileNames and the current timestep.
    This script can access self and FileNames and should return an output of type OutputDataType defined above"""
    from PVGPpy.read import getTimeStepFileIndex

    # This finds the index for the FileNames for the requested timestep
    i = getTimeStepFileIndex(self, FileNames, dt=Time_Step)

    """If you specifically do not want the ability to read time series
    Then delete the above code and access the file name by adding a string
    variable called `FileName` to the Properties dict. """
    # --------------------- #
    # Generate Output Below
    if Print_File_Names:
        print(FileNames[i])


def RequestInformation(self):
    from PVGPpy.read import setOutputTimesteps
    # This is necessary to set time steps
    setOutputTimesteps(self, FileNames, dt=Time_Step)
