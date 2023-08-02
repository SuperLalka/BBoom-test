from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from rest_framework_simplejwt.authentication import JWTAuthentication

from bboom_test.settings import AUTHENTICATION_COOKIE_NAME
from users.models import User


class CustomModelBackend(ModelBackend):
    def authenticate(self, request, name=None, email=None, **kwargs):
        user = User.objects.filter(name=name, email=email).first()

        if user and self.user_can_authenticate(user):
            return user


class CustomJWTAuthentication(JWTAuthentication):
    www_authenticate_realm = "api"
    media_type = "application/json"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = get_user_model()

    def authenticate(self, request):
        cookie = request.COOKIES.get(AUTHENTICATION_COOKIE_NAME)
        if cookie:
            raw_token = cookie.encode()
            validated_token = self.get_validated_token(raw_token)
            return self.get_user(validated_token), validated_token
