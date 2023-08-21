from rest_framework import serializers

from apps.cities.models.city import City
from apps.cities.serializers.subdomain import SubdomainSerializer

class CitySerializer(serializers.ModelSerializer):
    subdomain = SubdomainSerializer()

    class Meta:
        model = City
        fields = '__all__'