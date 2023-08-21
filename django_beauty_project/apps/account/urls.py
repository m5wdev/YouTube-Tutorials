from django.urls import path, include

from apps.account.views import (
    logout_view,
    login_view,

    user_profile_view,
    change_password_view,

    reset_password_view,
    reset_password_instructions_view,

    add_salon_client_view,
    add_salon_action_view,

    salon_appointments_journal_view,
    salon_clients_view,

    client_appointments_view,

    register_by_phone_view,
    register_password_view,
)


app_name = 'user'

urlpatterns = [
    path('user/', include([
        path('login/', login_view, name='login'),
        path('logout/', logout_view, name='logout'),

        path('reset-password/', reset_password_view, name='reset-password'),
        path('reset-password-instructions/', reset_password_instructions_view, name='reset-password-instructions'),

        path('registration/', register_by_phone_view, name='registration-by-phone'),
        path('registration/password/', register_password_view, name='registration-password'),
    ])),

    path('profile/', include([
        path('', user_profile_view, name='profile'),
        path('change-password/', change_password_view, name='change-password'),

        # Salon
        path('salon/', include([
            path('add-client/', add_salon_client_view, name='salon-add-client'),
            path('add-action/', add_salon_action_view, name='salon-add-action'),

            path('appointments/', salon_appointments_journal_view, name='salon-appointments'),
            path('clients/', salon_clients_view, name='salon-clients'),
        ])),

        # Client
        path('client/', include([
            path('appontments/', client_appointments_view, name='client-appointments'),
        ])),
    ])),
]