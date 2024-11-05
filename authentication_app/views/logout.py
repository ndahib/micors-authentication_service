##############################Imports########################################
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.logout import TokenSerializer
from rest_framework_simplejwt.tokens import RefreshToken

####################################Logout###################################

class LogoutView(APIView):

    def post(self, request):
        serializer = TokenSerializer(data={
            'refresh_token': request.COOKIES.get('token'),
            'access_token': request.data.get('access')
        })
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        refresh_token = RefreshToken(serializer.validated_data['refresh_token'])
        refresh_token.blacklist()

        response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        response.set_cookie("token", "", httponly=True, secure=True, samesite="Lax", max_age=0, expires=0)
        return response
