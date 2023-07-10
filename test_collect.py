#!/usr/bin/python3
"""
Python "unittest" test module for photo collector library/program
"""
import os
import re
import subprocess
import sys
import unittest

UNITTEST_VERBOSITY = 1

class CommonTest(unittest.TestCase):

    def setUp(self):
        """Common setup method"""


class TestCollectStructure(CommonTest):
    """
    Test the "collect.py" library and program
    """

    def test_collector_library(self):
        try:
            import collect
        except (ImportError, ModuleNotFoundError):
            self.fail("Unable to import collect.py library")
        col = collect.Collect()

    def test_collector_import_class(self):
        try:
            from collect import Collect
        except ModuleNotFoundError:
            self.fail("Unable to import collect.py library")
        except ImportError:
            self.fail("Unable to import 'Collect' class from collect.py library")
        col = Collect()

    def test_collector_program(self):
        try:
            subprocess.call('py collect.py')
        except subprocess.CalledProcessError:
            self.fail("Unable to invoke collect.py program")


unittest.main(verbosity=UNITTEST_VERBOSITY)
