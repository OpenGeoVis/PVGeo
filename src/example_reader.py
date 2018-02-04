"""
Example python file reader demonstrating some of the features available for
python programmable file readers.
This file reader simply lists the file name at the requested time step
Credit for implementing time series goes to: Daan van Vugt <daanvanvugt@gmail.com>
"""
Name = 'ExamplePythonReader'        # Name to be used for coding/macros
Label = 'Example Python Reader'     # Label for the reader in the menu
FilterCategory = 'CSM GP Readers'   # The source menu category

Extensions = ''
ReaderDescription = 'All Files: Example Python Reader'

# A general overview of the plugin
Help = 'This reader provides a starting point for making a file reader in a Programmable Python Source.'

NumberOfInputs = 0                          # Specify zero for readers
# No input data type
OutputDataType = 'vtkUnstructuredGrid'      # NEED to specify

# Any extra XML GUI components you might like:
ExtraXml = ''

# These are the parameters/properties of the plugin:
Properties = dict(
    Print_File_Names=True,
)

# This is the description for each of the properties variable:
#- Include if you'd like. Totally optional.
#- The variable name (key) must be identical to the property described.
PropertiesHelp = dict(
    Print_File_Names='This is a description about the Print_File_Names property! This will simple print the file name at the current time step if set to true.'
)

# from paraview import vtk is done automatically in the reader
def RequestData(self):
    """Create a VTK output given the list of filenames and the current timestep.
    This script can access self and FileNames and should return an output of type
    OutputDataType above"""
    import numpy as np

    def GetUpdateTimestep(algorithm):
        """Returns the requested time value, or None if not present"""
        executive = algorithm.GetExecutive()
        outInfo = executive.GetOutputInformation(0)
        if outInfo.Has(executive.UPDATE_TIME_STEP()):
            return outInfo.Get(executive.UPDATE_TIME_STEP())
        else:
            return None
    # Get the current timestep
    req_time = GetUpdateTimestep(self)
    # Read the closest file
    #np.asarray([get_time(file) for file in FileNames])
    xtime = np.arange(len(FileNames), dtype=float)
    i = np.argwhere(xtime == req_time)

    """If you specifically do not want the ability to read time series
    Then delete the above code and access the file name by adding a string
    variable called `FileName` to the Properties dict. """
    # --------------------- #
    # Generate Output Below
    if Print_File_Names:
        print(FileNames[i])


"""
Given a list of filenames this script should output how many timesteps are available.
See paraview guide 13.2.2
"""
def RequestInformation(self):
    def setOutputTimesteps(algorithm):
        executive = algorithm.GetExecutive()
        outInfo = executive.GetOutputInformation(0)
        # Calculate list of timesteps here
        #np.asarray([get_time(file) for file in FileNames])
        xtime = range(len(FileNames))
        outInfo.Remove(executive.TIME_STEPS())
        for i in range(len(FileNames)):
            outInfo.Append(executive.TIME_STEPS(), xtime[i])
        # Remove and set time range info
        outInfo.Remove(executive.TIME_RANGE())
        outInfo.Append(executive.TIME_RANGE(), xtime[0])
        outInfo.Append(executive.TIME_RANGE(), xtime[-1])

    # --------------------- #
    # Generate Output Below
    setOutputTimesteps(self)
