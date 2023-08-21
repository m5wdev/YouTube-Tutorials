from rest_framework import serializers

from .models import Blog

class BlogSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='get_group_name_display')

    class Meta:
        model = Blog
        fields = '__all__'