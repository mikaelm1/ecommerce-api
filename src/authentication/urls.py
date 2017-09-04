from django.conf.urls import url
from .views import (
    LoginView, UserRegister, ConfirmAcct, ResendConfirmEmail
)


urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', UserRegister.as_view(), name='register'),
    url(r'^confirm-email/$', ConfirmAcct.as_view(), name='confirm-acct'),
    url(r'^resend-email/$', ResendConfirmEmail.as_view(), name='resend-email'),
]
