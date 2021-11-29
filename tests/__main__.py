"""This module provideas a convienance method to run all of the tests for PVGeo.
Each suite within PVGeo has its own ``*_test.py`` file for all unittest
implementations to live and each file is executable on its own.
"""

__all__ = [
    'test',
]

import unittest
import glob
import os
import sys

if sys.version_info >= (3, 0):
    import faulthandler

    faulthandler.enable()


def test(close=False):
    """This is a convienance method to run all of the tests in ``PVGeo`` while
    in an active python environment.

    Args:
        close (bool): exit the python environment with error code if errors or failures occur
    """
    try:
        from colour_runner.runner import ColourTextTestRunner as TextTestRunner
    except ImportError:
        from unittest import TextTestRunner
    os.chdir(os.path.dirname(__file__))
    test_file_strings = glob.glob('*_test.py')
    module_strings = [str[0 : len(str) - 3] for str in test_file_strings]
    suites = [
        unittest.defaultTestLoader.loadTestsFromName(str) for str in module_strings
    ]
    testSuite = unittest.TestSuite(suites)

    # unittest.TextTestRunner(verbosity=2).run(testSuite)
    run = TextTestRunner(verbosity=2).run(testSuite)
    if close:
        exit(len(run.failures) > 0 or len(run.errors) > 0)
    return run


if __name__ == '__main__':
    close = False
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg.lower() == 'close':
            close = True
        else:
            raise RuntimeError('Unknown argument: %s' % arg)
    test(close=close)
