import os
import jwt
from django.urls import reverse
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import AccessToken
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

class Util:
    @staticmethod
    def generate_token(payload):
        token = jwt.encode(payload=payload, key=os.environ.get("VERIFICATION_EMAIL_JWT_SECRET"), algorithm="HS256")
        return token

    @staticmethod
    def create_email_data(request, email, token):
        current_site = get_current_site(request)
        relativeLink = reverse("email-verify")
        port = ":"+str(request.META.get('SERVER_PORT'))
        absoluteLink = "http://"+current_site.domain+port+relativeLink+"?token="+str(token)
        verification_link = absoluteLink
        subject = "Verify your email"
        html_message = render_to_string('email.html', {'verification_link': verification_link})
        plain_message = strip_tags(html_message)
        from_email = 'Micros <' + os.environ.get("EMAIL_USER") + '>'
        to = email
        email = EmailMultiAlternatives(subject, plain_message, from_email, [to])
        email.attach_alternative(html_message, "text/html")
        email.send()

    @staticmethod
    def send_verificationEmail(request, email):
        payload = {
            "sub": email,
            'exp': datetime.now() + timedelta(hours=1),
            'iss': "micros/auth_verify_email",
            'scope': 'verifyEmailLink',
            'redirecType': 'signup',
            'action': "verify-email",
        }
        token = Util.generate_token(payload=payload)
        Util.create_email_data(request, email, token)
    



    #     @staticmethod
    # # change the name of this function and genrate it with reset password
    # def create_email_data(request, email, token):
    #     current_site = get_current_site(request)
    #     relativeLink = reverse("email-verify")
    #     port = ":"+str(request.META.get('SERVER_PORT'))
    #     absoluteLink = "http://"+current_site.domain+port+relativeLink+"?token="+str(token)
    #     verification_link = absoluteLink
    #     subject = "Verify your email"
    #     html_message = render_to_string('email.html', {'verification_link': verification_link})
    #     plain_message = strip_tags(html_message)
    #     from_email = 'Micros <' + os.environ.get("EMAIL_USER") + '>'
    #     to = email
    #     email = EmailMultiAlternatives(subject, plain_message, from_email, [to])
    #     email.attach_alternative(html_message, "text/html")
    #     email.send()

    @staticmethod
    def send_reset_password_email(email, reset_link):
        subject = "Reset your password"
        html_message = render_to_string('reset_password.html', {'reset_link': reset_link})
        plain_message = strip_tags(html_message)
        from_email = 'Micros <' + os.environ.get("EMAIL_USER") + '>'
        to = email
        email = EmailMultiAlternatives(subject, plain_message, from_email, [to])
        email.attach_alternative(html_message, "text/html")
        email.send()

