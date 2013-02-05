__author__ = 'tim'
import socket
from time import sleep
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

tftp_server = '10.10.10.150'

def get_config(device_ip):
    #A good reference for tftp config is: http://ccie20728.wordpress.com/2008/05/20/get-the-cisco-configuration-over-snmp/

    #Set copy protocol to TFTP
    set_snmp('9.9.96.1.1.1.1.2.111', 1, device_ip)
    #Set copy source to running config
    set_snmp('9.9.96.1.1.1.1.3.111', 4, device_ip)
    #Set destination to network file
    set_snmp('9.9.96.1.1.1.1.4.111', 1, device_ip)
    #Set address of tftp server. Passing address=True lets try_snmp know it's an ip
    set_snmp('9.9.96.1.1.1.1.5.111',tftp_server, device_ip, address=True)
    #Set filename to save to - this needs to exist and be writable
    set_snmp('9.9.96.1.1.1.1.6.111', 'receive.txt', device_ip)
    #Start the transfer
    set_snmp('9.9.96.1.1.1.1.14.111', 1, device_ip)

    #While the transfer hasn't completed (Status 3) loop
    while int(get_snmp('9.9.96.1.1.1.1.10.111', device_ip)) is not 3:
        sleep(0.01)

    #Set copy status to delete, this is _must_ to clear up the whole transaction
    set_snmp('9.9.96.1.1.1.1.14.111',6, device_ip)

    #Open the downloaded config and read into a string
    linestring = open('/Users/tigarner/PycharmProjects/ajax_prj/tftp/receive.txt', 'r').read()
    return linestring

def set_config(device_ip, config):
    #A good reference for tftp config is: http://ccie20728.wordpress.com/2008/05/20/get-the-cisco-configuration-over-snmp/

    #Get the config into the text file
    open('/Users/tigarner/PycharmProjects/ajax_prj/send.txt', 'w').write(config)


    #Set copy protocol to TFTP
    set_snmp('9.9.96.1.1.1.1.2.111', 1, device_ip)
    #Set copy source to network file
    set_snmp('9.9.96.1.1.1.1.3.111', 1, device_ip)
    #Set destination to startup config
    set_snmp('9.9.96.1.1.1.1.4.111', 3, device_ip)

    #Set address of tftp server. Passing address=True lets try_snmp know it's an ip
    set_snmp('9.9.96.1.1.1.1.5.111',tftp_server, device_ip, address=True)    #Start the transfer

    #Set filename to save to - this needs to exist and be writable
    set_snmp('9.9.96.1.1.1.1.6.111', 'send.txt', device_ip)


    #Start the transfer
    set_snmp('9.9.96.1.1.1.1.14.111', 1, device_ip)

    #While the transfer hasn't completed (Status 3) loop
    #while result = int(get_snmp('9.9.96.1.1.1.1.10.111', device_ip)) and result is not 3:
      #  sleep(0.01)
    while True:
        result = int(get_snmp('9.9.96.1.1.1.1.10.111', device_ip))
        if result is 3: break
        if result is 4:
            return False;

    #Set copy status to delete, this is _must_ to clear up the whole transaction
    set_snmp('9.9.96.1.1.1.1.14.111',6, device_ip)

    #Reload the box to apply new config
    set_snmp('9.2.9.9.0',2, device_ip)


    #return the result
    return True

def get_snmp(oid, device):
    cmdGen = cmdgen.CommandGenerator()

    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData('community'),
        cmdgen.UdpTransportTarget((device, 161)),
        (cmdgen.MibVariable('SNMPv2-SMI', 'enterprises', oid)),
    )

    # Check for errors and print out results
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print(errorStatus)
    else:
        for name, val in varBinds:
            print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
            return val.prettyPrint()

def set_snmp(oid, value, device, address=False):
    if isinstance(value, int):
        value = rfc1902.Integer(value)
    elif isinstance(value, str) and address is False:
        value = rfc1902.OctetString(value)
    elif isinstance(value, str) and address is True:
        value = rfc1902.IpAddress(value)
    else:
        return "Value type not correct"

    cmdGen = cmdgen.CommandGenerator()

    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd(
        cmdgen.CommunityData('community'),
        cmdgen.UdpTransportTarget((device, 161)),
        (cmdgen.MibVariable('SNMPv2-SMI', 'enterprises', oid), value),
    )

    # Check for errors and print out results
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print(errorStatus)
    else:
        for name, val in varBinds:
            print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
            return val
















