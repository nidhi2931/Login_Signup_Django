from django.urls import path
from .views import CustomAuthToken,SignupAPIView

urlpatterns=[
    path('signup/',SignupAPIView.as_view(),name='signup'),
    path('login/',CustomAuthToken.as_view(), name='login')
]