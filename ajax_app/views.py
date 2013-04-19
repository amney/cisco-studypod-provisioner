# Create your views here.

import datetime
import operator
import logging
import pytz

from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import HttpResponse, render_to_response, redirect
from django.template import RequestContext

from forms import BookForm, ConfirmForm, ConfigSetForm, AlternateConfigSetForm
from models import Pod, Booking, ConfigSet, Config
from cisco_middleware.config import get_config, configure_device_group

# Get an instance of a logger
logger = logging.getLogger(__name__)


def list_pods(request):
    pods = Pod.objects.all()
    return render_to_response("maintenance/list_pods.html", {'pods': pods}, context_instance=RequestContext(request))


def list_bookings(request):
    future_bookings = Booking.objects.filter(start_datetime__gte=datetime.datetime.now(tz=pytz.utc))

    past_bookings = Booking.objects.filter(start_datetime__lte=datetime.datetime.now(tz=pytz.utc)).order_by('-start_datetime')

    return render_to_response("maintenance/list_bookings.html",
                              {'future_bookings': future_bookings, 'past_bookings': past_bookings},
                              context_instance=RequestContext(request))


@login_required
def my_bookings(request):
    user = request.user
    future_bookings = Booking.objects.filter(user=user.username, start_datetime__gte=datetime.datetime.now(tz=pytz.utc))
    past_bookings = Booking.objects.filter(user=user.username, start_datetime__lte=datetime.datetime.now(tz=pytz.utc))
    return render_to_response("maintenance/list_bookings.html",
                              {'future_bookings': future_bookings, 'past_bookings': past_bookings},
                              context_instance=RequestContext(request))


@login_required
def active_booking(request):
    user = request.user
    #active_booking = Booking.objects.filter(user=user.username, start_datetime__gte=datetime.datetime.now(tz=pytz.utc),

    #                                        end_datetime__lte=datetime.datetime.now(tz=pytz.utc))[0]

    active_booking = Booking.objects.get(pk=1)

    return render_to_response("user/active_booking.html",
                              {'booking': active_booking}, context_instance=RequestContext(request))


@login_required
def book(request):
    logger.info("Showing the booking form")
    if request.method == 'POST': # If the form has been submitted...
        form = BookForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            study_type = form.cleaned_data['study_type']

            start_time = datetime.datetime.strptime(form.cleaned_data.get("start_time"), "%H:%M:%S")
            end_time = datetime.datetime.strptime(form.cleaned_data.get("end_time"), "%H:%M:%S")

            start_datetime = datetime.datetime.combine(form.cleaned_data.get('start_date'),
                                                       start_time.time())

            end_datetime = datetime.datetime.combine(form.cleaned_data.get('end_date'),
                                                     end_time.time())

            gmt = pytz.timezone('Europe/London')
            start_datetime = gmt.localize(start_datetime)
            end_datetime = gmt.localize(end_datetime)

            request.session['start_datetime'] = start_datetime
            request.session['end_datetime'] = end_datetime

            try:
                pods = Pod.objects.filter(study_types__id__exact=study_type).exclude(
                    booking__start_datetime__gt=start_datetime,
                    booking__end_datetime__lt=end_datetime
                ).prefetch_related('configset_set')

                for pod in pods:
                    pod.my_configs = pod.configset_set.filter(user=request.user.username)
                    pod.my_config_count = pod.my_configs.count()

                pods = sorted(pods, key=operator.attrgetter('my_config_count'), reverse=True)

                return render_to_response("book/pod_available.html", {'pods': pods},
                                          context_instance=RequestContext(request))

            except Pod.DoesNotExist:
                return HttpResponse("Ouch, no pods available at that time")

    else:
        form = BookForm()

    return render_to_response("book/book.html", {'form': form}, context_instance=RequestContext(request))


@login_required
def confirm_booking(request, pod_id):
    pod = Pod.objects.get(pk=pod_id)
    request.session['pod_id'] = pod_id

    start_datetime = request.session['start_datetime']
    end_datetime = request.session['end_datetime']

    if request.method == 'POST':
        pod_id = request.session['pod_id']
        form = ConfirmForm(request.POST, pod_id=pod_id, username=request.user.username)
        if form.is_valid():
            config_set = form.cleaned_data['config_set']

            b = Booking.objects.create(user=request.user.username,
                                       pod=Pod.objects.get(pk=pod_id),
                                       start_datetime=start_datetime, end_datetime=end_datetime,
                                       config_set=ConfigSet.objects.get(pk=config_set))

            messages.add_message(request, messages.SUCCESS, 'Successfully Created Booking: {}'.format(b.__unicode__()))
            send_mail('Booking Confirmation',
                      'Hi {},\n\nI can confirm your booking: {}'.format(b.user,b.__unicode__()),
                      'timgarner0@gmail.com',
                      ['{}@example.com'.format(b.user)],
                      fail_silently=False)

            return redirect('ajax_app.views.my_bookings')
        else:
            config_set_form = ConfirmForm(request.POST, pod_id=pod_id, username=request.user.username)
    else:
        config_set_form = ConfirmForm(pod_id=pod_id, username=request.user.username)

    return render_to_response("book/confirm_booking.html",
                              {'pod': pod, 'config_set_form': config_set_form, 't1': start_datetime, 't2': end_datetime},
                              context_instance=RequestContext(request))


@login_required
def collect_config_set(request, pod_id):
    c = ConfigSet(blank=False, user='Tim', pod=Pod.objects.get(pk=pod_id))

    if request.method == 'POST':
        form = ConfigSetForm(request.POST, instance=c)
        if form.is_valid():
            pod = Pod.objects.get(pk=pod_id)
            config_set = form.save()
            for dev in pod.device_set.all():
                Config.objects.create(configuration=get_config(dev.telnet.ipv4), device=dev,
                                      config_set=config_set)

            messages.success(request, 'Config Set Saved!')
            return redirect(reverse('home-view'))
    else:
        form = ConfigSetForm(instance=c)

    return render_to_response("config/collect_config_set.html", {'form': form}, context_instance=RequestContext(request))


@login_required
def alternate_config_set(request, pod_id):
    pod = Pod.objects.get(pk=pod_id)
    request.session['pod_id'] = pod_id

    if request.method == 'POST':
        pod_id = request.session['pod_id']
        form = AlternateConfigSetForm(request.POST, pod_id=pod_id, username=request.user.username)
        if form.is_valid():
            config_set = form.cleaned_data['config_set']

            configure_device_group(ConfigSet.objects.get(pk=config_set))
            messages.add_message(request, messages.SUCCESS, 'Successfully reconfigured Pod')
            return redirect('ajax_app.views.active_booking')
        else:
            config_set_form = AlternateConfigSetForm(request.POST, pod_id=pod_id, username=request.user.username)
    else:
        config_set_form = AlternateConfigSetForm(pod_id=pod_id, username=request.user.username)

    return render_to_response("config/alternate_config_set.html",
                              {'pod': pod, 'config_set_form': config_set_form},
                              context_instance=RequestContext(request))