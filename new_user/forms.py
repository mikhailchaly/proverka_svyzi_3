from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from new_user.utils import send_email_for_verify

User = get_user_model()


class MyAuthenticationForm(AuthenticationForm):

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password,
            )

            try:  # После добавления этого исключения, пропала ошибка, когда мы после смены пароля вводили новый пароль к другому емайлу
                if not self.user_cache.email_verify:
                    send_email_for_verify(self.request, self.user_cache)
                    raise ValidationError(
                        "Емаил не верифицирован, войдите в почту и перейдите по ссылке",
                        code="invalid_login",
                    )
            except:
                pass
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class MyUserCreationForm(UserCreationForm):

    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'state']
