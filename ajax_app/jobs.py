__author__ = 'tim'
from datetime import datetime, timedelta
from models import Booking
from cisco_middleware.config import configure_device_group
import logging
logger = logging.getLogger(__name__)

def configure_pods():
    logger.debug("Checking if any pods need configuring at: " + \
                 str(datetime.now()))

    #Get all bookings, that start now +- 1 minute
    #TODO: Sort out the correct time deltas
    past = datetime.now() - timedelta(hours=1)
    future = datetime.now() + timedelta(hours=1)
    bookings = Booking.objects.filter(date=datetime.today(),
                                      start_time__range=(past,future))

    for booking in bookings:
        logger.info("I am going to configure " + booking.pod.__unicode__() + \
              " for user: " + booking.user)
        configure_device_group(booking.config_set)
