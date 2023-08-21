from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from django.contrib.auth import get_user_model

MyUser = get_user_model()


class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username:
            username = kwargs.get('email')
        try:
            user = MyUser.objects.get(Q(email=username) | Q(username=username))
        except MyUser.DoesNotExist:
            MyUser().set_password(password)
        except MyUser.MultipleObjectsReturned:
            return MyUser.objects.filter(email=username).order_by('id').first()
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = MyUser.objects.get(pk=user_id)
        except MyUser.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None