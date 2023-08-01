from rest_framework.authtoken.views import ObtainAuthToken

from users.serializers.auth import CustomAuthTokenSerializer


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
