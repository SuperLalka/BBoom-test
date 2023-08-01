from django.contrib.auth.backends import ModelBackend

from users.models import User


class CustomModelBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, **kwargs):
        user = User.objects.filter(name=username, email=email).first()

        if user and self.user_can_authenticate(user):
            return user
