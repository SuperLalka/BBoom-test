from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView

from bboom_test.settings import AUTHENTICATION_COOKIE_NAME


class CustomTokenObtainPairView(TokenObtainPairView):

    def post(self, request: Request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = response.data["access"]
        response.set_cookie(AUTHENTICATION_COOKIE_NAME, token, httponly=True)
        return response


class CustomLogoutView(APIView):

    def get(self, request: Request):
        response = Response("Success", status=status.HTTP_200_OK)
        response.delete_cookie(AUTHENTICATION_COOKIE_NAME)
        return response
