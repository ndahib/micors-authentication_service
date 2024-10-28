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
        html_message = render_to_string('reset_password.html', {'verification_link': reset_link})
        plain_message = strip_tags(html_message)
        from_email = 'Micros <' + os.environ.get("EMAIL_USER") + '>'
        to = email
        email = EmailMultiAlternatives(subject, plain_message, from_email, [to])
        email.attach_alternative(html_message, "text/html")
        email.send()



#https://id.atlassian.com/login/changepassword?continue=https%3A%2F%2Fwww.atlassian.com%2Fgateway%2Fapi%2Fstart%2Fauthredirect&signature=eyJraWQiOiJtaWNyb3MvYWlkLWFjY291bnQvYWJjZDY1dGo3NnBxZDdpNiIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJ2b2hpeWVsMTEwQG5lc3R2aWEuY29tIiwiYXVkIjoibGluay1zaWduYXR1cmUtdmFsaWRhdG9yIiwibmJmIjoxNzMwMTA0ODA2LCJzY29wZSI6ImNoYW5nZVBhc3N3b3JkIiwiaXNzIjoibWljcm9zL2FpZC1hY2NvdW50IiwiZXhwIjoxNzMwMTA4NDA2LCJ1c2VySWQiOiI3MTIwMjA6OWRlZWMxN2QtNGIxNC00MTNjLWJmNjItOWJmZWUyMTNjZmI5IiwiaWF0IjoxNzMwMTA0ODA2LCJqdGkiOiJhMjdmYTIwYS05YjY0LTQ2ZmItODkzNC0xNDFmMzU4MDcxM2IifQ.ECzgOb5q1ObTlVSi1CXjZHZMxy2V1wMwRkI6LiK2pwrpDKl2jXYLexGPYMSq2zWORpUOeYIBW89e5hzM72sMSBzElEyr8-E_f501jSouR1Crxu6MLjuHmf9znECtceEAvfJBspZGQ0vbN12RBa3L1o17Am8q3tbd7qAAeUn9qTOVG4yAX_lj7T-AJway6YE4bJrO8k2-4e7E8XXzhPDJ9gvAfNngxl1OPQAHCOxj0b2xjrQQ5CNRZHJsnk1PC_oMYU5WK2nVJo7oMqcguHRTkH7yJch6ywUQZ1Oj0JuFm6fg3aQUiKR_tdmKYZ_Lx07hGw6_Yq9DxIHM3aBzL_m3fg&source=9607060d97aac19f42cc5c59b0ec4a1d
