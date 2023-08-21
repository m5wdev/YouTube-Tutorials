from rest_framework import serializers

from .models.company_application import CompanyApplication
from .models.company_abuse import CompanyAbuse
from .models.repair_application import RepairApplication


class CompanyApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyApplication
        # fields = '__all__'
        exclude = ('created_at', )


class CompanyAbuseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyAbuse
        # fields = '__all__'
        exclude = ('created_at', )


class RepairApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairApplication
        # fields = '__all__'
        exclude = ('created_at', )
