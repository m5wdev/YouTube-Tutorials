from rest_framework import serializers

from apps.company.models.point import Point, MetroStation
from apps.cities.serializers import metro_station
from apps.company.models.company import Company
from apps.cities.serializers.city import CitySerializer

class PointSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source="get_city_name",read_only=True)
    metro = metro_station.MetroStationSerializer(many=True,read_only=True)
    metro_id = serializers.IntegerField(min_value=0, max_value=1000000,write_only=True,required = False)
    city_id = serializers.IntegerField(min_value=1, max_value=1000000,write_only=True)
   

    company_id = serializers.IntegerField(min_value=1, max_value=100000,write_only=True)
    
    

    class Meta:
        model = Point
        fields = '__all__'

    def create(self, validated_data):
        metro_id = None
        print('create')
        metro_id = 0
        if validated_data.get('metro_id'):
            metro_id = validated_data.pop('metro_id')
        city_id = validated_data.pop('city_id')
        company_id = validated_data.pop('company_id')
        company = Company.objects.get(id = company_id)
        point = Point.objects.create(**validated_data,city_id=city_id)


        if metro_id != 0:
            metro = MetroStation.objects.get(id=metro_id)
            point.metro.add(metro)
        point.company.add(company)
        point.save()
        return point


    def update(self, instance, validated_data):
        print('update')
        metro_id = None
        if validated_data.get('metro_id'):
            metro_id = validated_data.pop('metro_id')
        city_id = validated_data.pop('city_id')
        company_id = validated_data.pop('company_id')
        point = Point.objects.get(id = instance.id)
        for key, value in validated_data.items():
            setattr(point, key, value)
        if metro_id:
            try:
                metro = MetroStation.objects.get(id=metro_id)
                point.metro.add(metro)
            except:
                pass
        else:
            point.metro.clear()
        if city_id:
            point.city_id = city_id
    
        point.save()
        return point

    def retvie (self, instance, validated_data):
        metro_id = None
        if validated_data.get('metro_id'):
            metro_id = validated_data.pop('metro_id')
        city_id = validated_data.pop('city_id')
        company_id = validated_data.pop('company_id')
        company = Company.objects.get(id = company_id)
        point = Point.objects.create(**validated_data,city_id=city_id)
        if metro_id:
            try:
                metro = MetroStation.objects.get(id=metro_id)
                point.metro.add(metro)
            except:
                pass
        point.company.add(company)
        point.save()
        return point


class PointUserSerializer(PointSerializer):
    city = CitySerializer()