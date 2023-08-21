from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title    = models.CharField(max_length=255)
    slug     = models.SlugField(blank=True, null=True, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    body     = models.TextField(blank=True, null=True)
    tags     = models.ManyToManyField(Tag, blank=True)
    author   = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT)
    created  = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title


class Communities(models.Model):
    name       = models.CharField(max_length=255)
    blog_posts = models.ManyToManyField(Blog, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Community'
        verbose_name_plural = 'Communities'
