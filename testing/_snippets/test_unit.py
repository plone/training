# -*- coding: utf-8 -*-

from plonetraining.testing.helper_functions import double_number

import unittest


class SomeTest(unittest.TestCase):
    def test_a_feature(self):
        self.assertTrue(1 == 1)
        self.assertEqual(1, 1)

    def test_double_number(self):
        self.assertEqual(double_number(1), 2)
        self.assertEqual(double_number(2), 4)
        self.assertNotEqual(double_number(2), 3)
