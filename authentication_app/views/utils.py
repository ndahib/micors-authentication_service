import os
import jwt
from django.urls import reverse
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from datetime import datetime, timedelta

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        # email.send()
    
    @staticmethod
    def generate_token(payload):
        token = jwt.encode(payload=payload, key=os.environ.get("VERIFICATION_EMAIL_JWT_SECRET"), algorithm="HS256")
        return token

    @staticmethod
    def create_email_data(request, email, token):
        current_site = get_current_site(request)
        relativeLink = reverse("email-verify")
        port = ":"+str(request.META.get('SERVER_PORT'))
        redirectUrl = os.environ.get("WELCOME_FRONTEND_URL")
        absoluteLink = "http://"+current_site.domain+port+relativeLink+"?token="+str(token)+"&continuue="+redirectUrl  #tochange later to HTTPS
        email_body = "Hi, Use link below to verify your email \n"+absoluteLink
        email = {
            "email_body": email_body,
            "email_subject": "Verify your email",
            "to_email": email          
        }
        print(email)
        return email

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
        email_data = Util.create_email_data(request, email, token)
        Util.send_email(data=email_data)
    


# https://id.atlassian.com/signup/verify-email/otp?continue=https%3A%2F%2Fwww.atlassian.com%2Fgateway%2Fapi%2Fstart%2Fauthredirect&token=eyJraWQiOiJtaWNyb3MvYWlkLWFjY291bnQvcGo2OGV2Z2V0cjhtaGZhdiIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJ5aWhvcml3NTE1QHJlZ2lzaHViLmNvbSIsImF1ZCI6Imxpbmstc2lnbmF0dXJlLXZhbGlkYXRvciIsIm5iZiI6MTcyOTkzMTY1NCwibWZhVG9rZW4iOiJleUpyYVdRaU9pSnRhV055YjNNdmFXUXRZWFYwYUdWdWRHbGpZWFJwYjI0dllqZGpkR2R5YkhWbmNYWTNPRzV1YWlJc0ltRnNaeUk2SWxKVE1qVTJJbjAuZXlKemRXSWlPaUp0YVdOeWIzTXZhV1F0WVhWMGFHVnVkR2xqWVhScGIyNGlMQ0pqYjI1MFlXbHVaWEpVZVhCbElqb2laMnh2WW1Gc0lpd2lhWE56SWpvaWJXbGpjbTl6TDJsa0xXRjFkR2hsYm5ScFkyRjBhVzl1SWl3aWNISnZkbWxrWldSR1lXTjBiM0p6SWpwYlhTd2lkSEpoYm5OaFkzUnBiMjVKWkNJNkluVnpMV1ZoYzNRdE1YeGpNVEk0TVRabE1pMHhOVE5pTFRSallUTXRZVGhsWVMxaU1qRmxPV015TkdabU1EZ2lMQ0p6ZFdKVFkyOXdaU0k2SWtWdFlXbHNUM2R1WlhKemFHbHdJaXdpWVhWa0lqb2lhV1F0WVhWMGFHVnVkR2xqWVhScGIyNGlMQ0psYldGcGJFRmtaSEpsYzNNaU9pSjVhV2h2Y21sM05URTFRSEpsWjJsemFIVmlMbU52YlNJc0ltNWlaaUk2TVRjeU9Ua3pNVFkxTkN3aWMyTnZjR1VpT2lKTlptRkRhR0ZzYkdWdVoyVWlMQ0ptWVdOMGIzSlVlWEJsSWpvaVJVMUJTVXdpTENKbGVIQWlPakUzTWprNU16TTBOVFFzSW1saGRDSTZNVGN5T1Rrek1UWTFOQ3dpYW5ScElqb2lkWE10WldGemRDMHhmRFl3TldJMFpEWXpMVEV4WmpJdE5EQmhNUzA1TTJNNExUWXhZakU1TkdWaFptTmhaQ0o5LmlEY3JQaUg3cG1mYTNWTVY0Tm1aQ0dYbDNpc0VEazdNb0dwVGMtQ1JBUlJBbkR4WENWVGV0OGpjcl9LcUJLWkl5V21ydUJoaFl1Sm91Q05kWmgzNnU0MEhGTmdCMVl6SDUySHhDYjN5dDFQNHNUSUJaWHFPeXlIYlBNSGlNOUVORnI4ZjZQakRXQkRuRzZ4SGFRS2ZvWWl0Y0NzVk5CSlFhb25wVWxfMERMZjlSd2RrbTVXdFpXbTluSXNvY19abmRCXzdFX0RyTjI5aC1RNjU5LW9KckZJTTNwaEpIUmU4QjZfZVVtVUhyZDRpMmkydENLWENqSFplM3BsNTBRRFVobUlyQ2FDT2c2ODhPX3FlSU5menllTXFPYzNMbVhWN3huQTVyX3hicFpfanJNVWpGM2FmM2czc0pfLTg0UlJWdldXQzZmYVhpeHRvdmhZQnVkYk1JdyIsInNjb3BlIjoidmVyaWZ5RW1haWxPdHAiLCJpc3MiOiJtaWNyb3MvYWlkLWFjY291bnQiLCJyZWRpcmVjdFR5cGUiOiJzaWdudXAiLCJleHAiOjE3Mjk5MzI1NTQsInVzZXJJZCI6IjcxMjAyMDpkYTI3YzE3ZS00N2Q3LTRjNGYtOWI5MC1iMTQxZWU0OTgxNzgiLCJyZWNhcHRjaGFTY29yZSI6IjAuOSIsImlhdCI6MTcyOTkzMTY1NCwianRpIjoiM2VhNDgzMTMtMmRhNS00ZTNkLWExODgtMzlhMTk1YmMwZWZkIn0.fA_oqRDQGyNcFav7q-iISKZLJ0RSawjMLu9Y9YNiR3lmSY69n_c_dQBxOsqeRgpgGKzVfMtS5hv3VfmbRVRweCmD_aTWET5pKKDWySbhPuPbmhU5ki1zvjBOEfKTwL4fBy9eFpsD0INGXn4x8NDLL547FHS6OaxAPIrQTtcn1MA-c3Bee0roiX5RAmB7YzxH26VYINJgu6NuLnCAXqlsr7MMftXZtF5fB4pbz3VOS9WIO0voaf1XWLEBfbNnyWp8-TnZIfrY57gxUA_qCty7hXATXr946SBHHH5P2Gy7xuvjRokAhFiV3M9U1FB7WaWiEquf6xKIzjNknkRzc3cGgw
# https://id.atlassian.com/signup/welcome?token=eyJraWQiOiJtaWNyb3Mvc2lnbi1pbi1zZXJ2aWNlL29hdXB2aHZuaTFvNDljN3IiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiJsaW5rLXNpZ25hdHVyZS12YWxpZGF0b3IiLCJzdWIiOiJqb3llZG92NzcyQHJlZ2lzaHViLmNvbSIsIm5iZiI6MTcyOTkzMTI2Mywic2NvcGUiOiJ3ZWxjb21lIiwiaXNzIjoibWljcm9zL3NpZ24taW4tc2VydmljZSIsInJlZGlyZWN0VHlwZSI6InNpZ251cCIsImV4cCI6MTczMDUzNjA2MywicmVjYXB0Y2hhU2NvcmUiOiIwLjkiLCJpYXQiOjE3Mjk5MzEyNjMsImp0aSI6ImU3OTU4MmFhLTcwNDMtNDg5NS1hNTIyLWE1ODI2YmU5MDI5OSJ9.hu8RjAKZw2TG3cczVvLKviSQDnWyo_CycGF7hR7GWcJ-2TXRjd4gQrJeYJ-pyjJO240Uuxx_rT-XGOFatn1E_E6kfPYEvp57T4_yFYnv7g1bkiA5GYWxZef4YkFcyhnZyTZ3uYeTxmSfTJwd_Wv4CeWMQVAE6yf7HXdpFt-dAqgH-klB46VMUhvokcI54Sz1YrbPqGsAURLhu6NoC_wbrvkfge3zUNJ0phZ7t7tctPWdZBebS9rTN1DTSdBzVrU3pJb-K-5IWHnjKWiq2nRJf-StcNFblOTa6h8mR8oBNGCdOiWWFJOuAfwiK0RfzEGzPcIpxACgxcwLyxIwIVygwA&continue=https%3A%2F%2Fwww.atlassian.com%2Fgateway%2Fapi%2Fstart%2Fauthredirect