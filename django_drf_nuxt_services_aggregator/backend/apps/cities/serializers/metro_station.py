from rest_framework import serializers

from apps.cities.models.metro_station import MetroStation
from apps.cities.serializers.metro_station import MetroStation

class MetroStationSerializer(serializers.ModelSerializer):
    # metro_line = serializers.CharField(source="get_metro_line_name",read_only=True)
    metro_line_pk = MetroStation()
    city = serializers.CharField(source="get_city_name", read_only=True)

    class Meta:
        model = MetroStation
        fields = '__all__'
