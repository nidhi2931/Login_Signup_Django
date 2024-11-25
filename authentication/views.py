from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
# Create your views here.



class SignupAPIView(APIView):
    def post(self,request,*args,**kwargs):
        username=request.data.get('username')
        email=request.data.get('email')
        password=request.data.get('password')

        # check if all required fields are provided
        if not username or not password or not email:
            return Response({"error":"Please provide username,email and password"},status=status.HTTP_400_BAD_REQUEST)

        # check if username is already exists
        if User.objects.filter(username=username).exists():
            return Response({"error":"Username already exists"},status=status.HTTP_400_BAD_REQUEST)

        # create a new user
        user=User.objects.create_user(username=username,email=email,password=password)


        # Generate anew token for each user

        token,created=Token.objects.get_or_create(user=user)

        return Response({
                "message":"User created successfully",
                "username":user.username,
                "email":user.email,
                "token":token.key,},status=status.HTTP_201_CREATED)


class CustomAuthToken(ObtainAuthToken):
    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token,created = Token.objects.get_or_create(user=user)

        return Response({
            'token':token.key,
            'user_id':user.pk,
            'email':user.email
        })

