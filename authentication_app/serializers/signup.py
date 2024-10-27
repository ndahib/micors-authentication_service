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
    token = serializers.CharField(max_length=500)
    continuue = serializers.CharField()

    EXPECTED_ACTION = "verify-email"
    EXPECTED_REDIRECT_TYPE = "signup"
    EXPECTED_SCOPE = "verifyEmailLink"
    EXPECTED_ISSUER = "micros/auth_verify_email"

    @staticmethod
    def generate_username(email):
        """Generate username from name"""
        username = slugify(email)
        unique_suffix = str(random.randint(1000, 9999))
        username = f"{username}{unique_suffix}"
        if not CustomUser.objects.filter(username=username).exists():
            return username
        return EmailVerificationSerializer.generate_username(username)

    def validate(self, attrs):
        token = attrs["token"]
        redirect_url = attrs["continuue"]

        try:
            payload = jwt.decode(
                token, os.environ["VERIFICATION_EMAIL_JWT_SECRET"], algorithms=["HS256"]
            )
            if (
                payload["action"] != self.EXPECTED_ACTION
                or payload["redirecType"] != self.EXPECTED_REDIRECT_TYPE
                or payload["scope"] != self.EXPECTED_SCOPE
                or payload["iss"] != self.EXPECTED_ISSUER
                or payload["exp"] < datetime.now().timestamp()
                or redirect_url != os.environ["WELCOME_FRONTEND_URL"]
            ):
                raise serializers.ValidationError("Verification link is invalid or expired.")
            email = payload["sub"]
            if CustomUser.objects.filter(email=email).exists():
                if CustomUser.objects.get(email=email).is_verified:
                    raise serializers.ValidationError(
                        "Verification link is invalid or expired."
                    )
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError("Verification link expired.")
        except jwt.DecodeError:
            raise serializers.ValidationError("Verification link is invalid.")
        except jwt.InvalidTokenError:
            raise serializers.ValidationError("Verification link is invalid.")

        return super().validate({**attrs, "email": email})

    def create(self, validated_data):
        email = validated_data["email"]
        username = self.generate_username(email)
        user = CustomUser.objects.create_user(username, email)
        user.is_complete = True
        user.is_verified = True
        user.save()
        return user

from service_core.settings import PASSWORD_POLICY
######################## Complet Profile Serializer #########################################       
class CompleteProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True, required=True)

    class Meta:
        model = CustomUser 
        fields = ['username', 'password', 'email']

    def validate(self, attrs):
        token = self.context['request'].COOKIES.get("token")
        email = Util.get_email_from_token(token)

        if email is None:
            raise serializers.ValidationError("Invalid token.")
        password = attrs.get('password')
        try:
            PASSWORD_POLICY.test(password)
        except PASSWORD_POLICY.PasswordPolicyError as e:
            raise serializers.ValidationError(e)
        attrs['email'] = email
        return attrs

    def create(self, validated_data):
        user = self._get_user_by_email(validated_data['email'])
        user.set_password(validated_data['password'])
        user.username = validated_data['username']
        user.save()
        return user

    def _get_user_by_email(self, email: str) -> CustomUser:
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({'email': 'User with this email does not exist.'})
