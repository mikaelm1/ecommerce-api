from django.conf.urls import url
from .views import (
    ItemsView, ItemDetailView
)

urlpatterns = [
    url(r'^$', ItemsView.as_view(), name='index'),
    url(r'^item/(?P<id>\d+)/$', ItemDetailView.as_view(), name='detail'),
]
