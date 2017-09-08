from django.conf.urls import url
from .views import (
    CartDetailView, AddItemToCartView, EditCartView, CheckoutView
)


urlpatterns = [
    url(r'^cart$', CartDetailView.as_view(), name='detail'),
    url(r'^add-item$', AddItemToCartView.as_view(), name='add-item'),
    url(r'^edit$', EditCartView.as_view(), name='edit'),
    url(r'^checkout$', CheckoutView.as_view(), name='checkout'),
]
