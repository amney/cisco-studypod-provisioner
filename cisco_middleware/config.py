__author__ = 'tim'
import snmp, test_snmp
from ajax_app.models import ConfigSet, Config
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

#Set the right snmp backend
snmp_backend = test_snmp

def configure_device(config):
    logger.info("Configuring device: " + \
          str(config.device.telnet.ipv4) \
          + " " + str(config.configuration))

    snmp_backend.set_config(config.device.telnet.ipv4, config.configuration)


def configure_device_group(config_set):
    for config in config_set.config_set.all():
        configure_device(config)
