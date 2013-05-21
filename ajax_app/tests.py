from django.db import IntegrityError
from django.test import TestCase, Client
import pytz
from ajax_app.forms import BookForm, ConfirmForm
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


class FormTest(TestCase):

    fixtures = ['ajax_app/fixtures/initial_data.json']

    def test_booking_valid(self):
        data = {'study_type': 1,
                'start_date': '21/05/2013',
                'start_time': '12:00:00',
                'end_date': '21/05/2013',
                'end_time': '13:00:00'}
        form = BookForm(data=data)
        self.assertEqual(form.is_valid(), True)

    def test_booking_invalid(self):
        data = {'study_type': 1,
                'start_date': '21/05/2013',
                'start_time': '12:00:00',
                'end_date': '21/05/2013',
                'end_time': '12:00:00'}
        form = BookForm(data=data)
        self.assertEqual(form.is_valid(), False)

    def test_confirm_valid(self):
        data = {'config_set': 2}
        form = ConfirmForm(data=data, pod_id=1, username='tim')
        self.assertEqual(form.is_valid(), True)

    def test_confirm_invalid(self):
        data = {'config_set': 1}
        form = ConfirmForm(data=data, pod_id=1, username='tim')
        self.assertEqual(form.is_valid(), False)


class SNMPTest(TestCase):

    fixtures = ['ajax_app/fixtures/initial_data.json']

    def test_high_level_get(self):
        result = config.get_config('192.168.1.1')
        self.assertEqual(result, 'Got config for 192.168.1.1')

    def test_high_level_set(self):
        conf_set = ConfigSet.objects.get(pk=3)
        result = config.configure_device_group(conf_set)
        self.assertEqual(result, None)

    def test_get(self):
        """Test a low level GET response"""
        result = test_snmp.get_config('192.168.1.1')
        self.assertEqual(result, 'Got config for 192.168.1.1')

    def test_set(self):
        """Test a low level SET"""
        result = test_snmp.set_config('192.168.1.1', 'test')
        self.assertEqual(result, True)


class APITest(TestCase):

    fixtures = ['ajax_app/fixtures/initial_data.json']

    def test_get_booking(self):
        client = Client()
        response = client.get('/api/v1/booking/')
        self.assertEqual(response.status_code, 200)

    def test_get_pod(self):
        client = Client()
        response = client.get('/api/v1/pod/')
        self.assertEqual(response.status_code, 200)

    def test_get_device(self):
        client = Client()
        response = client.get('/api/v1/device/')
        self.assertEqual(response.status_code, 200)

    def test_get_availability(self):
        client = Client()
        response = client.get('/api/v1/availability/?end=2013-03-05%2013%3A00%3A00&start=2013-03-05%2012%3A00%3A00&study_type=CCNA')
        self.assertEqual(response.status_code, 200)




