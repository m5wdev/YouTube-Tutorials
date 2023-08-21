# from django.contrib.auth.models import User
from apps.users.models import CustomUser


class CreateSuperuser:
    username = 'admin'
    password = '123'
    email    = 'admin@gmail.com'

    @classmethod
    def create(cls):
        get_admin = CustomUser.objects.filter(username=cls.username).exists()
        if not get_admin:
            # create_user = User()
            create_user = CustomUser()
            create_user.username = cls.username
            create_user.email    = cls.email
            create_user.is_superuser = True
            create_user.is_staff     = True
            create_user.is_active    = True
            create_user.set_password(cls.password)
            create_user.save()
            print('User Successfully Created!', 'login: ' + create_user.username, 'password: ' + cls.password)
