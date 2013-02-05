from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import datetime
from django import forms
from ajax_app.models import  Pod
from models import Booking, StudyType
__author__ = 'tim'


class BookForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'book'
        self.helper.add_input(Submit('submit', 'Check Availability'))
        super(BookForm, self).__init__(*args, **kwargs)

    study_type  = forms.ChoiceField(choices=StudyType.objects.values_list('id', 'name'))
    date        = forms.DateField(required=True, initial=datetime.date.today())

    #Initial field is set to the nearest hour, and hour+1
    start_time  = forms.ChoiceField(choices=Booking.TIME_CHOICES, initial=datetime.time(datetime.datetime.now().hour, 00))
    end_time    = forms.ChoiceField(choices=Booking.TIME_CHOICES, initial=datetime.time((datetime.datetime.now() + datetime.timedelta(hours=1)).hour, 00))

    def clean(self):
        cleaned_data    = super(BookForm, self).clean()
        start_time      = datetime.datetime.strptime(cleaned_data.get("start_time"), "%H:%M:%S")
        end_time        = datetime.datetime.strptime(cleaned_data.get("end_time"), "%H:%M:%S")

        if start_time >= end_time:
            raise forms.ValidationError("End time must be after start time.")

        # Always return the full collection of cleaned data.
        return cleaned_data

class ConfirmForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.add_input(Submit('submit', 'Book me up Scotty!'))
        pod_id = kwargs.pop('pod_id', 0)
        username = kwargs.pop('username', 'tim')
        super(ConfirmForm, self).__init__(*args, **kwargs)
        self.fields['config_set'].choices = Pod.objects.get(pk=pod_id).configset_set.filter(user=username).values_list('id','description')

    config_set = forms.ChoiceField(label='One last thing, please choose which configuration you would like us to load onto the pod?', required=True)