from typing import ClassVar

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

INPUT_CLASS = "w-full rounded-xl border-gray-200 bg-gray-50 px-4 py-3 text-sm focus:border-[#6d4c41] focus:ring-[#6d4c41]"


class LoginForm(AuthenticationForm):
    error_messages: ClassVar[dict] = {
        "invalid_login": "❌  Invalid username or password. Try again.",
        "inactive": "😴  This account is inactive.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"placeholder": "👤  Username", "class": INPUT_CLASS}
        )
        self.fields["password"].widget.attrs.update(
            {"placeholder": "🔒  Password", "class": INPUT_CLASS}
        )


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"placeholder": "👤  Choose a username", "class": INPUT_CLASS}
        )
        self.fields["username"].help_text = ""
        self.fields["email"].widget.attrs.update(
            {"placeholder": "📧  Email (optional)", "class": INPUT_CLASS}
        )
        self.fields["password1"].widget.attrs.update(
            {"placeholder": "🔒  Password", "class": INPUT_CLASS}
        )
        self.fields["password1"].help_text = ""
        self.fields["password2"].widget.attrs.update(
            {"placeholder": "🔒  Confirm password", "class": INPUT_CLASS}
        )
        self.fields["password2"].help_text = ""

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if (
            email
            and User.objects.filter(email=email).exclude(pk=self.instance.pk).exists()
        ):
            raise forms.ValidationError("⚠️  This email is already registered.")
        return email
