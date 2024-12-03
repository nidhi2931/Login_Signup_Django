from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class CustomAuthTokenSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password =serializers.CharField(write_only=True)

    def validate(self,attrs):
        email=attrs.get('email')
        password=attrs.get('password')
        try:
            user=User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid Email or Password')

        user=authenticate(username=user.username,password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password")
        
        attrs['user']=user
        return attrs




