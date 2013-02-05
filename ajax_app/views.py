# Create your views here.

from django.contrib.auth.decorators import login_required
from forms import BookForm, ConfirmForm
from django.shortcuts import HttpResponse, render_to_response
from django.template import RequestContext
from models import Pod, Booking, ConfigSet
from datetime import datetime
import operator

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

def list_pods(request):
    pods = Pod.objects.all()
    return render_to_response("list_pods.html", {'pods':pods}, context_instance=RequestContext(request))

def list_bookings(request):
    future_bookings = Booking.objects.filter(date__gte=datetime.today(),
                                             start_time__gte=datetime.now())

    past_bookings = Booking.objects.filter(date__lte=datetime.today(),
                                       start_time__lte=datetime.now()).order_by('-date','-start_time')
    return  render_to_response("list_bookings.html", {'future_bookings': future_bookings, 'past_bookings': past_bookings},
                           context_instance=RequestContext(request))
@login_required
def my_bookings(request):
    user = request.user
    future_bookings = Booking.objects.filter(user=user.username, date__gte=datetime.today(),
                                             start_time__gte=datetime.now())
    past_bookings   = Booking.objects.filter(user=user.username, date__lte=datetime.today(),
                                             start_time__lte=datetime.now())
    return  render_to_response("list_bookings.html", {'future_bookings': future_bookings, 'past_bookings' : past_bookings}, context_instance=RequestContext(request))

@login_required
def book(request):
    logger.info("Showing the booking form")
    if request.method == 'POST': # If the form has been submitted...
        form = BookForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            study_type = form.cleaned_data['study_type']
            d = form.cleaned_data['date']
            t1 = form.cleaned_data['start_time']
            t2 = form.cleaned_data['end_time']
            request.session['date'] = d
            request.session['start_time'] = t1
            request.session['end_time'] = t2

            try:
                pods = Pod.objects.filter(
                    study_types__id__exact=study_type).exclude(
                    booking__date=d,
                    booking__start_time__lt=t2,
                    booking__end_time__gt=t1, )

                for pod in pods:
                    pod.my_configs = pod.configset_set.filter(user=request.user.username)
                    pod.my_config_count = pod.my_configs.count()

                pods = sorted(pods, key=operator.attrgetter('my_config_count'), reverse=True)

                return render_to_response("pod_available.html", {'pods': pods},
                                          context_instance=RequestContext(request))

            except Pod.DoesNotExist:
                return HttpResponse("Ouch, no pods available at that time")


    else:
        form = BookForm()

    return render_to_response("book.html", {'form': form}, context_instance=RequestContext(request))

@login_required
def confirm_booking(request, pod_id):
    pod = Pod.objects.get(pk=pod_id)
    request.session['pod_id'] = pod_id
    d   = request.session['date']
    t1  = request.session['start_time']
    t2  = request.session['end_time']

    if request.method == 'POST':
        pod_id = request.session['pod_id']
        form = ConfirmForm(request.POST, pod_id=pod_id, username=request.user.username)
        if form.is_valid():
            config_set = form.cleaned_data['config_set']

            Booking.objects.create(user=request.user.username,
                                   pod=Pod.objects.get(pk=pod_id), date=d,
                                   start_time=t1, end_time=t2,
                                   config_set=ConfigSet.objects.get(pk=config_set))

            return HttpResponse("Booking successfully made! <a href=\"/\">Go Home</a>")
        else:
            config_set_form = ConfirmForm(request.POST, pod_id=pod_id, username=request.user.username)
    else:
        config_set_form = ConfirmForm(pod_id=pod_id, username=request.user.username)

    return render_to_response("confirm_booking.html", {'pod': pod, 'config_set_form': config_set_form, 'd' : d, 't1': t1, 't2':t2},
                              context_instance=RequestContext(request))
