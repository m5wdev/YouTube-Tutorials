from rest_framework import serializers

from apps.company.models.often_repair import OftenRepair


class OftenRepairSerializer(serializers.ModelSerializer):
    class Meta:
        model = OftenRepair
        # fields = '__all__'
        fields = ['name', 'slug']
