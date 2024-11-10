import os
from .utils import Util
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.signup import EmailVerificationSerializer, SignUpSerializer, CompleteProfileSerializer

#################################### Sign Up View ########################################
class SignUpView(generics.GenericAPIView):
    """
    View for user signup that sends an email verification with an account activation link
    containing an access token generated by JWT.
    """

    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            try:
                Util.send_verificationEmail(request=request, email=email)
            except:
                return Response({"message": "Email not sent"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

############################### Email Verification View# ###################################

class EmailVerificationView(generics.GenericAPIView):
    """
    View for email verification that takes an token generated by JWT
    and redirects the user to the welcome page.
    """
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = None


        query_params = {key: str(value) for key, value in request.query_params.items()}
        serializer = self.serializer_class(data=query_params)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()
        response = Response({"message": "Verification successful."}, status=status.HTTP_200_OK)
        
        if token: 
            response.set_cookie(
                key='token',
                value=str(token), 
                httponly=True,
                # secure=True,
                samesite='Lax',
                path=os.environ.get("COMPLETE_URL"),
                expires= 10 * 60,
                max_age= 10 * 60
            )

        response['Location'] = os.environ.get("WELCOME_FRONTEND_URL")
        response.status_code = status.HTTP_302_FOUND
        return response


####################Complete Profile View ##############################################
class CompleteProfileView(APIView):
    """View for completing a user's profile that takes a token generated by JWT."""

    serializer_class = CompleteProfileSerializer

    def post(self, request) -> Response:
        """Handles the POST request to complete a user's profile."""

        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = user.tokens()
        # if Util.create_user_profile(user) is False:
        #     return Response({"message": "Error creating user profile"}, status=status.HTTP_400_BAD_REQUEST) # to change later
        response = Response({"message": "Profile completed successfully", 
                            "access": tokens["access"],},
                            status=status.HTTP_200_OK)
        response.set_cookie("r_token", tokens["refresh"], httponly=True, secure=True, samesite="Lax")
        # set cokkie token to expire that and remove it form the token database
        return response
