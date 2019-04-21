__all__ = [
    '_calculate_time_range',
    'update_time_steps',
    'get_requested_time',
    'get_input_time_steps',
    'get_combined_input_time_steps',
]

import numpy as np
import collections


def _calculate_time_range(nt, dt=1.0):
    """Discretizes time range accoridng to step size ``dt`` in seconds
    """
    return np.arange(0,nt*dt,dt, dtype=float)


def update_time_steps(algorithm, nt, dt=1.0, explicit=False):
    """Handles setting up the timesteps on on the pipeline for a file series reader.

    Args:
        algorithm (vtkDataObject): The data object (Proxy) on the pipeline
            (pass `self` from algorithm subclasses)
        nt (int or list): Number of timesteps (Pass a list to use length of
            that list)
        dt (float): The discrete value in seconds for the time step.
        explicit (boolean): if true, this will treat the nt argument as the exact
            timestep values to use

    Return:
        numpy.array : Returns the timesteps as an array
    """
    if explicit and isinstance(nt, collections.Iterable):
        timesteps = nt
    else:
        if isinstance(nt, collections.Iterable):
            nt = len(nt)
        timesteps = _calculate_time_range(nt, dt=1.0)
    if len(timesteps) < 1:
        # NOTE: we may want to raise a warning here on the dev side.
        #       if developing a new algorithm that uses this, you may want to
        #       know exactly when this failse to update
        #'update_time_steps() is not updating because passed time step values are NULL.'
        return None
    executive = algorithm.GetExecutive()
    oi = executive.GetOutputInformation(0)
    #oi = outInfo.GetInformationObject(0)
    oi.Remove(executive.TIME_STEPS())
    oi.Remove(executive.TIME_RANGE())
    for t in timesteps:
        oi.Append(executive.TIME_STEPS(), t)
    oi.Append(executive.TIME_RANGE(), timesteps[0])
    oi.Append(executive.TIME_RANGE(), timesteps[-1])
    return timesteps


def get_requested_time(algorithm, outInfo, idx=0):
    """Handles setting up the timesteps on on the pipeline for a file series
    reader.

    Args:
        algorithm (vtkDataObject) : The data object (Proxy) on the pipeline
            (pass `self` from algorithm subclasses)
        outInfo (vtkInformationVector) : The output information for the
            algorithm
        idx (int) : the index for the output port

    Return:
        int : the index of the requested time

    Example:
        >>> # Get requested time index
        >>> i = _helpers.get_requested_time(self, outInfo)
    """
    executive = algorithm.GetExecutive()
    timesteps = algorithm.get_time_step_values()
    outInfo = outInfo.GetInformationObject(idx)
    if timesteps is None or len(timesteps) == 0:
        return 0
    elif outInfo.Has(executive.UPDATE_TIME_STEP()) and len(timesteps) > 0:
        utime = outInfo.Get(executive.UPDATE_TIME_STEP())
        return np.argmin(np.abs(np.array(timesteps) - utime))
    else:
        # if we cant match the time, give first
        if not len(timesteps) > 0:
            raise AssertionError('Number of timesteps must be greater than 0')
        return 0


def get_input_time_steps(algorithm, port=0, idx=0):
    """Get the timestep values for the algorithm's input

    Args:
        algorithm (vtkDataObject) : The data object (Proxy) on the pipeline
            (pass `self` from algorithm subclasses)
        port (int)  : the input port
        idx (int) : optional : the connection index on the input port

    Return:
        list : the time step values of the input (if there arn't any, returns ``None``)
    """
    executive = algorithm.GetExecutive()
    ii = executive.GetInputInformation(port, idx)
    return ii.Get(executive.TIME_STEPS())


def get_combined_input_time_steps(algorithm, idx=0):
    """This will iterate over all input ports and combine their unique timesteps
    for an output algorithm to have.

    Args:
        algorithm (vtkDataObject) : The data object (Proxy) on the pipeline
            (pass `self` from algorithm subclasses)

    Return:
        np.ndarray : a 1D array of all the unique timestep values (empty array if no time variance)
    """
    executive = algorithm.GetExecutive()
    tsteps = []
    for port in range(executive.GetNumberOfInputPorts()):
        ii = executive.GetInputInformation(port, idx)
        ti = ii.Get(executive.TIME_STEPS())
        if ti is None: ti = np.array([])
        tsteps.append(ti)
    return np.unique(np.concatenate(tsteps, 0))
