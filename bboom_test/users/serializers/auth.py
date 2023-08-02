
from django.contrib.auth import authenticate

from rest_framework import serializers


class CustomAuthTokenSerializer(serializers.Serializer):
    name = serializers.CharField(
        write_only=True
    )
    email = serializers.EmailField(
        write_only=True
    )
    token = serializers.CharField(
        read_only=True
    )

    def validate(self, attrs):
        name = attrs.get('name')
        email = attrs.get('email')

        if name and email:
            user = authenticate(
                request=self.context.get('request'),
                name=name, email=email
            )
            if not user:
                raise serializers.ValidationError(
                    'Authorization failed, please check your credentials.',
                    code='authorization'
                )
        else:
            raise serializers.ValidationError(
                'Must include "name" and "email".',
                code='authorization'
            )

        attrs['user'] = user
        return attrs
