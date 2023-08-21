# from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from apps.company.serializers.point import Point
from apps.company.serializers.point import PointSerializer


class PointModelViewSet(viewsets.ModelViewSet):
    """
    Класс для создания и обновления модели Point
    """
    queryset = Point.objects.all()
    serializer_class = PointSerializer
