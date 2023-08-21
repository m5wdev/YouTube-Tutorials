from django.contrib import admin
from apps.core.classes.singleton_model import SingletonAdminModel
from apps.core.models import SiteSettings


admin.site.register(SiteSettings, SingletonAdminModel)
