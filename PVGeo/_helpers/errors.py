__all__ = [
    'PVGeoError',
    'ErrorObserver',
    'HiddenPrints',
]

import re
import os
import sys


class PVGeoError(Exception):
    """This is a custom error class for handling errors when proccessing on the
    VTK pipeline. It makes the error messages easy to decipher in ParaView and
    cleans the messages when used in Python outside of ParaView. When on the VTK
    pipeline, errors aren't really raised but passed over and printed to the
    console. This class makes decipher the error streams a whole lot easier for
    human eyes.
    """
    QUALIFIER_L = '@@@@PVGeoError ---> '
    QUALIFIER_R = ' <--- PVGeoError@@@@'
    SEARCHER = re.compile(r'@@@@PVGeoError --->.+?<--- PVGeoError@@@@', re.MULTILINE|re.DOTALL)


    def __init__(self, message):
        # Place special characters arround the message for easy extraction
        self.message = '\n\n\n\n' + self.QUALIFIER_L + message + self.QUALIFIER_R + '\n\n\n\n'


    def __str__(self):
        return self.message #.replace(self.QUALIFIER, '')

    @staticmethod
    def clean_message(message):
        return message.replace(PVGeoError.QUALIFIER_L, '').replace(PVGeoError.QUALIFIER_R, '')



class ErrorObserver:
    """A class for catching errors when processing on a VTK pipeline. The
    ``AlgorithmBase`` class handles setting up this observer on initialization.

    Example:
        >>> import PVGeo
        >>> # Only use this observer on sub classes of the AlgorithmBase:
        >>> f = PVGeo.AlgorithmBase()
        >>> f.Update()
        >>> if f.error_occurred():
        >>>    print(f.get_error_message())
        ERROR: ...

    """
    def __init__(self):
        self.__error_occurred = False
        self.__get_error_message = None
        self.__get_error_messageEtc = None
        self.CallDataType = 'string0'
        # Object to observe:
        self.__observing = False

    def __call__(self, obj, event, message):
        self.__error_occurred = True
        # Serch the message for a PVGeoError qualifier to extract
        msg = PVGeoError.SEARCHER.findall(message)
        if len(msg) > 0:
            info = '\nPVGeoError: '
            message = info + info.join(PVGeoError.clean_message(m) for m in msg)
        elif self.__get_error_message is not None:
            self.__get_error_messageEtc = message
            return
        # if no qualifier is present and message has not already been set, entire message stream gets set
        self.__get_error_message = message
        print(message)

    def error_occurred(self):
        """Ask self if an error has occured
        """
        occ = self.__error_occurred
        self.__error_occurred = False
        return occ

    def get_error_message(self, etc=False):
        """Get the last set error message

        Return:
            str: the last set error message
        """
        if etc:
            return self.__get_error_messageEtc
        return self.__get_error_message

    def make_observer(self, algorithm):
        """Make this an observer of an algorithm
        """
        if self.__observing:
            raise RuntimeError('This error observer is already observing an algorithm.')
        algorithm.GetExecutive().AddObserver('ErrorEvent', self)
        algorithm.AddObserver('ErrorEvent', self)
        self.__observing = True
        return


class HiddenPrints:
    """Use this object to hide print statements when perfroming a task.
    This is used to suppress printed warnings from discretize on import:

    Example:
    >>> with HiddenPrints():
    ...     import discretize
    """
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
