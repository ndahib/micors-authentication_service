
from django.urls import path, re_path
from .views.signup import SignUpView , EmailVerificationView, CompleteProfileView

urlpatterns = [
    re_path(r'^signup$', SignUpView.as_view(), name='signup'),
    # path('signup', SignUpView.as_view(), name='signup'),
    path('signup/verify', EmailVerificationView.as_view(), name='email-verify'),
    path('signup/complete', CompleteProfileView.as_view(), name='complete_profile'),
]