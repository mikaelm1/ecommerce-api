from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from django.db.models import Q
from django.conf import settings
from django.views import View
from django.shortcuts import redirect, render
from .models import User
from .tasks import send_acct_confirm_email
from .tokens import account_activation_token


class LoginView(APIView):
    """
    post:
    Verify and return JWT token.
    """
    # authentication_classes = (JSONWebTokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def post(self, req):
        data = req.data
        ident = data.get('identifier')
        pwd = data.get('password')
        user = User.objects.filter(
            Q(username=ident) |
            Q(email=ident)
        ).first()
        if user and user.email_verified is False:
            return Response({'error': 'Your email is not verified.'},
                            status=401)
        if user and user.check_password(pwd):
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response({'user': user.to_json(), 'token': token})
        return Response({'error': 'Invalid login credentials.'}, status=401)


class UserRegister(APIView):
    """
    post:
    Create new account. Sends confirmation email.
    """
    def post(self, req):
        d = req.data
        username = d.get('username')
        email = d.get('email')
        pwd = d.get('password')
        user = User.objects.filter(email=email)
        if user:
            return Response({'error':
                             'An account with that email already exists.'},
                            status=404)
        user = User.objects.filter(username=username)
        if user:
            return Response({'error':
                             'An account with that username already exists.'},
                            status=404)
        if len(pwd) < settings.MIN_PASSWORD_LENGTH:
            return Response({'error':
                             'Password must be at least {} characters long'
                             .format(settings.MIN_PASSWORD_LENGTH)})
        user = User.objects.create_user(username=username, email=email,
                                        password=pwd)
        url = req.build_absolute_uri('/auth/confirm-email')
        uid = user.id * settings.EMAIL_CONFIRM_HASH_NUM
        token = account_activation_token.make_token(user)
        url += '?token={}&uid={}'.format(token, uid)
        send_acct_confirm_email.delay(user.id, url)
        return Response({'user': user.to_json()})


class ConfirmAcct(View):
    def get(self, req):
        confirmed = False
        token = req.GET.get('token')
        uid = int(float(req.GET.get('uid')) / settings.EMAIL_CONFIRM_HASH_NUM)
        if token and uid:
            user = User.objects.filter(id=uid).first()
            if user is None:
                confirmed = False
            elif user.email_verified:
                print('Email is already verified')
                confirmed = True
            else:
                if account_activation_token.check_token(user, token):
                    user.email_verified = True
                    user.save()
                    confirmed = True
        return render(req, 'auth/confirm.html',
                      {'confirmed': confirmed, 'uid': uid})


class ResendConfirmEmail(View):
    def get(self, req, *args):
        # TODO: redirect to front end app
        uid = req.GET.get('uid')
        user = User.objects.filter(id=uid).first()
        print(uid)
        print(user)
        if user is None:
            print('User not found')
        elif user.email_verified:
            print('email already confirmed')
            return redirect('/')
        else:
            url = req.build_absolute_uri('/auth/confirm-email')
            uid = user.id * settings.EMAIL_CONFIRM_HASH_NUM
            token = account_activation_token.make_token(user)
            url += '?token={}&uid={}'.format(token, uid)
            send_acct_confirm_email.delay(user.id, url)
        return redirect('/')