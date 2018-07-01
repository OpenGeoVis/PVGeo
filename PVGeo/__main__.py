__all__ = [
    'test',
]

def test():
    """
    @desc: This is a convienance method to run all of the tests in `PVGeo`.

    @notes:
    This can be executed from either the command line of within a standard Python environment:

    ```bash
    $ python -m PVGeo test
    ```

    ```py
    >>> import PVGeo
    >>> PVGeo.test()
    ```
    """
    import unittest
    import fnmatch
    import os
    path = os.path.dirname(__file__) # path to remove
    path = path[0:path.rfind('/')]
    test_file_strings = []
    for root, dirnames, filenames in os.walk(os.path.dirname(__file__)):
        for filename in fnmatch.filter(filenames, '__test__.py'):
            test_file_strings.append(os.path.join(root, filename).replace(path, ''))
    # Remove extensions and change to module import syle
    module_strings = [str[1:len(str)-3].replace('/', '.') for str in test_file_strings]
    suites = [unittest.defaultTestLoader.loadTestsFromName(str) for str
              in module_strings]
    testSuite = unittest.TestSuite(suites)
    return unittest.TextTestRunner(verbosity=2).run(testSuite)


if __name__ == '__main__':
    import sys
    arg = sys.argv[1]
    if arg.lower() == 'test':
        test()
    else:
        raise RuntimeError('Unknown argument: %s' % arg)
