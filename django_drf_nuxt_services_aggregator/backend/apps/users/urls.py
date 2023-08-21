from django.urls import path

from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('', UserModelViewSet.as_view({'get': 'list'}), name='list'),
    # path('create/', UserModelViewSet.as_view({'post': 'create'}), name='create'),
    path('users/',DataUserAuthAPIView.as_view({'get': 'list'}), name="list"),

    path('user-data/',DataUserAuthAPIView.as_view({'get': 'get_data_auth_user'}), name="user_data"),

    path('create/', create, name='create'),
    path('add-avatar/<int:pk>/',DataUserAuthAPIView.as_view({'post': 'add_or_reset_avatar_user'}), name="add_or_reset_avatar_user"),
    path('delete-avatar/<int:pk>/',DataUserAuthAPIView.as_view({'delete': 'delete_avatar_user'}), name="delete_avatar_user"),
    path('send-code/', send_verifity_email_code, name='send_verifity_email_code'),
    path('reset-password/', reset_password_user, name='reset_password_user'),

    path('verify-email/<uidb64>/<token>/', user_email_succes, name='user_email_succes'),
    path('<int:pk>/', UserModelViewSet.as_view({'put': 'update'}), name='update'),
    path('retrieve/<int:pk>/', UserModelViewSet.as_view({'get': 'retrieve'}), name='retrieve'),
    path('delete/<int:pk>/', UserModelViewSet.as_view({'delete': 'destroy'}), name='delete'),

    #auth
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
