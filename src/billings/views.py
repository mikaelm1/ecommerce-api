from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ecommerce.permissions import EmailConfirmed


class CreateCreditCardView(APIView):
    """
    post:
    Create a new CreditCard for a user.
    """
    permission_classes = (IsAuthenticated, EmailConfirmed,)
    
    def post(self, req):
        return Response({})
