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
            msg = 'Card was declined.'
            return False, msg
        except stripe.error.InvalidRequestError as e:
            return False, e
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
            return False, e
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
