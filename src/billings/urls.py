from django.conf.urls import url
from .views import (
    CreateCreditCardView, CreditCardView, BillingHistoryView,
    ReceiptDetailView
)


urlpatterns = [
    url(r'^add-card$', CreateCreditCardView.as_view(), name='add-card'),
    url(r'^card$', CreditCardView.as_view(), name='card'),
    url(r'^purchases$', BillingHistoryView.as_view(), name='purchases'),
    url(r'^purchases/(?P<rid>\d+)$', ReceiptDetailView.as_view(),
        name='purchase-details'),
]
