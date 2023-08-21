from django.contrib.auth.models import Group

from apps.account.models import Account
from apps.salon.models.salon import Salon

from .add_dummy_content import AddDummyContent


class AddDefaultSettings(AddDummyContent):
    def createGroups(self):
        groups = ['Manager', 'Salon', 'Client']
        for group in groups:
            try:
                gr = Group.objects.get(name=group)
                print(f"Group {gr.name} already exists")
            except Group.DoesNotExist:
                gr = Group(name=group)
                gr.save()
                print(f"Group {gr.name} created!")


    def createSuperuser(self):
        try:
            superuser = Account.objects.get(username="admin")
            print("Superuser alredy exists")
        except Exception as e:
            superuser = Account(phone="000", \
                                    username="admin", \
                                    first_name="", \
                                    city="Москва")
            superuser.set_password('123')

            # set superuser params
            superuser.is_superuser = True
            superuser.is_admin = True
            superuser.is_staff = True

            superuser.save()
            print("Superuser creted!")


    def createUserClient(self):
        try:
            user_client = Account.objects.get(username="user_client")
            print("UserClient alredy exists")
        except Exception as e:
            user_client = Account(phone="111", \
                                    username="user_client", \
                                    first_name="Клиент", \
                                    city="Москва")
            user_client.set_password('123')
            user_client.save()
            print("UserClient creted and set Group \"Client\"")
        client_group = Group.objects.get(name='Client')
        client_group.user_set.add(user_client)


    def createUserSalon(self):
        try:
            user_salon = Account.objects.get(username="user_salon")
            print("UserSalon alredy exists")
        except Exception as e:
            # TODO: wrap in try
            salon_instance = Salon.objects.get(id=1)
            user_salon = Account(phone="222", \
                                    username="user_salon", \
                                    first_name="Салон", \
                                    city="Москва", \
                                    salon=salon_instance)
            user_salon.set_password('123')
            user_salon.save()
            print("UserSalon creted and set Group \"Salon\"")
        salon_group = Group.objects.get(name='Salon')
        salon_group.user_set.add(user_salon)


    def createUserManager(self):
        try:
            user_manager = Account.objects.get(username="user_manager")
            print("UserManager alredy exists")
        except Exception as e:
            user_manager = Account(phone="333", \
                                    username="user_manager", \
                                    first_name="Менеджер", \
                                    city="Москва")
            user_manager.set_password('123')
            user_manager.save()
            print("UserManager creted and set Group \"Manager\"")
        manager_group = Group.objects.get(name='Manager')
        manager_group.user_set.add(user_manager)


    def addSettings(self):
        # in case you don't need dummy content - comment this
        self.createDummyContent()

        self.addServices()
        self.createGroups()

        self.createSuperuser()
        self.createUserClient()
        self.createUserSalon()
        self.createUserManager()

        self.addClientAppointments()