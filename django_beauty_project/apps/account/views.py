import random

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test

from django.forms.models import modelformset_factory, inlineformset_factory

# Models
from django.contrib.auth.models import Group

from apps.salon.models.salon import Salon
from apps.salon.models.salon_services import SalonServices
from apps.salon.models.client import Client
from apps.salon.models.client_appointment import ClientAppointment
from apps.account.models import Account

# Forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from apps.account.forms import (
    RegistrationForm,
    RegistrationByPhoneForm,
    EditAccountForm,
    ResetPasswordForm,
)
from apps.actions.forms import AddActionsForm
from apps.salon.forms import (
    AddClientForm,
    EditSalonForm,
    ClientAppointmentForm,

    AddSalonServicesForm,
    EditSalonServicesForm,
)


@user_passes_test(lambda user: user.is_anonymous)
def login_view(request):
    context = {}
    context['page_title'] = 'Вход'
    if request.POST:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('user:profile')
        else:
            context['form'] = form
    else: #GET request
        form = AuthenticationForm()
        context['form'] = form
    return render(request, 'account/login.html', context)


@login_required(login_url='user:login')
def logout_view(request):
    logout(request)
    return redirect('homepage')


@login_required(login_url='user:login')
def user_profile_view(request):
    context = {}
    context['page_title'] = 'Личный кабинет'

    # Clean session
    if request.session.get('first_name'):
        del request.session['first_name']
        request.session.modified = True
    if request.session.get('phone'):
        del request.session['phone']
        request.session.modified = True
    if request.session.get('password'):
        del request.session['password']
        request.session.modified = True
    if request.session.get('first_view'):
        del request.session['first_view']
        request.session.modified = True

    if request.POST:
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user:profile')
        else:
            context['form'] = form
    else: #GET request
        form = EditAccountForm(instance=request.user)
        context['form'] = form

    # Salon Group
    if request.user.groups.filter(name='Salon').exists():
        # context['page_title'] = f'Салон красоты "{request.user.salon.name}"'
        context['salon_services'] = SalonServices.objects.filter(salon=request.user.salon).reverse()

        salon_instance = Salon.objects.get(id=request.user.salon.id)

        # EditSalonServicesForm
        EditSalonServicesFormFormSet = inlineformset_factory(Salon, SalonServices, form=EditSalonServicesForm, fields=('salon', 'service', 'price'), extra=0, can_delete=False)
        if request.POST and 'edit_prices' in request.POST:
            formset = EditSalonServicesFormFormSet(request.POST, instance=salon_instance)
            if formset.is_valid():
                formset.save()
                return redirect('user:profile')
            else:
                context['form_edit_salon_services'] = formset
        else:
            formset = EditSalonServicesFormFormSet(instance=salon_instance)
            context['form_edit_salon_services'] = formset

        # EditSalonForm
        if request.POST:
            form_edit_salon = EditSalonForm(request.POST, instance=salon_instance)
            if form_edit_salon.is_valid():
                form_edit_salon.save()
                return redirect('user:profile')
            else:
                context['form_edit_salon'] = form_edit_salon
        else: #GET request
            form_edit_salon = EditSalonForm(instance=salon_instance)
            context['form_edit_salon'] = form_edit_salon

        # AddSalonServicesForm
        if request.POST:
            form_add_salon_services = AddSalonServicesForm(request.POST, salon=request.user.salon.id)
            if form_add_salon_services.is_valid():
                form_add_salon_services.save()
                return redirect('user:profile')
            else:
                context['form_add_salon_services'] = form_add_salon_services
        else: #GET request
            form_add_salon_services = AddSalonServicesForm(salon=request.user.salon.id)
            context['form_add_salon_services'] = form_add_salon_services


    # Manager Group
    # if request.user.groups.filter(name='Manager').exists():
    #     context['page_title'] = f'Личный кабинет менеджера {request.user.first_name}'


    # Client Group
    # if request.user.groups.filter(name='Manager').exists():
    #     context['page_title'] = f'Личный кабинет клиента {request.user.first_name}'

    return render(request, 'account/profile.html', context)


@login_required(login_url='user:login')
def change_password_view(request):
    context = {}
    context['page_title'] = 'Смена пароля'
    if request.POST:
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('user:profile')
        else:
            context['form'] = form
    else: #GET request
        form = PasswordChangeForm(user=request.user)
        context['form'] = form
    return render(request, 'account/profile-change-password.html', context)


