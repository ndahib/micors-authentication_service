##############################Imports########################################
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

####################################Logout###################################
class LogoutView(APIView):
    def get(self, request):
        try:
            refresh_token = request.headers.get("Authorization")
            print(refresh_token)
            if refresh_token is None:
                return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            if not token.check_blacklist():
                token.blacklist()
            else:
                return Response({"error": "Token is invalid"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Logout Successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)