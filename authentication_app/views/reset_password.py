from rest_framework import generics, status
from rest_framework.response import Response
from ..serializers.reset_password import PasswordResetSerializer
from .utils import Util
# ############################### Password Reset View ################################
class PasswordResetView(generics.GenericAPIView):
    """View for password reset that takes an email and sends a password reset link"""

    serializer_class = PasswordResetSerializer
    
    def post(self, request):
        print("Request --->> :", request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        reset_link = serializer.save()
        print("Reset Link --->> :", reset_link)
        Util.send_reset_password_email(serializer.validated_data["email"], reset_link=reset_link)
        return Response({"message": "Password reset email sent successfully"}, status=status.HTTP_200_OK)