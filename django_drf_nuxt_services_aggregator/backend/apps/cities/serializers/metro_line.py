from rest_framework import serializers

from apps.cities.models.metro_line import MetroLine


class MetroLineSerializer(serializers.ModelSerializer):

    class Meta:
        model = MetroLine
        fields = '__all__'