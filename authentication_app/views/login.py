from rest_framework import generics, status
from rest_framework.response import Response
from ..serializers.login import LoginSerializer
#################################Login###################################
class LoginView(generics.GenericAPIView):
    """View for user login that takes email and password and returns 
    access and refresh token"""

    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        response = Response(
            {
                "message": "Login successful",
                "username": validated_data["username"],
                "email": validated_data["email"],
                "refresh": validated_data["tokens"]["access"],
            },
            status=status.HTTP_200_OK,
        )
        response.set_cookie(
            key="r_token",
            value=str(validated_data["tokens"]["refresh"]), 
            httponly=True,
            secure=True,
            samesite="Strict",
            max_age=1800,
            expires=1800,
            path="/login",
            domain="127.0.0.1",
        )
        return response


