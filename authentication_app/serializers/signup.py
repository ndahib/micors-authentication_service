import re
import os
import jwt
import random
from datetime import datetime
from django.utils.text import slugify
from rest_framework import serializers
from authentication_app.models import CustomUser


######################################Sign Up Serializer########################################
class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if len(email) > 6 and re.match("^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email) != None:
                return email
        raise serializers.ValidationError('Email is not valid')

    def validate(self, attrs):
        email = attrs.get('email')
        validated_email = self.validate_email(email)
        user = CustomUser.objects.filter(email=validated_email)
        is_exist = user.exists()
        if is_exist and user.get().is_complete:
            raise serializers.ValidationError('User already exists and is complete')
        return super().validate(attrs)

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
    

######################################Email Verification Serializer################################
class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)
    url = serializers.CharField(max_length=255)
    email = serializers.EmailField()

    class Meta:
        model = CustomUser
        fields = ['email']
    

    EXPECTED_ACTION = "verify-email"
    EXPECTED_REDIRECT_TYPE = "signup"
    EXPECTED_SCOPE = "verifyEmailLink"
    EXPECTED_ISSUER = "micros/auth_verify_email"
    
    @staticmethod
    def _generate_username(email):
        """Generate username from name
        """
        username = slugify(email)
        unique_suffix = str(random.randint(1000, 9999))
        username = username + unique_suffix
        if not CustomUser.objects.filter(username=username).exists():
            return username
        else:
            return EmailVerificationSerializer._generate_username(username)

    def validate(self, attrs):
        token = attrs.get('token')
        url = attrs.get('continue')

        try:
            payload = jwt.decode(token, os.environ.get("VERIFICATION_EMAIL_JWT_SECRET"), algorithms=["HS256"])
            
            if (payload['action'] != self.EXPECTED_ACTION or
                payload['redirecType'] != self.EXPECTED_REDIRECT_TYPE or
                payload['scope'] != self.EXPECTED_SCOPE or
                payload['iss'] != self.EXPECTED_ISSUER or
                payload['exp'] < datetime.now().timestamp() or
                url != f"{os.environ.get('VERIFICATION_EMAIL_LINK')}?token={token}"):
                raise serializers.ValidationError("Verification link is invalid or expired.")
        
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError("Verification link expired.")
        except jwt.DecodeError:
            raise serializers.ValidationError("Verification link is invalid.")
        except jwt.InvalidTokenError:
            raise serializers.ValidationError("Verification link is invalid.")
        
        return super().validate(attrs)
    

    def create(self, validated_data):
        email = validated_data.get('email')
        username = self._generate_username(email)
        is_complete = False
        is_verified = True
        return CustomUser.objects.create_user(username=username, 
                                            email=email, 
                                            is_complete=is_complete, 
                                            is_verified=is_verified)


######################## Complet Profile Serializer #########################################
class CompleteProfileSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, min_length=8, write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password']
    
    def validate(self, attrs):
        # check if password in strong 
        password = attrs.get('password')
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if r'[^A-Za-z0-9]' not in password:
            raise serializers.ValidationError("Password must contain at least one digit and one special character.")
        if not any(char.isupper() for char in password):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        return super().validate(attrs)

    def create(self, validated_data):
        user = CustomUser.objects.get(email=validated_data.get('email'))
        user.set_password(validated_data.get('password'))
        user.is_complete = True
        user.username = validated_data.get('username')
        user.save()
        return user
    
        
        