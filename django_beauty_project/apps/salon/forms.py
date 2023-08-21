from django import forms

from apps.account.models import Account

from apps.salon.models.client import Client
from apps.salon.models.client_appointment import ClientAppointment
from apps.salon.models.salon import Salon
from apps.salon.models.salon_services import SalonServices

from apps.services.models import Services


class AddClientForm(forms.ModelForm):
    # active = forms.BooleanField(initial=True, disabled=True)
    salon = forms.ModelChoiceField(disabled=True, queryset=Salon.objects.all())

    def __init__(self, *args, **kwargs):
        # Select current Salon in form
        self.salon = kwargs.pop('salon')
        super(AddClientForm, self).__init__(*args, **kwargs)
        self.fields['salon'].initial = self.salon


    class Meta:
        model = Client
        # fields = ("phone", "first_name")
        fields = "__all__"
        # exclude = ["active"]


class EditSalonForm(forms.ModelForm):
    class Meta:
        model = Salon
        fields = "__all__"
        exclude = ["active"]


class ClientAppointmentForm(forms.ModelForm):
    client   = forms.ModelChoiceField(disabled=True, queryset=Account.objects.all())
    # datetime = forms.DateTimeField(widget=forms.DateTimeInput())

    def __init__(self, *args, **kwargs):
        # Select current user in form client
        self.client = kwargs.pop('client')
        super(ClientAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['client'].initial = self.client

    class Meta:
        model = ClientAppointment
        fields = "__all__"
        exclude = ["status"]


class AddSalonServicesForm(forms.ModelForm):
    salon   = forms.ModelChoiceField(disabled=True, queryset=Salon.objects.all())
    service = forms.ModelChoiceField(required=True, queryset=SalonServices.objects.all())

    def __init__(self, *args, **kwargs):
        # Select current Salon
        self.salon = kwargs.pop('salon')
        super(AddSalonServicesForm, self).__init__(*args, **kwargs)
        self.fields['salon'].initial = self.salon

        # Get Services in queryset except selected to curret Salon
        # salon_services_ids_list = list(SalonServices.objects.filter(salon=self.salon).values_list('service__id', flat=True))

        salon_services_ids = SalonServices.objects.filter(salon=self.salon).values_list('service__id', flat=True)
        # Avoid to add None value to list
        salon_services_ids_list = list(filter(None, salon_services_ids))
        self.fields['service'].queryset = Services.objects.exclude(id__in=salon_services_ids_list)

    class Meta:
        model = SalonServices
        fields = "__all__"


class EditSalonServicesForm(forms.ModelForm):
    salon   = forms.ModelChoiceField(disabled=True, queryset=Salon.objects.all())
    service = forms.ModelChoiceField(disabled=True, queryset=Services.objects.all())
    # price   = forms.DecimalField(required=True)

    # def __init__(self, *args, **kwargs):
    #     # Select current Salon
    #     self.salon = kwargs.pop('salon')
    #     super(EditSalonServicesForm, self).__init__(*args, **kwargs)
    #     self.fields['salon'].initial = self.salon

    class Meta:
        model = SalonServices
        fields = "__all__"
        # exclude = ["salon"]