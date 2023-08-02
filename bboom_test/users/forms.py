from django import forms
from django.contrib.auth.forms import UsernameField
from django.core.exceptions import ValidationError
from django.utils.text import capfirst

from users.models import User
from users.backends import CustomModelBackend


class PostForm(forms.Form):
    title = forms.CharField(
        label="Title",
        max_length=255
    )
    body = forms.CharField(
        label="Body",
        max_length=1000,
        widget=forms.Textarea(attrs={'rows': 3})
    )


class CustomAuthenticationForm(forms.Form):
    name = UsernameField(label="Name", widget=forms.TextInput(attrs={"autofocus": True}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput())

    error_messages = {
        "invalid_login": (
            "Please enter a correct %(name)s and email. Note that both "
            "fields may be case-sensitive."
        ),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        self.fields["name"].max_length = 255
        self.fields["name"].widget.attrs["maxlength"] = 255

    def clean(self):
        name = self.cleaned_data.get("name")
        email = self.cleaned_data.get("email")

        if name is not None and email:
            self.user_cache = CustomModelBackend().authenticate(
                self.request, name=name, email=email
            )

            if self.user_cache is None:
                raise self.get_invalid_login_error()

        return self.cleaned_data

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
            params={"name": self.username_field.verbose_name},
        )
