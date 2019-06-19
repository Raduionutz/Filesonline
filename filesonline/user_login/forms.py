from django import forms
from django.contrib.auth.models import User
from .models import UserExtraInfo

class RegForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')

class ExtraRegForm(forms.ModelForm):

    class Meta():
        model = UserExtraInfo
        fields = ('user_picture', 'vault_key')

