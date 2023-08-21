from rest_framework import serializers
from django.utils.text import slugify
from .models import CategoryService, Service


class ServiceSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = '__all__'

    def get_slug(self, instance):
        return slugify(instance.slug)


class CategoryServicesSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = CategoryService
        fields = '__all__'


class CategoryServicesCitySerializer(serializers.ModelSerializer):
    service = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = CategoryService
        fields = ['name',]
