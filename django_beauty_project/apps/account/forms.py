from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from apps.account.models import Account
from apps.salon.models.salon import Salon

from datetime import datetime


class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=100, help_text='Required. Add a valid username')
    email    = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')
    phone    = forms.CharField(max_length=100, help_text='Required. Add a valid phone number')

    class Meta:
        model = Account
        fields = ("username", "email", "phone", "password1", "password2")


class RegistrationByPhoneForm(forms.Form):
    first_name  = forms.CharField(label='Your name', max_length=100)
    phone       = forms.CharField(label='Phone', max_length=100)
    agree_terms = forms.BooleanField(initial=False)

    def clean(self):
        cleaned_data = super().clean()

        first_name  = cleaned_data.get('first_name')
        phone       = cleaned_data.get('phone')
        agree_terms = cleaned_data.get('agree_terms')

        try:
            account = Account.objects.get(phone=phone)
            self.add_error('phone', 'Пользователь с данным номером телефона уже зарегистрирован')
        except Account.DoesNotExist:
            pass

        if first_name is not None and len(first_name) < 2:
            self.add_error('first_name', 'First name can\'t be less than 2 digits')

        if phone is not None and len(phone) < 5:
            self.add_error('phone', 'Phone can\'t be less than 5 digits')

        return cleaned_data


class EditAccountForm(forms.ModelForm):
    first_name = forms.CharField(disabled=True)
    phone      = forms.CharField(disabled=True)
    salon      = forms.ModelChoiceField(disabled=True, queryset=Salon.objects.all())

    birth_date = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1950, datetime.now().year - 15)),
    )

    class Meta:
        model = Account
        fields = ("first_name", "phone", "email", "city", "birth_date", "salon")


class ResetPasswordForm(forms.Form):
    phone_or_email = forms.CharField(label="Phone or Email", max_length=100, help_text='Required. Add a valid phone or email')

    def clean(self):
        cleaned_data = super().clean()

        phone_or_email = cleaned_data.get('phone_or_email')

        # if len(first_name) < 2:
        #     self.add_error('first_name', 'First name can\'t be less than 2 digits')

        # if image != '' and image_url != '':
        #     self.add_error('image', 'Заполните только одно поле!')
        #     self.add_error('image_url', 'Заполните только одно поле!')

        return cleaned_data