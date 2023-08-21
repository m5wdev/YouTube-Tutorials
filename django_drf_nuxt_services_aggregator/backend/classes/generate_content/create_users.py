import random
from apps.users.models import CustomUser


class CreateUsers:
    username = 'u'
    password = '123'
    email    = '@gmail.com'

    create_qty = 10
    count_in_db = CustomUser.objects.all().count()


    @classmethod
    def create_user(cls, counter):
        create_user = CustomUser()
        create_user.username        = f'{cls.username}{counter}'
        create_user.email           = f'{cls.username}{counter}{cls.email}'
        create_user.is_superuser    = False
        create_user.is_staff        = bool(random.getrandbits(1))
        create_user.is_active       = True
        create_user.email_confirmed = bool(random.getrandbits(1))
        create_user.set_password(cls.password)
        create_user.save()
        print('User Successfully Created!', 'login: ' + create_user.username, 'password: ' + cls.password)


    @classmethod
    def fill_db(cls, qty=create_qty):
        start = 0

        # if cls.count_in_db > 0:
        if cls.count_in_db == 0:
            start = cls.count_in_db
            qty += cls.count_in_db

            for i in range(start, qty):
                cls.create_user(i)
        else:
            print('Users already generated')
