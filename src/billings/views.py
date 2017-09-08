from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ecommerce.permissions import EmailConfirmed
from .utils_stripe import StripeWrapper
from .models import CreditCard
from .serializers import CreditCardSerializer

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
        # User can only have one credit card for now.
        if req.user.creditcard_set.count() > 0:
            return Response({'error':
                             'User has already registered a credit card.'},
                            status=401)
        if req.user.stripe_id is None:
            client = StripeWrapper()
            created, res = client.create_customer(user=req.user,
                                                  exp_month=d.get('exp_month'),
                                                  exp_year=d.get('exp_year'),
                                                  number=d.get('card_number'),
                                                  cvc=d.get('cvc'),
                                                  token=d.get('stripe_token'))
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
