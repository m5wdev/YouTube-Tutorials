from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from apps.users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    # groups = forms.ModelChoiceField(queryset=Group.objects.all())
    groups = forms.ModelChoiceField(queryset=Group.objects.exclude(name='Администратор'))

    class Meta:
        model = CustomUser
        # fields = "__all__"
        fields = ('username', 'fio', 'gender', 'birth_date', 'groups')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        # fields = "__all__"
        fields = ('username', 'fio', 'gender', 'birth_date', 'groups')
