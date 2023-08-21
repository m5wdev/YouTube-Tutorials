from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings


def callback_form(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        msg_body = f'Имя: {name}\nТелефон: {phone}\nСообщение: {message}'

        send_mail('Заявка на обратный звонок [monolit.site]', msg_body, settings.EMAIL_HOST_USER, ['jqphp@yandex.ru', 'mostovaya@monolit.net'])

        return redirect(request.POST.get("url_from"))


def mortgage_form(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        msg_body = f'Имя: {name}\nТелефон: {phone}\nСообщение: {message}'

        send_mail('Заявка на ипотеку [monolit.site]', msg_body, settings.EMAIL_HOST_USER, ['jqphp@yandex.ru', 'mostovaya@monolit.net'])

        return redirect(request.POST.get("url_from"))


def book_site_form(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        url_from = request.POST.get("url_from")

        msg_body = f'Имя: {name}\nТелефон: {phone}\nСообщение: {message}\nURL квартиры: {url_from}'

        send_mail('Заявка на бронирование квартиры [monolit.site]', msg_body, settings.EMAIL_HOST_USER, ['jqphp@yandex.ru', 'mostovaya@monolit.net'])

        return redirect(request.POST.get("url_from"))
