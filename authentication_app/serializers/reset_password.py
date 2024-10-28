from rest_framework import serializers
from authentication_app.models import CustomUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
######################### Password Reset Serializer ##############################################

class PasswordResetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "User with this email does not exist."})
        return attrs
    
    def create(self, validated_data):
        user = CustomUser.objects.get(email=validated_data['email'])
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
        current_site = get_current_site(self.request).domain
        port = ":"+str(self.request.META.get('SERVER_PORT'))
        resetLink = "http://"+current_site+port+relativeLink+"?token="+str(token)
        return resetLink