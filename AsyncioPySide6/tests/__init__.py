import unittest
from .test_AsyncioPySide6 import TestAsyncioPySide6
from .test_config import TestAsyncioPySide6Config, TestConfigFunctions

def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestAsyncioPySide6))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestAsyncioPySide6Config))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestConfigFunctions))
    return test_suite
