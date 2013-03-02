from django.conf.urls import patterns, include, url
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf import settings
from tastypie.api import Api
from ajax_app.api import BookingResource, PodResource, DeviceResource, DeviceTypeResource, ConnectionResource
from ajax_app.jobs import configure_pods, save_configurations
from apscheduler.scheduler import Scheduler
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

v1_api = Api(api_name='v1')

v1_api.register(PodResource())
v1_api.register(BookingResource())
v1_api.register(DeviceResource())
v1_api.register(DeviceTypeResource())
v1_api.register(ConnectionResource())




#Start the scheduler
#TODO: This is VERY hacky, fix up the scheduling
#sched = Scheduler()
#sched.start()
logger.info("Starting configuration scheduled job")
#sched.add_interval_job(configure_pods, minutes=1)
#sched.add_interval_job(save_configurations, minutes=1)

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()
dajaxice_autodiscover()

urlpatterns = patterns('',
                       url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/images/favicon.ico'}),
                       url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^api/', include(v1_api.urls)),
                       )

urlpatterns += patterns('ajax_app.views',
    url(r'^$',TemplateView.as_view(template_name="home.html"), name="home-view"),
    url(r'^about/$',TemplateView.as_view(template_name="about.html"), name="about"),
    url(r'^contact/$',TemplateView.as_view(template_name="contact.html"), name="contact"),
    url(r'^config/$',TemplateView.as_view(template_name="config/get_config.html"), name="get-config"),
    url(r'^book/$','book', name="book"),
    url(r'^book/confirm_booking/(?P<pod_id>\d)/$', 'confirm_booking', name="confirm_booking"),
    url(r'^config/save/(?P<pod_id>\d)/$', 'collect_config_set', name="collect_config_set"),
    url(r'^config/load/(?P<pod_id>\d)/$', 'alternate_config_set', name="alternate_config_set"),
    url(r'^maintenance/list_pods/$', 'list_pods', name="list_pods"),
    url(r'^maintenance/list_bookings/$', 'list_bookings', name="list_bookings"),
    url(r'^user/my_bookings/$', 'my_bookings', name="my_bookings"),
    url(r'^user/active_booking/$', 'active_booking', name="active_booking"),
    )

urlpatterns += patterns('django.contrib.auth.views',
                        url(r'^accounts/login/$', 'login', {'template_name': 'admin/login.html'}, name="login"),
                        url(r'^accounts/logout/$', 'logout', name="logout"),
                        )

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG is False:   #if DEBUG is True it will be served automatically
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
