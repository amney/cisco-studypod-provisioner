import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from ajax_app.models import Pod
from models import Booking, StudyType, ConfigSet


__author__ = 'tim'


class BookForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'book'
        self.helper.add_input(Submit('submit', 'Check Availability'))
        super(BookForm, self).__init__(*args, **kwargs)

    study_type = forms.ChoiceField(choices=StudyType.objects.values_list('id', 'name'))
    start_date = forms.DateField(required=True, initial=datetime.date.today())

    #Initial field is set to the nearest hour, and hour+1
    start_time = forms.ChoiceField(choices=Booking.TIME_CHOICES,
                                   initial=datetime.time(datetime.datetime.now().hour, 00))

    end_date = forms.DateField(required=True, initial=datetime.date.today())

    end_time = forms.ChoiceField(choices=Booking.TIME_CHOICES,
                                 initial=datetime.time((datetime.datetime.now() + datetime.timedelta(hours=1)).hour,
                                                       00))

    def clean(self):
        cleaned_data = super(BookForm, self).clean()

        start_time = datetime.datetime.strptime(cleaned_data.get("start_time"), "%H:%M:%S")
        end_time = datetime.datetime.strptime(cleaned_data.get("end_time"), "%H:%M:%S")

        start_datetime = datetime.datetime.combine(cleaned_data.get('start_date'),
                                                   start_time.time())

        end_datetime = datetime.datetime.combine(cleaned_data.get('end_date'),
                                                 end_time.time())

        if start_datetime >= end_datetime:
            raise forms.ValidationError("End time must be after start time.")

        # Always return the full collection of cleaned data.
        return cleaned_data


class ConfirmForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.add_input(Submit('submit', 'Confirm Booking', css_class='btn-success'))
        pod_id = kwargs.pop('pod_id', 0)
        username = kwargs.pop('username', 'tim')
        super(ConfirmForm, self).__init__(*args, **kwargs)
        self.fields['config_set'].choices = Pod.objects.get(pk=pod_id).configset_set.filter(user=username).values_list(
            'id', 'description')

    config_set = forms.ChoiceField(
        label='One last thing, please choose which configuration you would like us to load onto the pod?',
        required=True)


class ConfigSetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.add_input(Submit('submit', 'Collect Config'))
        super(ConfigSetForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ConfigSet
        exclude = ('blank', 'user', 'pod')


class AlternateConfigSetForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.add_input(Submit('submit', 'Load Config'))
        pod_id = kwargs.pop('pod_id', 0)
        username = kwargs.pop('username', 'tim')
        super(AlternateConfigSetForm, self).__init__(*args, **kwargs)
        self.fields['config_set'].choices = Pod.objects.get(pk=pod_id).configset_set.filter(user=username).values_list(
            'id', 'description')

    config_set = forms.ChoiceField(
        label='Select Configuration To Load', required=True)

