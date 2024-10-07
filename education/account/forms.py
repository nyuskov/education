from typing import Any
from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm)
from django.contrib.auth.models import User
from django.forms import ModelForm, ValidationError


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'username'
        self.fields['password1'].widget.attrs['placeholder'] = 'password'
        self.fields['password2'].widget.attrs['placeholder'] = 'password'


class CustomUserForm(ModelForm):
    class Meta:
        model = User
        fields = ("username", "password",
                  "groups", "first_name", "last_name",
                  "email", "user_permissions",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["readonly"] = True
        self.fields["groups"].widget.attrs["readonly"] = True
        self.fields["user_permissions"].widget.attrs["readonly"] = True

    def clean(self):
        data = super().clean()

        for key in ("username", "groups", "user_permissions"):
            new_data = data.get(key)

            if key in ("groups", "user_permissions"):
                initial_data = list(self.initial[key])
            else:
                initial_data = self.initial[key]

            if new_data and initial_data != new_data:
                self.add_error(key, ValidationError(
                    "This field is readonly"))

        return data


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'username'
        self.fields['password'].widget.attrs['placeholder'] = 'password'
