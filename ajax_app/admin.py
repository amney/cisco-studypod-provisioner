__author__ = 'tim'
from ajax_app.models import Device, Connection, Pod, StudyType, Booking, DeviceType, Location, Config, ConfigSet
from django.contrib import admin

class ConnectionInlines(admin.StackedInline):
   model =  Connection

class DeviceInlines(admin.TabularInline):
    model = Device
    extra = 5

class DeviceAdmin(admin.ModelAdmin):
    #inlines = [ConnectionInlines]
    pass

class PodAdmin(admin.ModelAdmin):
    inlines = [DeviceInlines]

admin.site.register(Device, DeviceAdmin)
admin.site.register(Connection)
admin.site.register(Pod, PodAdmin)
admin.site.register(StudyType)
admin.site.register(Booking)
admin.site.register(DeviceType)
admin.site.register(Location)
admin.site.register(Config)
admin.site.register(ConfigSet)