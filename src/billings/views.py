from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ecommerce.permissions import EmailConfirmed
from .utils_stripe import StripeWrapper
from .models import CreditCard
from .serializers import (
    CreditCardSerializer, CreateCreditCardSerializer, EditCreditCardSerializer
)

"""
Stripe Testing Credit Card Numbers:
    https://stripe.com/docs/testing#cards
Stripe Client Side Tokens. Recommended:
    https://stripe.com/docs/phone-verification-for-cards#how-to-securely-collect-payment-details
"""


class CreateCreditCardView(APIView):
    """
    post:
    Create a new CreditCard for a user.
    """
    permission_classes = (IsAuthenticated, EmailConfirmed,)

    def post(self, req):
        d = req.data
        ser = CreateCreditCardSerializer(data=d)
        if ser.is_valid() is False:
            return Response({'error': ser.errors})
        # User can only have one credit card for now.
        if req.user.creditcard_set.count() > 0:
            return Response({'error':
                             'User has already registered a credit card.'},
                            status=401)
        if req.user.stripe_id is None:
            client = StripeWrapper()
            created, res = client.create_customer(
                user=req.user,
                exp_month=ser.data.get('exp_month'),
                exp_year=ser.data.get('exp_year'),
                number=ser.data.get('card_number'),
                cvc=ser.data.get('cvc'),
                token=ser.data.get('stripe_token')
            )
            if created:
                req.user.stripe_id = res.get('customer_id')
                req.user.save()
                card = CreditCard(
                    name=res.get('name'),
                    last_four=res.get('last_four'),
                    exp_month=res.get('exp_month'),
                    exp_year=res.get('exp_year'),
                    user=req.user,
                    stripe_id=res.get('card_id'),
                )
                card.save()
                return Response(CreditCardSerializer(card).data)
            else:
                return Response({'error': res}, status=401)
        else:
            # If user has a stripe_id then he should already have a card as
            # well. If reached here, something wrong with logic.
            print('already customer')
        return Response({'error': 'User already has a credit card on file. \
            Try editing the card.'}, status=401)


class CreditCardView(APIView):
    """
    get:
    Returns user's credit card info.
    put:
    Edit a user's credit card.
    """
    permission_classes = (IsAuthenticated, EmailConfirmed,)

    def get(self, req):
        cards = req.user.creditcard_set
        if cards.count() == 0:
            return Response({'error':
                             'User has not registered a credit card.'},
                            status=404)
        # User can only have on credit card on file. Added one-to-many in case
        # need to change in future.
        return Response(CreditCardSerializer(cards.first()).data)

    def put(self, req):
        cards = req.user.creditcard_set
        if cards.count() == 0:
            return Response({'error':
                             'User has not registered a credit card.'},
                            status=404)
        card = cards.first()
        d = req.data
        exp_month = d.get('exp_month')
        exp_year = d.get('exp_year')
        client = StripeWrapper()
        updated, res = client.update_card(req.user, card, exp_month=exp_month,
                                          exp_year=exp_year)
        if updated:
            return Response(CreditCardSerializer(res).data)
        return Response({'error': res}, status=401)
