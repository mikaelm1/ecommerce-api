from django.conf.urls import url
from .views import (
    LoginView, UserRegister, ResendConfirmEmailView,
    ConfirmAccountView
)


urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', UserRegister.as_view(), name='register'),
    url(r'^confirm-account/$', ConfirmAccountView.as_view(),
        name='confirm-account'),
    url(r'^resend-email/$', ResendConfirmEmailView.as_view(), name='resend-email'),
]
