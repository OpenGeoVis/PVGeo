__all__ = [
    'test',
]
__displayname__ = 'Test Runner'

import unittest
import fnmatch
import os


def test(close=False):
    """This is a convienance method to run all of the tests in ``PVGeo`` while
    in an active python environment.

    Note:
        This can be executed from either the command line of within a standard Python environment.

    Example:
        .. code-block:: bash

           # From the command line
           $ python -m PVGeo test

        >>> # From an active Python environment
        >>> import PVGeo
        >>> PVGeo.test()

    """
    try:
        from colour_runner.runner import ColourTextTestRunner as TextTestRunner
    except ImportError:
        from unittest import TextTestRunner
    test_file_strings = []
    for root, dirnames, filenames in os.walk(os.path.dirname(__file__)):
        for filename in fnmatch.filter(filenames, '__test__.py'):
            test_file_strings.append(os.path.join(root, filename))
    # Remove extensions and change to module import syle
    test_file_strings = [s.replace(os.path.dirname(os.path.dirname(__file__)), '') for s in test_file_strings]
    idx = 0
    if test_file_strings[0][0] == '/':
        idx = 1
    module_strings = [mod[idx:len(mod)-3].replace('/', '.') for mod in test_file_strings]
    suites = [unittest.defaultTestLoader.loadTestsFromName(mod) for mod
              in module_strings]
    testSuite = unittest.TestSuite(suites)
    run = TextTestRunner(verbosity=2).run(testSuite)
    if close:
        exit(len(run.failures) > 0 or len(run.errors) > 0)
    return run
