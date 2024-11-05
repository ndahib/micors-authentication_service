import qrcode
import base64
from io import BytesIO
from .utils import Util
from ..models import CustomUser
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_otp.plugins.otp_totp.models import TOTPDevice
from ..serializers.twoFa import TwoFaSerializer, TOTPSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication


class Enable2FaView(generics.GenericAPIView):
    "" " View for enabling 2FA. """

    authentication_classes = [JWTAuthentication]
    serializer_class = TwoFaSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, 
                                           context={"request": request, 'toEnable': True}, 
                                           partial=True)
        
        if serializer.is_valid(raise_exception=True) is True:
            user = serializer.update(serializer.validated_data)
            if user.is_2fa_enabled is True:
                device, created = TOTPDevice.objects.get_or_create(user=user, name="Pingo")
                if created:
                    device.save()
                return Response({"two_factor_enabled": user.is_2fa_enabled}, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
   
class Disable2FaView(generics.GenericAPIView):
    """ View for disabling 2FA. """

    serializer_class = TwoFaSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, 
                                           context={"request": request, 'toEnable': False}, 
                                           partial=True)
        
        if serializer.is_valid(raise_exception=True) is True:
            user = serializer.update(serializer.validated_data)
            if user.is_2fa_enabled is False:
                TOTPDevice.objects.filter(user=user).delete()
                return Response({"two_factor_enabled": user.is_2fa_enabled}, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CodeQrGenerator(APIView):
    """ Generates QR code for 2FA , Assuming the user enabled 2FA. """

    def get(self, request):
        user = CustomUser.objects.get(username="ndahib")
        if user.is_2fa_enabled is False:
            return Response({"message": "2FA not enabled"}, status=status.HTTP_400_BAD_REQUEST)
        device = TOTPDevice.objects.get(user=user, name="Pingo")
        otp_uri = device.config_url

        qr = qrcode.make(otp_uri)
        buffer = BytesIO()
        qr.save(buffer, "PNG")
        buffer.seek(0)

        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return Response({"qr_code": img_base64}, status=status.HTTP_200_OK)
    

class Verify2FaView(generics.GenericAPIView):
    """ View for verifying 2FA. """

    serializer_class = TOTPSerializer

    def post(self, request):
        # user is in jwt token 
        serializer = self.serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            response = Util.build_response(serializer.validated_data)
            print(response)
            response.set_cookie(
                key="token", 
                value="", 
                max_age=0,
                expires=0,)
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   