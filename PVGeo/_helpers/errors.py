

class ErrorObserver:
    """@desc: A class for catching errors when testing

    Usage:
    ```py
    e = _helpers.ErrorObserver()

    f = algorithm()
    f.AddObserver('ErrorEvent', e)

    f.Update()
    if e.ErrorOccurred():
        print(e.ErrorMessage())

    ```

    """
    def __init__(self):
        self.__ErrorOccurred = False
        self.__ErrorMessage = None
        self.CallDataType = 'string0'

    def __call__(self, obj, event, message):
        self.__ErrorOccurred = True
        self.__ErrorMessage = message

    def ErrorOccurred(self):
        occ = self.__ErrorOccurred
        self.__ErrorOccurred = False
        return occ

    def ErrorMessage(self):
        return self.__ErrorMessage

    def MakeObserver(self, algorithm):
        algorithm.GetExecutive().AddObserver('ErrorEvent', self)
        algorithm.AddObserver('ErrorEvent', self)
        return
