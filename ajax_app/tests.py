from django.db import IntegrityError
from django.test import TestCase
import pytz
from ajax_app.models import *
from datetime import datetime
from cisco_middleware import config, test_snmp
config.snmp_backend = test_snmp
import slumber


class BookTest(TestCase):
    """Test the bookings subsystem"""
    #fixtures = ['fixtures.json']

    def setUp(self):
        self.pod = Pod.objects.get(pk=1)
        self.config_set = self.pod.configset_set.get(pk=1)

        # Create a booking to use in later tests
        Booking.objects.create(user='tim', pod=self.pod,
                               start_datetime=datetime(2013, 04, 22, 10, 0, 0, 0, pytz.utc),
                               end_datetime=datetime(2013, 04, 22, 11, 0, 0, 0, pytz.utc),
                               config_set=self.config_set,
                               )

    def test_creation(self):
        b = Booking.objects.create(user='tim', pod=self.pod,
                                   start_datetime=datetime(2013, 04, 22, 21, 0, 0, 0, pytz.utc),
                                   end_datetime=datetime(2013, 04, 22, 22, 0, 0, 0, pytz.utc),
                                   config_set=self.config_set,
                                   )
        self.assertIsNotNone(b)

    def test_overlap(self):
        """Try and create an overlapping booking, ensure that it raises an integrity error"""
        self.assertRaises(IntegrityError, Booking.objects.create, user='tim', pod=self.pod,
                          start_datetime=datetime(2013, 04, 22, 10, 0, 0, 0, pytz.utc),
                          end_datetime=datetime(2013, 04, 22, 11, 0, 0, 0, pytz.utc),
                          config_set=self.config_set)



class SNMPTest(TestCase):

    def test_get(self):
        """Test a low level GET response"""
        result = test_snmp.get_config('192.168.1.1')
        self.assertEqual(result, 'Got config for 192.168.1.1')

    def test_set(self):
        """Test a low level SET"""
        result = test_snmp.set_config('192.168.1.1', 'test')
        self.assertEqual(result, True)


class APITest(TestCase):

    def test_creation(self):
        """Make a booking through API. Check it exists"""
        # api = slumber.API("http://127.0.0.1:8000/api/v1/")
        # booking = api.booking.post({
        #     "start_datetime": "2013-04-20T10:00:00",
        #     "end_datetime": "2013-04-20T11:00:00",
        #     "pod": "/api/v1/pod/1/",
        #     "config_set": "/api/v1/configset/13/",
        #     "study_type": "CCNA",
        #     "user": "tim"
        # })



