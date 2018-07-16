__all__ = [
    'PVGeoError',
    'ErrorObserver',
]

import re


class PVGeoError(Exception):
    """This is a custom error class for handling errors when proccessing on the VTK pipeline. It makes the error messages easy to decipher in ParaView and cleans the messages when used in Python outside of ParaView. When on the VTK pipeline, errors aren't really raised but passed over and printed to the console. This class makes decipher the error streams a whole lot easier for human eyes.
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
    def CleanMessage(message):
        return message.replace(PVGeoError.QUALIFIER_L, '').replace(PVGeoError.QUALIFIER_R, '')



class ErrorObserver:
    """A class for catching errors when processing on a VTK pipeline. The ``AlgorithmBase`` class handles setting up this observer on initialization.

    Example:
        >>> import PVGeo
        >>> # Only use this observer on sub classes of the AlgorithmBase:
        >>> f = PVGeo.AlgorithmBase()
        >>> f.Update()
        >>> if f.ErrorOccurred():
        >>>    print(f.ErrorMessage())
        ERROR: ...

    """
    def __init__(self):
        self.__ErrorOccurred = False
        self.__ErrorMessage = None
        self.__ErrorMessageEtc = None
        self.CallDataType = 'string0'
        # Object to observe:
        self.__observing = False

    def __call__(self, obj, event, message):
        self.__ErrorOccurred = True
        # Serch the message for a PVGeoError qualifier to extract
        msg = PVGeoError.SEARCHER.findall(message)
        if len(msg) > 0:
            info = '\nPVGeoError: '
            message = info + info.join(PVGeoError.CleanMessage(m) for m in msg)
        elif self.__ErrorMessage is not None:
            self.__ErrorMessageEtc = message
            return
        # if no qualifier is present and message has not already been set, entire message stream gets set
        self.__ErrorMessage = message
        print(message)

    def ErrorOccurred(self):
        """Ask self if an error has occured
        """
        occ = self.__ErrorOccurred
        self.__ErrorOccurred = False
        return occ

    def ErrorMessage(self, etc=False):
        """Get the last set error message

        Return:
            str: the last set error message
        """
        if etc:
            return self.__ErrorMessageEtc
        return self.__ErrorMessage

    def MakeObserver(self, algorithm):
        """Make this an observer of an algorithm
        """
        if self.__observing:
            raise RuntimeError('This error observer is already observing an algorithm.')
        algorithm.GetExecutive().AddObserver('ErrorEvent', self)
        algorithm.AddObserver('ErrorEvent', self)
        self.__observing = True
        return
