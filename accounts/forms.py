from typing import Any, Dict
from .models import User, UserProfile
from django import forms

class RegistrationForm(forms.ModelForm):  # Fixed typo
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter Password", "class": "form-control"}
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter Password", "class": "form-control"}
        )
    )

    class Meta:
        model = User
        fields = [
            "name",
            "email",
            "password",
        ]

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)  # Fixed typo
        self.fields["name"].widget.attrs["placeholder"] = "Enter Name"
        self.fields["email"].widget.attrs["placeholder"] = "Enter Email Address"
  
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "name",
        ]

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


class UserProfileForm(forms.ModelForm):
  

    class Meta:
        model = UserProfile
        fields = [
            "address",
            "city",
            "state",
            "country",
        ]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"