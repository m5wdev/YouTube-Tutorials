from django import forms

from apps.actions.models import Actions
from apps.services.models import Services
from apps.salon.models.salon import Salon
from apps.salon.models.salon_services import SalonServices


class AddActionsForm(forms.ModelForm):
    # active = forms.BooleanField(initial=True, disabled=True)
    salon    = forms.ModelChoiceField(disabled=True, queryset=Salon.objects.all())
    services = forms.ModelChoiceField(queryset=Services.objects.all())

    def __init__(self, *args, **kwargs):
        # Select current Salon
        self.salon = kwargs.pop('salon')
        super(AddActionsForm, self).__init__(*args, **kwargs)
        self.fields['salon'].initial = self.salon

        salon_services_ids = SalonServices.objects.filter(salon=self.salon).values_list('service__id', flat=True)
        # Avoid to add None value to list
        salon_services_ids_list = list(filter(None, salon_services_ids))
        self.fields['services'].queryset = Services.objects.filter(id__in=salon_services_ids_list)

    class Meta:
        model = Actions
        fields = "__all__"
        # exclude = ["active"]