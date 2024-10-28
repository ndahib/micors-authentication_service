
from django.urls import path, re_path
from .views.signup import SignUpView , EmailVerificationView, CompleteProfileView
from .views.reset_password import PasswordResetView, PasswordResetConfirmView, SetNewPasswordView

urlpatterns = [
    re_path(r'^signup$', SignUpView.as_view(), name='signup'),
    path('signup/verify', EmailVerificationView.as_view(), name='email-verify'),
    path('signup/complete', CompleteProfileView.as_view(), name='complete_profile'),

    re_path(r'^reset$', PasswordResetView.as_view(), name="reset-password"),
    path("password-reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    path("set-new-password", SetNewPasswordView.as_view(), name="set-new-password"),


    re_path(r'^login$', PasswordResetView.as_view(), name="reset-password"),

]