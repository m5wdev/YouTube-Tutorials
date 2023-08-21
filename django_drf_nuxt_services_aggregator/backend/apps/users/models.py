import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
# from django.utils.translation import gettext_lazy as _

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

from .managers import CustomUserManager


def avatar_path(instance, filename):
    name, ext = os.path.splitext(filename.lower())
    new_name = f'avatar{ext}'
    if instance.id:
        return f'users/{instance.id}/{new_name}'

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username   = models.CharField('Username', unique=True, blank=True, max_length=255)
    email      = models.EmailField('Username\\Email', unique=True, blank=True, null=True)
    first_name = models.CharField('Имя пользователя', max_length=255, blank=True, null=True)
    avatar     = ProcessedImageField(verbose_name='Аватар пользователя',
                                        upload_to=avatar_path,
                                        processors=[ResizeToFit(256, 256)],
                                        format='JPEG',
                                        options={'quality': 75},
                                        blank=True, null=True)
    email_confirmed = models.BooleanField('Email подтвержден', help_text='Email подтвержден', default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    date_joined     = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
