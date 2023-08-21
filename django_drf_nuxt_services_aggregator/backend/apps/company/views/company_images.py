from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from apps.company.models.company_image import CompanyImage
from apps.company.serializers.company_image import CompanyImageSerializer


class CompanyImagesModelViewSet(viewsets.ModelViewSet):

    """
    Класс для создания и обновления модели Company
    """

    queryset = CompanyImage.objects.all()
    serializer_class = CompanyImageSerializer


    def create_from_company(self,request,company_id,*args, **kwargs):
        # new_image =  super().create(request,*args, **kwargs)
        new_image = CompanyImage.objects.create(
            image=request.data['image_company'],
            company_id=company_id
            )
        return Response({'message':new_image.id})