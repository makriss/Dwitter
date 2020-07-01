from django.contrib.auth import get_user_model
from django import forms


class LoginUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']
