from django.conf.urls import url
from .views import CreateCreditCardView


urlpatterns = [
    url(r'^add-card$', CreateCreditCardView.as_view(), name='add-card'),
]
