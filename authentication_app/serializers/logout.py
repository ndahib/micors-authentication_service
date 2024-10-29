from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


######################Refresh Token ##################################
class TokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)
    access_token = serializers.CharField(required=True)

    def validate(self, data):
        try:
            RefreshToken(data['refresh_token'], verify=True)
            AccessToken(data['access_token'], verify=True)
        except Exception as error:
            raise serializers.ValidationError({"message": str(error)})
        return data