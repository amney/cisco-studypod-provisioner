"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class BookTest(TestCase):
    def test_creation(self):
        self.assertEqual(1, 1)


class SaveConfigTest(TestCase):
    def test_creation(self):
        self.assertEqual(1, 1)


class LoadConfigTest(TestCase):
    def test_creation(self):
        self.assertEqual(1, 1)


class APITest(TestCase):
    def test_creation(self):
        self.assertEqual(1, 1)
