from datetime import datetime, time
from django.db import models
# Create your models here.

class DeviceType(models.Model):
    ROUTER = 'RT'
    SWITCH = 'SW'
    SERVER = 'SRV'

    DEVICE_TYPE_CHOICES = (
        (ROUTER, 'Router'),
        (SWITCH, 'Switch'),
        (SERVER, 'Server'),
        )

    type = models.CharField(max_length=3, null=False, blank=False, choices=DEVICE_TYPE_CHOICES, default=ROUTER)
    model = models.CharField(max_length=25,null=False, blank=False, default=0, )
    ram = models.IntegerField(null=True, blank=True, )

    class Meta:
        verbose_name = 'Device Type'
        verbose_name_plural = 'Device Types'
        unique_together = ("type","model","ram")

    def __unicode__(self):
        return self.model.__str__()

class Connection(models.Model):
    ipv4 = models.IPAddressField()
    port = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ("ipv4", "port")

    def __unicode__(self):
        return self.ipv4.__str__() + ":" + self.port.__str__()


class Location(models.Model):
    row = models.CharField(max_length=1,null=False)
    rack = models.IntegerField(max_length=2,null=False)

    class Meta:
        unique_together = ("row", "rack")

    def __unicode__(self):
        return self.row + self.rack.__str__()


class StudyType(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField()

    def __unicode__(self):
        return self.name

class Pod(models.Model):
    description = models.CharField(max_length=128, null=True)
    study_types = models.ManyToManyField(StudyType)

    def __unicode__(self):
        return self.description


class Device(models.Model):
    serial_number   = models.CharField(max_length=128, null=False, default="", blank=True)
    telnet          = models.ForeignKey(Connection, related_name="device_telnet", null=True, blank=True, unique=True)
    ssh             = models.ForeignKey(Connection, related_name="device_ssh", null=True, blank=True, unique=True)
    serial          = models.ForeignKey(Connection, related_name="device_serial", null=True, blank=True, unique=True)
    date_created    = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    location        = models.ForeignKey(Location,null=False)
    devicetype      = models.ForeignKey(DeviceType, blank=True, null=True )
    pod             = models.ForeignKey(Pod, blank=True, null=True)

    def __unicode__(self):
        return self.devicetype.model.__str__() + " at " + self.location.__unicode__()

    class Meta:
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'


class ConfigSet(models.Model):
    blank = models.BooleanField(null=False, default=False)
    study_type = models.ForeignKey(StudyType)
    user = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=100)
    pod = models.ForeignKey(Pod, null=False)
    create_datetime = models.DateTimeField(auto_now_add=True)
    modify_datetime = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.description


class Config(models.Model):
    configuration = models.TextField()
    device = models.ForeignKey(Device)
    config_set = models.ForeignKey(ConfigSet)
    create_datetime = models.DateTimeField(auto_now_add=True)
    modify_datetime = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Config for: " + self.device.__unicode__() + " in Config set " + self.config_set.__unicode__()


class Booking(models.Model):
    TIME_CHOICES = (
        (time(1, 00), '01:00'),
        (time(2, 00), '02:00'),
        (time(3, 00), '03:00'),
        (time(4, 00), '04:00'),
        (time(5, 00), '05:00'),
        (time(6, 00), '06:00'),
        (time(7, 00), '07:00'),
        (time(8, 00), '08:00'),
        (time(9, 00), '09:00'),
        (time(10, 00), '10:00'),
        (time(11, 00), '11:00'),
        (time(12, 00), '12:00'),
        (time(13, 00), '13:00'),
        (time(14, 00), '14:00'),
        (time(15, 00), '15:00'),
        (time(16, 00), '16:00'),
        (time(17, 00), '17:00'),
        (time(18, 00), '18:00'),
        (time(19, 00), '19:00'),
        (time(20, 00), '20:00'),
        (time(21, 00), '21:00'),
        (time(22, 00), '22:00'),
        (time(23, 00), '23:00'),
        (time(00, 00), '00:00'),
    )

    user        = models.CharField(null=False,blank=False, max_length=50)
    pod         = models.ForeignKey(Pod, null=False, blank=False)
    date        = models.DateField(null=False,blank=False, default=datetime.today())
    start_time  = models.TimeField(null=False, blank=False, choices=TIME_CHOICES, default=time(00,00))
    end_time    = models.TimeField(null=False, blank=False, choices=TIME_CHOICES, default=time(00, 00))
    config_set  = models.ForeignKey(ConfigSet, null=False, blank=False)

    def __unicode__(self):
        return self.user + " on pod " + self.pod.description + " between " + self.start_time.__str__() + " and " + self.end_time.__str__() + " on " + self.date.__str__()

    class Meta:
        unique_together = ("pod","date","start_time","end_time")

