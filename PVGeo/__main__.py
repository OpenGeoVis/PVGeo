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
    import glob
    test_file_strings = glob.glob('**/__test__.py', recursive=True)
    # Remove extensions and change to module import syle
    module_strings = [str[0:len(str)-3].replace('/', '.') for str in test_file_strings]
    suites = [unittest.defaultTestLoader.loadTestsFromName(str) for str
              in module_strings]
    testSuite = unittest.TestSuite(suites)
    unittest.TextTestRunner(verbosity=2).run(testSuite)
    return None


if __name__ == '__main__':
    import sys
    arg = sys.argv[1]
    if arg.lower() == 'test':
        test()
    else:
        raise RuntimeError('Unknown argument: %s' % arg)
