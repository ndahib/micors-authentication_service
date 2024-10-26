
from django.urls import path
from .views.signup import SignUpView

urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    # path('signup', SignUpView.as_view(), name='email-verify'),
    # path('signup', SignUpView.as_view(), name='finish_signup'),
]