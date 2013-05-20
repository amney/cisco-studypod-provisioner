from django.core.mail import send_mail
import pytz

__author__ = 'tim'
from datetime import datetime, timedelta
import logging

from models import Booking, ConfigSet, Config
from cisco_middleware.config import configure_device_group, get_config


logger = logging.getLogger(__name__)


tz = pytz.timezone('Europe/London')

def configure_pods():
    """This is run at the start of a booking, automatically loading the correct configuration on"""
    logger.debug("Checking if any pods need configuring at: " + str(datetime.now()))

    # Get all bookings, that start now +- 1 minute
    # TODO: Sort out the correct time deltas, at the moment the delta is
    # set to +- an hour for testing purposes

    past = datetime.now(tz=tz) - timedelta(hours=1)
    future = datetime.now(tz=tz) + timedelta(hours=1)
    bookings = Booking.objects.filter(start_datetime__range=(past, future))

    for booking in bookings:
        logger.info("I am going to configure " + booking.pod.__unicode__() +
                    " for user: " + booking.user)
        configure_device_group(booking.config_set)
        send_mail('Booking Started',
                  'Hi {},\n\nYour Booking {} has now started\n\nThanks,\nThe Csco.SRL Team.'.format(booking.user, booking.__unicode__()),
                  'timgarner0@gmail.com',
                  ['{}@example.com'.format(booking.user)],
                  fail_silently=False)

def save_configurations():
    """This is run at the end of a booking, automatically saving the configuration and
    notifiying the user"""

    logger.debug("Checking if any pods need saving at: " + str(datetime.now()))

    # Get all bookings, that finish now +- 1 minute
    # TODO: Sort out the correct time deltass, at the moment the delta is
    # set to +- an hour for testing purposes

    past = datetime.now(tz=tz) - timedelta(hours=1)
    future = datetime.now(tz=tz) + timedelta(hours=1)
    bookings = Booking.objects.filter(end_datetime__range=(past, future))

    for booking in bookings:
        logger.info("I am going to save " + booking.pod.__unicode__() +
                    " for user: " + booking.user)
        pod = booking.pod
        config_set = ConfigSet.objects.create(user=booking.user,
                                              study_type=booking.config_set.study_type,
                                              description='Autosaved Config at ' + str(datetime.now(tz=tz)),
                                              pod=pod)
        for dev in pod.device_set.all():
            Config.objects.create(configuration=get_config(dev.telnet.ipv4),
                                  device=dev,
                                  config_set=config_set)

        send_mail('Booking Finished',
                  'Hi {},\n\nYour Booking {} has now finished\n\nThanks,\nThe Csco.SRL Team.'.format(booking.user, booking.__unicode__()),
                  'timgarner0@gmail.com',
                  ['{}@example.com'.format(booking.user)],
                  fail_silently=False)