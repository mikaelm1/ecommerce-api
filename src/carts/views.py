from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.models import User


class CartDetailView(APIView):
    """
    Returns user's cart.
    """
    def get(self, req, uid, cid):
        user = User.objects.filter(id=uid).first()
        if user is None:
            return Response({'error': 'User not found.'}, status=404)
        
        # if req.user.is_staff is False and 
        return Response({})
