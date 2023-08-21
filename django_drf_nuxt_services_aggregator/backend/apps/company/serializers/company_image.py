from rest_framework import serializers

from apps.company.models.company_image import CompanyImage

class CompanyImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyImage
        fields = '__all__'