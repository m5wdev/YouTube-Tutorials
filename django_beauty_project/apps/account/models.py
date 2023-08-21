from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from apps.salon.models.salon import Salon


class AccountManager(BaseUserManager):
    # def create_user(self, username, email, phone, password=None):
    def create_user(self, username, phone, password=None):
        if not username:
            raise ValueError('Users must have a username')
        # if not email:
        #     raise ValueError('Users must have an email address')
        if not phone:
            raise ValueError('Users must have a phone number')
        user = self.model(
            # email=self.normalize_email(email),
            username=username,
            phone=phone,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_superuser(self, username, email, phone, password=None):
    def create_superuser(self, username, phone, password=None):
        user = self.create_user(
            username=username,
            # email=self.normalize_email(email),
            phone=phone,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    phone        = models.CharField('Phone', max_length=100, unique=True)
    # email        = models.EmailField('Email', max_length=60, unique=True)
    email        = models.EmailField('Email', max_length=60, blank=True, null=True)
    first_name   = models.CharField('First Name', max_length=100, blank=True, null=True)
    city         = models.CharField('City', max_length=255, blank=True, null=True)
    birth_date   = models.DateField('Дата рождения', blank=True, null=True)
    # birth_date   = models.CharField('Дата рождения', max_length=50, blank=True, null=True)
    salon        = models.ForeignKey(Salon, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Салон')

    # Requiered
    username     = models.CharField(max_length=30, unique=True)
    date_joined  = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login   = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin     = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=True)
    is_staff     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['email', 'phone']
    REQUIRED_FIELDS = ['phone']

    objects = AccountManager()

    def __str__(self):
        return self.username

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True