@login_required(login_url='user:login')
@user_passes_test(lambda user: user.groups.filter(name='Salon').exists() or user.is_superuser)
def add_salon_client_view(request):
    context = {}
    context['page_title'] = 'Добавить Клиента Салона'
    if request.POST:
        form = AddClientForm(request.POST, salon=request.user.salon)
        if form.is_valid():
            form.save()
            return redirect('user:profile')
        else:
            context['form'] = form
    else: #GET request
        form = AddClientForm(salon=request.user.salon)
        context['form'] = form
    return render(request, 'account/profile/salon/profile-salon-add-client.html', context)


@login_required(login_url='user:login')
@user_passes_test(lambda user: user.groups.filter(name='Salon').exists() or user.is_superuser)
def add_salon_action_view(request):
    context = {}
    context['page_title'] = 'Добавить Салон'
    if request.POST:
        form = AddActionsForm(request.POST, salon=request.user.salon.id)
        if form.is_valid():
            form.save()
            return redirect('user:profile')
        else:
            context['form'] = form
    else: #GET request
        form = AddActionsForm(salon=request.user.salon.id)
        context['form'] = form
    return render(request, 'account/profile/salon/profile-salon-add-action.html', context)


@login_required(login_url='user:login')
@user_passes_test(lambda user: user.groups.filter(name='Salon').exists() or user.is_superuser)
def salon_appointments_journal_view(request):
    context = {}
    context['page_title'] = f'Журнал записи Салона {request.user.salon.name}'
    context['client_appontents'] = ClientAppointment.objects.filter(employee__salon=request.user.salon)
    return render(request, 'account/profile/salon/profile-salon-appointments.html', context)


@login_required(login_url='user:login')
@user_passes_test(lambda user: user.groups.filter(name='Client').exists() or user.is_superuser)
def client_appointments_view(request):
    context = {}
    # context['page_title'] = 'Клиенты'
    context['appointments'] = ClientAppointment.objects.filter(client=request.user)

    # ClientAppointmentForm
    if request.POST:
        form = ClientAppointmentForm(request.POST, client=request.user)
        if form.is_valid():
            form.save()
            return redirect('user:client-appointments')
        else:
            context['form'] = form
    else: #GET request
        form = ClientAppointmentForm(client=request.user)
        context['form'] = form

    return render(request, 'account/profile-client-appointments.html', context)


@user_passes_test(lambda user: user.is_anonymous)
def register_by_phone_view(request):
    context = {}
    context['page_title'] = 'Регистрация'

    if request.POST:
        form = RegistrationByPhoneForm(request.POST)
        if form.is_valid():
            first_name  = form.cleaned_data['first_name']
            phone       = form.cleaned_data['phone']
            agree_terms = form.cleaned_data['agree_terms']

            # Generate password and write it to session
            request.session['first_name'] = first_name
            request.session['phone'] = phone
            request.session['password'] = str(random.randint(0000, 9999))
            request.session['first_view'] = True
            request.session.modified = True

            return redirect('user:registration-password')
        else:
            context['form'] = form
    else: #GET request
        form = RegistrationByPhoneForm()
        context['form'] = form

    return render(request, 'account/register-by-phone.html', context)


def register_password_view(request):
    context = {}
    context['page_title'] = 'Ваш Пароль'

    first_name = request.session.get('first_name')
    phone      = request.session.get('phone')
    password   = request.session.get('password')
    first_view = request.session.get('first_view')

    if first_view:
        user = Account(username=phone, \
                        # email='noemail@gmail.com', \
                        first_name=first_name,
                        phone=phone, \
                        # password=password
                    )
        user.set_password(password)
        user.save()
    else:
        try:
            del request.session['first_view']
            request.session.modified = True
        except Exception as e:
            pass

    # Set user Group
    group = Group.objects.get(name='Client')
    group.user_set.add(user)

    login(request, user, backend='apps.account.auth_backends.PhoneAuthBackend')
    return render(request, 'account/register-password.html', context)


# TODO: reset password
def reset_password_view(request):
    context = {}
    context['page_title'] = 'Восстановление пароля'

    if request.POST:
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            # form.save()
            phone_or_email = form.cleaned_data['phone_or_email']
            return redirect('user:reset-password-instructions')
        else:
            context['form'] = form
    else: #GET request
        form = ResetPasswordForm()
        context['form'] = form
    return render(request, 'account/reset-password.html', context)


# TODO: reset password instructions manipulate with session
def reset_password_instructions_view(request):
    context = {}
    context['page_title'] = 'Сброс пароля'
    return render(request, 'account/reset-password-instructions.html', context)


@login_required(login_url='user:login')
@user_passes_test(lambda user: user.groups.filter(name='Salon').exists() or user.is_superuser)
def salon_clients_view(request):
    context = {}
    context['page_title'] = 'Клиенты Салона'
    context['salon_clients'] = Client.objects.filter(active=True, salon=request.user.salon.id)
    return render(request, 'account/profile/salon/profile-salon-clients.html', context)