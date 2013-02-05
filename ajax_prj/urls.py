from django.conf.urls import patterns, include, url
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf import settings
from ajax_app.jobs import configure_pods
from apscheduler.scheduler import Scheduler
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

#Start the scheduler
#TODO: This is VERY hacky, fix up the scheduling
sched = Scheduler()
sched.start()
logger.info("Starting configuration scheduled job")
sched.add_interval_job(configure_pods, minutes=1)

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()
dajaxice_autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/images/favicon.ico'}),
    url(r'^$',TemplateView.as_view(template_name="home.html"), name="home-view"),
    url(r'^about/$',TemplateView.as_view(template_name="about.html"), name="about"),
    url(r'^contact/$',TemplateView.as_view(template_name="contact.html"), name="contact"),
    url(r'^config/$',TemplateView.as_view(template_name="get_config.html"), name="get-config"),
    url(r'^book/$','ajax_app.views.book', name="book"),
    url(r'^book/confirm_booking/(?P<pod_id>\d)/$', 'ajax_app.views.confirm_booking', name="confirm_booking"),
    url(r'^maintenance/list_pods/$', 'ajax_app.views.list_pods', name="list_pods"),
    url(r'^maintenance/list_bookings/$', 'ajax_app.views.list_bookings', name="list_bookings"),
    url(r'^user/my_bookings/$', 'ajax_app.views.my_bookings', name="my_bookings"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'},name="login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name="logout"),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),

)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG is False:   #if DEBUG is True it will be served automatically
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
