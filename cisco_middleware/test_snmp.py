__author__ = 'tim'
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

def get_config(device_ip):
    return 'Got config for ' + str(device_ip)

def set_config(device_ip, config):
    logger.info('Config set for device: ' + str(device_ip))
    return True

def get_snmp(oid, device):
    return 'Got SNMP'

def set_snmp(oid, value, device, address=False):
    return 'Set SNMP'