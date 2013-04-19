__author__ = 'tigarner'
from datetime import datetime
import pytz
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from tastypie.authorization import Authorization
from ajax_app.models import Booking, Pod, ConfigSet, Device, DeviceType, Connection, StudyType


class DeviceTypeResource(ModelResource):
    class Meta:
        queryset = DeviceType.objects.all()
        collection_name = 'devicetypes '


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
    devices = fields.ToManyField(DeviceResource, 'device_set', full=True)

    class Meta:
        queryset = Pod.objects.all()
        collection_name = 'pods'
        filtering = {
            'study_types': ALL,
            'booking': ALL,
            'description': ALL,
        }


class ConfigSetResource(ModelResource):
    pod = fields.ForeignKey(PodResource, 'pod')

    def dehydrate(self, bundle):
        bundle.data['pod'] = bundle.obj.pod.description
        return bundle

    class Meta:
        queryset = ConfigSet.objects.all()
        collection_name = 'configsets'
        filtering = {
            'pod': ALL_WITH_RELATIONS,
            'user': ALL
        }


class BookingResource(ModelResource):
    pod = fields.ForeignKey(PodResource, 'pod', full=True)
    config_set = fields.ForeignKey(ConfigSetResource, 'config_set')

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
        authorization = Authorization()
        always_return_data = True


class AvailabilityResource(ModelResource):

    def get_object_list(self, request):
        gmt = pytz.timezone('Europe/London')

        start = gmt.localize(datetime.strptime(request.GET["start"], "%Y-%m-%d %H:%M:%S"))
        end = gmt.localize(datetime.strptime(request.GET["end"], "%Y-%m-%d %H:%M:%S"))
        study_type_id = StudyType.objects.filter(name=request.GET['study_type'])[0].pk

        pods = Pod.objects.filter(study_types__id__exact=study_type_id).exclude(
            booking__start_datetime__gte=start,
            booking__end_datetime__lte=end)
        return pods

    class Meta:
        collection_name = 'pods'
        queryset = Pod.objects.all()





