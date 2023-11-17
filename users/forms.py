from django import forms
from .models import Users

class signUpForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['role', 'firstName', 'lastName', 'email', 'userName', 'password']
        widgets = {'password': forms.PasswordInput()}