# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import QRCode

# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Please provide a valid email address.")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')

        # Alphanumeric check
        if not re.match("^[a-zA-Z0-9]*$", username):
            raise forms.ValidationError("Username can only contain letters and numbers.")

        # Minimum length check
        if len(username) < 5:
            raise forms.ValidationError("Username must be at least 5 characters long.")

        # Minimum letter count check
        letters_count = sum(c.isalpha() for c in username)
        if letters_count < 3:
            raise forms.ValidationError("Username must contain at least 3 letters.")

        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not re.search("[A-Z]", password1):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search("[a-z]", password1):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search("[0-9]", password1):
            raise forms.ValidationError("Password must contain at least one digit.")
        if not re.search("[@#$%^&+=]", password1):
            raise forms.ValidationError("Password must contain at least one special character (@, #, $, etc.).")

        return password1

'''class UserRegistrationForm(forms.ModelForm):
    """
    A form for registering new users. Includes all the required
    fields, plus a repeated password for verification.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_password_confirm(self):
        # Ensure the passwords match
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        return password_confirm
'''
class CSVUploadForm(forms.Form):
    """
    A form for uploading a CSV file. The CSV is used to generate QR codes.
    """
    csv_file = forms.FileField()