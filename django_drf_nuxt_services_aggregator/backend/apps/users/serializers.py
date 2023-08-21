from rest_framework import serializers

from .models import CustomUser
from .services import send_verify_link_email


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['first_name','username']

class UserSerializer(serializers.ModelSerializer):

    """
    Возвращает данные пользователя .
    Исключается поле {password}
    """


    password = serializers.CharField(
    min_length=4,
    write_only=True,
    required=True,
    style={'input_type': 'password'}
    )

    class Meta:
        model = CustomUser
        fields = '__all__'



