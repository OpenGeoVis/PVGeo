__all__ = ['getTimeStepFileIndex', 'setOutputTimesteps']


import numpy as np

# This is the function to get the requested time step
def _getUpdateTimestep(algorithm):
    """Returns the requested time value, or None if not present"""
    executive = algorithm.GetExecutive()
    outInfo = executive.GetOutputInformation(0)
    if outInfo.Has(executive.UPDATE_TIME_STEP()):
        return outInfo.Get(executive.UPDATE_TIME_STEP())
    else:
        return None


def _calculateTimeRange(num, dt=1.0):
    """Discretizes time range accoridng to step size `dt` in seconds"""
    return np.arange(0,num*dt,dt, dtype=float)


# --------------------------------- #
# Absolutely necessary functions for reading file series

def getTimeStepFileIndex(algorithm, files, dt=1.0):
    """
    Description
    -----------

    Parameters
    ----------
    `algorithm` : vtkDataObject (Proxy)
    - The data object on the pipeline (pass `self` from Programmable Sources)

    `files` : list
    - All the files. (Pass files incase we implement a method to read time value from file)

    `dt` : float, optional
    - The discrete value in seconds for the time step

    Return
    ------
    int

    - Returns the index for the file to be read in `files`
    """
    if len(files) < 2:
        # Only one file...
        return 0
    # Get the current timestep
    req_time = _getUpdateTimestep(algorithm)
    # Read the closest file
    xtime = _calculateTimeRange(len(files), dt=dt)
    return np.argmin(np.abs(xtime - req_time))


def setOutputTimesteps(algorithm, files, dt=1.0):
    """
    Description
    -----------

    Parameters
    ----------
    `algorithm` : vtkDataObject (Proxy)
    - The data object on the pipeline (pass `self` from Programmable Sources)

    `files` : list
    - All the files. (Pass files incase we implement a method to read time value from file)

    `dt` : float, optional
    - The discrete value in seconds for the time step

    Return
    ------
    - Returns the argument `algorithm`
    """
    if len(files) < 2:
        # Only one file so do not update time steps
        return algorithm
    executive = algorithm.GetExecutive()
    outInfo = executive.GetOutputInformation(0)
    # Calculate list of timesteps here
    xtime = _calculateTimeRange(len(files), dt=dt)
    outInfo.Remove(executive.TIME_STEPS())
    for i in range(len(files)):
        outInfo.Append(executive.TIME_STEPS(), xtime[i])
    # Remove and set time range info
    outInfo.Remove(executive.TIME_RANGE())
    outInfo.Append(executive.TIME_RANGE(), xtime[0])
    outInfo.Append(executive.TIME_RANGE(), xtime[-1])
    return algorithm
