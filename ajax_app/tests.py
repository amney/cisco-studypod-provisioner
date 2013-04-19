from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class BookTest(TestCase):
    """Test the bookings subsystem"""
    def test_creation(self):
        self.assertEqual(1, 1)

    def test_overlap(self):
        """Try and create an overlapping booking"""
        pass

    def test_slot_available(self):
        """Create 2 bookings, check 3rd pod is still offered"""


class SaveConfigTest(TestCase):

    def test_creation(self):
        """Create a config save, test it is valid"""
        self.assertEqual(1, 1)


class LoadConfigTest(TestCase):

    def test_creation(self):
        """Load a config, check it is successfull"""
        self.assertEqual(1, 1)


class SNMPTest(TestCase):

    def test_get(self):
        """Test a low level GET response"""

    def test_set(self):
        """Test a low level SET response"""

    def test_set_config(self):
        """Test a low level config SET"""

    def test_get_config(self):
        """Test a low level config GET"""


class APITest(TestCase):

    def test_creation(self):
        """Make a booking through API. Check it exists"""
        self.assertEqual(1, 1)

