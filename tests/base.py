from __future__ import print_function
import unittest
import time

class TestBase(unittest.TestCase):
    """
    Base Class for all test classes to add timing support
    """
    def setUp(self):
        self.startTime = time.time()
        return

    def tearDown(self):
        self.time = time.time() - self.startTime
        #TODO: print(" in %.3fs " % (self.time) )
        return
