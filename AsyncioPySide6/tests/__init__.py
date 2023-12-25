import unittest
from .test_AsyncioPySide6 import TestAsyncioPySide6

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestAsyncioPySide6))
    return test_suite
