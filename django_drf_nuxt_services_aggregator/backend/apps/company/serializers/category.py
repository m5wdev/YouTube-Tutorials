from rest_framework import serializers

from apps.company.models.category import Category

class ChildrenCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    children_category = ChildrenCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'