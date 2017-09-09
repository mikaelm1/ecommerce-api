from django.conf.urls import url
from .views import (
    CreateCreditCardView, CreditCardView
)


urlpatterns = [
    url(r'^add-card$', CreateCreditCardView.as_view(), name='add-card'),
    url(r'^card$', CreditCardView.as_view(), name='card'),
]
