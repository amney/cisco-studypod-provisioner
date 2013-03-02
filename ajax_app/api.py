__author__ = 'tigarner'

from tastypie.resources import ModelResource
from tastypie import fields
from ajax_app.models import Booking, Pod, ConfigSet, Device, DeviceType, Connection


class DeviceTypeResource(ModelResource):
    class Meta:
        queryset = DeviceType.objects.all()
        collection_name = 'devicetypes'


class ConnectionResource(ModelResource):
    class Meta:
        queryset = Connection.objects.all()
        collection_name = 'connections'

class DeviceResource(ModelResource):
    devicetype = fields.ForeignKey(DeviceTypeResource, 'devicetype', full=True)
    telnet = fields.ForeignKey(ConnectionResource, 'telnet', full=True)

    class Meta:
        queryset = Device.objects.all()
        collection_name = 'devices'


class PodResource(ModelResource):
    devices = fields.ToManyField(DeviceResource,'device_set', full=True)

    class Meta:
        queryset = Pod.objects.all()
        collection_name = 'pods'


class BookingResource(ModelResource):
    pod = fields.ForeignKey(PodResource, 'pod', full=True)

    class Meta:
        queryset = Booking.objects.all()
        collection_name = 'bookings'

