__all__ = [
    'test',
]

def test(close=False):
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
    run = unittest.TextTestRunner(verbosity=2).run(testSuite)
    if close:
        exit(len(run.failures) > 0 or len(run.errors) > 0)
    return run


if __name__ == '__main__':
    import sys
    arg = sys.argv[1]
    if arg.lower() == 'test':
        test(True)
    else:
        raise RuntimeError('Unknown argument: %s' % arg)
