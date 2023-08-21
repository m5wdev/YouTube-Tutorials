from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Blog
from .serializers import BlogSerializer


@api_view(['GET'])
def get_blog_for_group(request):
    """
    Возвращает запись блога по названию группы блога
    """

    group_name = request.GET.get('group_name')
    blog_filter = Blog.objects.filter(group_name=group_name).first()
    if blog_filter is None:
        return Response({'такой страницы не существует'}, status=status.HTTP_404_NOT_FOUND)
    else:
        serializer = BlogSerializer(blog_filter)
        return Response(serializer.data)
