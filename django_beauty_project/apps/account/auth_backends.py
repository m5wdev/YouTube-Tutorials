from django.contrib.auth.models import User

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from django.contrib.auth.backends import ModelBackend


User = get_user_model()


class PhoneAuthBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(phone=username)
            if user.check_password(password):
                return user
            else:
                return None
        except User.DoesNotExist:
            raise ValidationError("Invalid credentials")

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None



# class EmailAuthBackend:
#     def authenticate(self, request, username=None, password=None):
#         try:
#             user = User.objects.get(email=username)
#             if user.check_password(password):
#                 return user
#             else:
#                 return None
#         except User.DoesNotExist:
#             raise ValidationError("Invalid credentials")

#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None