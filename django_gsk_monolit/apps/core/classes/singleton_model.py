# Author: https://steelkiwi.com/blog/practical-application-singleton-design-pattern/
from django.db import models
from django.core.cache import cache
from django.contrib import admin

from apps.core.classes.turn_off_admin_logging import TurnOffAdminLogging


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def set_cache(self):
        cache.set(self.__class__.__name__, self)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)
        self.set_cache()

    # Restrict deletion
    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        if cache.get(cls.__name__) is None:
            obj, created = cls.objects.get_or_create(pk=1)
            if not created:
                obj.set_cache()
        return cache.get(cls.__name__)


class SingletonAdminModel(TurnOffAdminLogging, admin.ModelAdmin):
    # Disable mass actions
    actions = None

    # Remove Delete button
    def has_delete_permission(self, request, obj=None):
        return False

    # Remove "Save and add another"
    def has_add_permission(self, request):
        if self.model.objects.count() > 0:
            return False
        return super().has_add_permission(request)

    # Turn off logging History
    # def log_addition(self, *args):
    #     return
    #
    # def log_change(self, *args):
    #     return
    #
    # def log_deletion(self, *args):
    #     return
    # END Turn off logging History
