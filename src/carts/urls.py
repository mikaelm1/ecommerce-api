from django.conf.urls import url
from .views import (
    CartDetailView
)


urlpatterns = [
    url(r'^cart/(?P<uid>\d+)/(?P<cid>\d+)/$', CartDetailView.as_view(), name='detail'),
]
