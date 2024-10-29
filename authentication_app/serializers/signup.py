import re
import os
import jwt
import random
from datetime import datetime
from django.utils.text import slugify
from rest_framework import serializers
from authentication_app.models import CustomUser
from service_core.settings import PASSWORD_POLICY
from rest_framework_simplejwt.tokens import AccessToken
from datetime import datetime, timedelta
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

    EXPECTED_ACTION = "verify-email"
    EXPECTED_REDIRECT_TYPE = "signup"
    EXPECTED_SCOPE = "verifyEmailLink"
    EXPECTED_ISSUER = "micros/auth_verify_email"

    @staticmethod
    def _generate_username(email):
        base_username = slugify(email)
        unique_suffix = str(random.randint(1000, 9999))
        new_username = f"{base_username}{unique_suffix}"
        if not CustomUser.objects.filter(username=new_username).exists():
            return new_username
        return EmailVerificationSerializer._generate_username(email)

    def validate(self, attrs):
        token = attrs.get("token")
        try:
            payload = jwt.decode(
                token, os.environ["VERIFICATION_EMAIL_JWT_SECRET"], algorithms=["HS256"]
            )
            if (
                payload.get("action") != self.EXPECTED_ACTION
                or payload.get("redirecType") != self.EXPECTED_REDIRECT_TYPE
                or payload.get("scope") != self.EXPECTED_SCOPE
                or payload.get("iss") != self.EXPECTED_ISSUER
                or payload.get("exp") < datetime.now().timestamp()
            ):
                raise serializers.ValidationError("Verification link is invalid or expired.")

            email = payload.get("sub")
            user = CustomUser.objects.filter(email=email).first()
            if user and user.is_verified:
                raise serializers.ValidationError("User is already verified, Complete your profile.", 
                                                  code="user_verified")
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError("Verification link expired.")
        except (jwt.DecodeError, jwt.InvalidTokenError) as e:
            raise serializers.ValidationError("Verification link is invalid.")

        attrs["email"] = email
        return super().validate(attrs)

    def create(self, validated_data):
        email = validated_data.get("email")
        username = self._generate_username(email)
        user = CustomUser.objects.create_user(username=username, email=email)
        user.is_verified = True
        user.save()

        access_token = AccessToken.for_user(user)
        access_token['aud'] = "link-signature-validator"
        access_token['sub'] = email
        access_token['scope'] = "welcome"
        access_token['iss'] = "micros/sign-in"
        access_token['redirectType'] = "signup"
        access_token.set_exp(lifetime=timedelta(hours=1))
        
        return user, access_token
    

######################## Complet Profile Serializer #########################################       
class CompleteProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True, required=True
    )
    username = serializers.CharField(max_length=255, required=True)
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email']

    def validate(self, attrs):
        token = self.context['request'].COOKIES.get('token')
        email = self._get_email_from_token(token)

        if email is None:
            raise serializers.ValidationError({'token': 'Invalid token.'})

        password = attrs.get('password')
        try:
            PASSWORD_POLICY.test(password)
        except PASSWORD_POLICY.PasswordPolicyError as e:
            raise serializers.ValidationError({'password': str(e)})

        attrs['email'] = email
        return attrs

    def create(self, validated_data):
        user = self._get_user_by_email(validated_data['email'])
        user.set_password(validated_data['password'])
        user.username = validated_data['username']
        user.is_complete = True
        user.save()
        return user

    def _get_user_by_email(self, email: str) -> CustomUser:
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({'email': 'User with this email does not exist.'})

    def _get_email_from_token(self, token: str) -> str:
        access_token = AccessToken(token)
        access_token.verify()
        payload = access_token.payload
        if (
            payload['scope'] != 'welcome'
            or payload['iss'] != 'micros/sign-in'
            or payload['redirectType'] != 'signup'
        ):
            raise Exception('Invalid token')
        return access_token['sub']

