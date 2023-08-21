from datetime import datetime, time, timedelta

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode, base36_to_int
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.crypto import constant_time_compare, get_random_string
from django.utils.encoding import force_bytes

from .models import CustomUser


class ParcelTokenGenerator(PasswordResetTokenGenerator):
    def check_token(self, user, token):
        """
        Check that a parcel edit token is correct for a given parcel.
        """
        if not (user and token):
            return False, None
        try:
            ts_b36, _ = token.split("-")
            legacy_token = len(ts_b36) < 4
        except ValueError:
            return False, None

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False, None

        # Check that the timestamp/uid has not been tampered with
        if not constant_time_compare(self._make_token_with_timestamp(user, ts), token):
            if not constant_time_compare(
                    self._make_token_with_timestamp(user, ts, legacy=True),
                    token,
            ):
                return False, None

        now = self._now()
        if legacy_token:
            ts *= 24 * 60 * 60
            ts += int((now - datetime.combine(now.date(), time.min)).total_seconds())

        seconds_passed = self._num_seconds(now) - ts
        seconds_left = settings.EMAIL_EDIT_BY_CLIENT_TOKEN_TIMEOUT * 24 * 60 * 60 - seconds_passed

        if seconds_left <= 0:
            return False, None

        return True, timedelta(seconds=seconds_left)

    def _make_hash_value(self,user, timestamp):
        return f'{user.pk}{timestamp}'

edit_token = ParcelTokenGenerator()

def send_verify_link_email(email, user):

    """
    Отправка проверочной ссылки для подтверждения  email
    """

    base_url = 'http://localhost:8000'
    url_for_email =(
    f'{base_url}/users/verify-email/'
    f'{urlsafe_base64_encode(force_bytes(user.id))}/'
    f'{edit_token.make_token(user)}'
    )
    print(url_for_email)
    # html_message = render_to_string(
    #     'emails/verifity_link_email.html', {
    #         'link_email': url_for_email
    #         }
    #     )
    # message = EmailMessage('ew project', html_message, settings.EMAIL_HOST_USER, [email],)
    # message.content_subtype = 'html'
    # message.send()


def get_email_and_time_left_by_credentials(uidb64, token):
    """
    Проверка uud token из ссылки для подтверждения  email
    """
    try:
        user_id = urlsafe_base64_decode(uidb64)
        user = CustomUser.objects.get(id=user_id)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        return None, None
    is_valid, time_left = edit_token.check_token(user, token)
    if not is_valid:
        return None, None
    return user


def send_user_code_notification(email,code):
    html_message = render_to_string('emails/verifity_code_email.html', {'code': code})
    message = EmailMessage('servis-centers.ru', html_message, settings.EMAIL_HOST_USER, [email],)
    message.content_subtype = 'html'
    print(12333333333333333333333333333333333333333333333333333333333, code)
    message.send()
