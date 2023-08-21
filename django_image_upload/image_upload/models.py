from django.db import models


def extended_image_upload_path(instance, filename):
    # filename = filename.lower()
    return f'extended-images/{filename}'

def modified_image_upload_path(instance, filename):
    # filename = filename.lower()
    return f'modified-images/{filename}'

class Image(models.Model):
    active         = models.BooleanField(default=False)
    extended_image = models.ImageField(upload_to=extended_image_upload_path, blank=True, null=True)
    modified_image = models.ImageField(upload_to=modified_image_upload_path, blank=True, null=True)
