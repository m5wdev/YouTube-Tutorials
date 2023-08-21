from rest_framework import serializers

from apps.cities.models.subdomain import Subdomain

class SubdomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subdomain
        fields = ('id','name')