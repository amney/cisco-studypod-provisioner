__author__ = 'tim'
from datetime import datetime, timedelta
import logging

from models import Booking, ConfigSet, Config
from cisco_middleware.config import configure_device_group, get_config


logger = logging.getLogger(__name__)


def configure_pods():
    logger.debug("Checking if any pods need configuring at: " + str(datetime.now()))

    #Get all bookings, that start now +- 1 minute
    #TODO: Sort out the correct time deltas
    past = datetime.now() - timedelta(hours=1)
    future = datetime.now() + timedelta(hours=1)
    bookings = Booking.objects.filter(date=datetime.today(),
                                      start_time__range=(past, future))

    for booking in bookings:
        logger.info("I am going to configure " + booking.pod.__unicode__() +
                    " for user: " + booking.user)
        configure_device_group(booking.config_set)


def save_configurations():
    logger.debug("Checking if any pods need saving at: " + str(datetime.now()))

    #Get all bookings, that finish now +- 1 minute
    #TODO: Sort out the correct time deltas
    past = datetime.now() - timedelta(hours=1)
    future = datetime.now() + timedelta(hours=1)
    bookings = Booking.objects.filter(date=datetime.today(),
                                      end_time__range=(past, future))

    for booking in bookings:
        logger.info("I am going to save " + booking.pod.__unicode__() +
                    " for user: " + booking.user)
        pod = booking.pod
        config_set = ConfigSet.objects.create(user=booking.user,
                                              study_type=booking.config_set.study_type,
                                              description='Autosaved Config at ' + str(datetime.now()),
                                              pod=pod)
        for dev in pod.device_set.all():
            Config.objects.create(configuration=get_config(dev.telnet.ipv4),
                                  device=dev,
                                  config_set=config_set)
