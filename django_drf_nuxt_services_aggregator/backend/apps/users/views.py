from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

import threading
import random

from . import serializers
from .models import CustomUser
from .services import *
from apps.company.models.company import Company


class UserModelViewSet(viewsets.ModelViewSet):
    """
    Класс для создания и обновления модели CustomUser
    """
    # queryset = CustomUser.objects.all()
    queryset = CustomUser.objects.filter(is_superuser=False, is_staff=False)
    serializer_class = serializers.UserSerializer

    def update(self, request, pk):
        self.serializer_class = serializers.UpdateUserSerializer
        return super().update(request, pk)


class DataUserAuthAPIView(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated]
    def list(self, request):
        """
        Возвращает список всех городов
        """
        users = CustomUser.objects.all()
        serializer = serializers.UserSerializer(users, many=True)
        return Response(serializer.data)

    def get_data_auth_user(self, request):
        """
        Возращает данные юсера по Jwt в заголовке headers
        """
        queryset = CustomUser.objects.get(id=request.user.id)
        serializer = serializers.UserSerializer(queryset)
        return Response(serializer.data)

    def add_or_reset_avatar_user(self,request,pk, *args, **kwargs):
        """
        Сохранение аватара пользователя
        """
        user = CustomUser.objects.get(id=pk)
        user.avatar = request.data.get('avatar')
        user.save()
        return Response({'message': 'ok'})

    def delete_avatar_user(self,request,pk, *args, **kwargs):
        """
        Сохранение аватара пользователя
        """
        user = CustomUser.objects.get(id=pk)
        user.avatar.storage.delete(user.avatar.name)
        user.avatar = ''
        user.save()
        return Response({'message': 'ok'})


@api_view(['POST'])
def create(request, *args, **kwargs):
    """
    Регистрация пользователя
    Обязательные поля:
    email password phone
    Поле ячейка генерируется с помощью функции {get_element}
    """
    # print(request.data['email'])
    user = CustomUser.objects.filter(email=request.data['email'])

    if user:
        return Response(
            {'message': 'Пользователь с таким  email  уже существует'},
            status=status.HTTP_400_BAD_REQUEST
        )
    else:
        new_user = CustomUser()
        new_user.email = request.data['email']
        new_user.set_password(request.data['password'])
        new_user.save()
        try:
            company = Company.objects.filter(email = new_user.email).all().update(
                author = new_user)
        except:
            pass
        return Response({'message':'ok'})


@api_view(['GET'])
def send_verifity_email_code(request, *args, **kwargs):
    """
    Отправка кода подтверждения на email
    указанный пользователем
    {status} статус -  1 регистрация статус 2 востановление
    Токен зашивается в кеш браузера в ответе
    и отправляется в таске по емайл и на фронте сверяется
    (пока так что бы не тянуть редис какой либо)
    Статус в котором пользователь запрашивает код для email(регистрация или востановление пароля)
    """
    email = request.GET.get('email')
    status_email = request.GET.get('status')
    token_email = ''.join([str(random.randint(0, 9)) for i in range(0, 6)])

    if status_email == '1':
        # print(123)
        if not CustomUser.objects.filter(email=email).first():
            print(token_email)
            threading.Thread(
                target=send_user_code_notification,
                args=(email, token_email,)
            ).start()
            # send_user_code_notification(email, token_email)

            return Response({'token_email': token_email})
        else:
            return Response(
                {'message': 'Пользователь с таким email уже существует'},
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        user = CustomUser.objects.filter(email=email).first()
        if user:
            # print('ttt',token_email)
            threading.Thread(
                target=send_user_code_notification,
                args=(email, token_email,)
            ).start()
            return Response({'token_email': token_email})
        else:
            return Response(
                {'message': 'Пользователя с таким email не существует'},
                status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['POST'])
def reset_password_user(request, *args, **kwargs):
    """
    Изменение пароля пользователя
    """
    email = request.data.get('email')
    password = request.data.get('password')
    user = CustomUser.objects.get(email=email)
    user.set_password(password)
    user.save()
    return Response({'message': 'Пароль успешно изменен'})


@api_view(['GET'])
def user_email_succes(request, uidb64, token):
    """
    Подтверждение email пользователем
    """
    user = get_email_and_time_left_by_credentials(uidb64, token)
    if user is None:
        return Response({'такой страницы не существует'}, status=status.HTTP_404_NOT_FOUND)
    else:
        user.email_succes = True
        user.save()
        return Response({'message':'Email подтвержден'})
