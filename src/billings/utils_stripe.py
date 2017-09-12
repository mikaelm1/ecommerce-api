import stripe
from functools import wraps
from django.conf import settings


def handle_stripe_errors(f):
    """
    A decorator for gracefully handling Stripe's errors.
    """
    @wraps(f)
    def decorated_func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except stripe.error.CardError as e:
            print(e)
            return False, e._message
        except stripe.error.InvalidRequestError as e:
            print(e)
            return False, e._message
        except stripe.error.AuthenticationError:
            msg = 'Stripe authentication failed.'
            return False, msg
        except stripe.error.APIConnectionError:
            msg = 'Network communication with Stripe failed. Try again.'
            return False, msg
        except stripe.error.RateLimitError as e:
            return 'Too many requests made to Stripe too quickly'
        except stripe.error.StripeError as e:
            print('got stripe error')
            return False, e._message
        except Exception as e:
            print(e)
            return False, 'Unknown error occured. Ensure all card details are provided.'
    return decorated_func


class StripeWrapper:
    stripe.api_key = settings.STRIPE_SECRET_KEY

    @handle_stripe_errors
    def create_customer(self, user, exp_month, exp_year, number, cvc, token):
        """
        Create a Stripe customer with a credit card.
        """
        if settings.TESTING:
            res = {
                'customer_id': 'cid',
                'card_id': 'id',
                'name': 'brand',
                'exp_month': 10,
                'exp_year': 2020,
                'last_four': 1234,
            }
            return True, res
        customer = stripe.Customer.create(
            description='Customer for {}'.format(user.email),
            source=token
        )
        card = customer['sources']['data'][0]
        res = {
            'customer_id': customer['id'],
            'card_id': card['id'],
            'name': card['brand'],
            'exp_month': card['exp_month'],
            'exp_year': card['exp_year'],
            'last_four': card['last4'],
        }
        return True, res

    @handle_stripe_errors
    def update_card(self, user, card, exp_month=None, exp_year=None):
        """
        Update user's credit card.
        """
        if settings.TESTING:
            card.exp_month = exp_month
            card.exp_year = exp_year
            card.save()
            return True, card
        customer = stripe.Customer.retrieve(user.stripe_id)
        c = customer.sources.retrieve(card.stripe_id)
        if exp_month:
            c.exp_month = exp_month
            card.exp_month = exp_month
        if exp_year:
            c.exp_year = exp_year
            card.exp_year = exp_year
        c.save()
        card.save()
        return True, card

    @handle_stripe_errors
    def make_purchase(self, user, amount, description, currency='usd'):
        """
        Charge a user's credit card for a given amount.
        """
        if settings.TESTING:
            return True, {'id': 'stripe_id'}
        charge = stripe.Charge.create(
            amount=amount,
            currency=currency,
            customer=user.stripe_id,
            description=description
        )
        return True, charge
