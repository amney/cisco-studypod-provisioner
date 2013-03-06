__author__ = 'tigarner'

from tastypie.resources import ModelResource, ALL
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

    def dehydrate(self, bundle):
        bundle.data['length'] = bundle.obj.get_length_delta_hours()
        bundle.data['config'] = bundle.obj.config_set
        bundle.data['study_type'] = bundle.obj.config_set.study_type
        return bundle

    class Meta:
        queryset = Booking.objects.all().order_by('start_datetime')
        collection_name = 'bookings'
        filtering = {
            'user': ALL,
                    }

