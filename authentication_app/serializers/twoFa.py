from rest_framework import serializers
from authentication_app.models import CustomUser
from django.contrib import auth
class TwoFaSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['is_2fa_enabled', 'password']
    
    def validate(self, attrs):
        password = attrs.get('password')
        toEnable = self.context['toEnable']
        # user = self.context['request'].user
        # print("---------->>", user.is_anonymous)
        try:
            user = CustomUser.objects.get(username="ndahib")
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('Invalid credentials')
        if not user.check_password(password):
            raise serializers.ValidationError('Invalid credentials')
        return {
            'instance': user,
            'toEnable': toEnable}
    
    def update(self, validated_data):
        instance = validated_data['instance']
        instance.is_2fa_enabled = validated_data['toEnable']
        instance.save()
        return instance


from django_otp.plugins.otp_totp.models import TOTPDevice
import jwt
from django.conf import settings

class TOTPSerializer(serializers.Serializer):
    """TOTP Serializer for TOTP verification"""

    totp = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        totp = attrs.get('totp')
        jwt_token = self.context['request'].COOKIES.get('token')
        try:
            decoded_token  = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
            payload = decoded_token.payload
            email = payload.get('sub')
            if not email:
                raise serializers.ValidationError('Invalid credentials')
            user = CustomUser.objects.get(email=email)
            device =  TOTPDevice.objects.get(user=user, name="Pingo")
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('Invalid credentials')
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Token expired')
        except jwt.DecodeError:
            raise serializers.ValidationError('Invalid token')
        except TOTPDevice.DoesNotExist:
            raise serializers.ValidationError('Invalid credentials')
        if not device.verify_token(totp):
            raise serializers.ValidationError('Invalid TOTP')
        return attrs