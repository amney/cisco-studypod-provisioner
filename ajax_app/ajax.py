__author__ = 'tim'
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from cisco_middleware import config as snmp_config
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
    result = snmp_config.get_config(ip)
    dajax.assign('#result', 'innerHTML',result)
    dajax.script('stopLoading();')
    return dajax.json()

@dajaxice_register
def set_config(request, ip, config):
    dajax = Dajax()
    result = snmp_config.set_config(ip, config)
    dajax.alert("Config set!")
    dajax.script('stopLoading();')
    return dajax.json()

@dajaxice_register
def set_config_deffered(request, ip, config):
    dajax = Dajax()
    sched = Scheduler()
    sched.start()
    job = sched.add_date_job(snmp_config.set_config, datetime.now() + timedelta(seconds=5),[ip,config])
    dajax.alert("Config set deferred for 5 seconds")
    dajax.script('stopLoading();')
    return dajax.json()

