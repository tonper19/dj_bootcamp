from django.contrib.auth import get_user_model
from django import forms
# check for unique email and username

User = get_user_model()


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password",
            }
        )
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-confirm-password",
            }
        )
    )

    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)
        if qs.exists():
            raise forms.ValidationError(
                "This is an invalid username, pick another one")
        return username

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError(
                "This is an invalid email, pick another one")
        return email


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password",
            }
        )
    )

    # def clean(self):
    #     username = self.cleaned_data.get("username")
    #     password = self.cleaned_data.get("password")

    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)
        if not qs.exists():
            raise forms.ValidationError("Invalid user")
        return username
