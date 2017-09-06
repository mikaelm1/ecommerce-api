from django.conf.urls import url
from .views import (
    CartDetailView, AddItemToCartView, EditCartView
)


urlpatterns = [
    url(r'^cart/(?P<uid>\d+)$', CartDetailView.as_view(), name='detail'),
    url(r'^add-item$', AddItemToCartView.as_view(), name='add-item'),
    url(r'^edit$', EditCartView.as_view(), name='edit'),
]
