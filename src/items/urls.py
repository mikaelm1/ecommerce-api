from django.conf.urls import url
from .views import (
    ItemsView
)

urlpatterns = [
    url(r'^index/$', ItemsView.as_view(), name='index'),
]
