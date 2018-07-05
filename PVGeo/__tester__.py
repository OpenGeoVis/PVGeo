__all__ = [
    'test',
]
import unittest
import fnmatch
import os

try:
    from colour_runner.runner import ColourTextTestRunner as TextTestRunner
except ImportError:
    from unittest import TextTestRunner


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
    test_file_strings = []
    for root, dirnames, filenames in os.walk('.'):
        for filename in fnmatch.filter(filenames, '__test__.py'):
            test_file_strings.append(os.path.join(root, filename))
    # Remove extensions and change to module import syle
    module_strings = [mod[2:len(mod)-3].replace('/', '.') for mod in test_file_strings]
    suites = [unittest.defaultTestLoader.loadTestsFromName(mod) for mod
              in module_strings]
    testSuite = unittest.TestSuite(suites)
    run = TextTestRunner(verbosity=2).run(testSuite)
    if close:
        exit(len(run.failures) > 0 or len(run.errors) > 0)
    return run

if __name__ == '__main__':
    test(True)
