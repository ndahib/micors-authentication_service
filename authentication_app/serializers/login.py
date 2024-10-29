
####################################Login###################################
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from ..models import CustomUser

class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    username = serializers.CharField(required=False, read_only=True)
    tokens = serializers.SerializerMethodField(method_name='get_tokens', read_only=True)

    def get_tokens(self, obj):
        user = CustomUser.objects.get(email=obj['email'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }
    
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email= attrs.get('email', '')
        password = attrs.get('password', '')
        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
        }
