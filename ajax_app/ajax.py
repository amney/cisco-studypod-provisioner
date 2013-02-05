__author__ = 'tim'
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from cisco_middleware import snmp
from datetime import datetime, timedelta
from apscheduler.scheduler import Scheduler

@dajaxice_register
def sayhello(request):
    return simplejson.dumps({'message':'This is - Hello World'})

@dajaxice_register
def multiply(request, a, b):
    dajax = Dajax()
    try:
        result = int(a) * int(b)
    except ValueError:
        result = "Invalid Parameters"

    dajax.assign('#result','value',str(result))
    return dajax.json()

@dajaxice_register
def get_config(request, ip):
    dajax = Dajax()
    result = snmp.get_config(ip)
    dajax.assign('#result', 'innerHTML',result)
    dajax.script('stopLoading();')
    return dajax.json()

@dajaxice_register
def set_config(request, ip, config):
    dajax = Dajax()
    result = snmp.set_config(ip, config)
    dajax.alert("Config set!")
    dajax.script('stopLoading();')
    return dajax.json()

@dajaxice_register
def set_config_deffered(request, ip, config):
    dajax = Dajax()
    sched = Scheduler()
    sched.start()
    job = sched.add_date_job(snmp.set_config, datetime.now() + timedelta(seconds=15),[ip,config])
    dajax.alert("Config set deffered for 15 seconds")
    dajax.script('stopLoading();')
    return dajax.json()

